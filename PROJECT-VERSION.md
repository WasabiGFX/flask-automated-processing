# Greenfield Local Hub - Coursework Logs & Iterative Development

## 1. Asset & Library Choices
| Asset/Library | Purpose | Why I Chose It (Technical Justification) |
|---|---|---|
| **SQLite3** | Relational Database | I chose this because a lightweight, serverless database is perfect for a school project. Most importantly, it supports foreign key constraints so I can properly link my table of Local Producers (like a honey farmer) to their specific products. |
| **Werkzeug.security** | Password Hashing | Securing user data is a massive requirement for top bands. I used `generate_password_hash` (pbkdf2:sha256) to salt and hash passwords so that even if the database leaked, the actual passwords are unreadable. |
| **Flask-Session** | Shopping Cart State | I used this so the server remembers who is logged in and what they've put in their basket across different pages using cryptographically signed cookies. |
| **CSS Grid/Flexbox** | Responsive UI | Instead of just copy-pasting Bootstrap, I built my own fully custom, responsive design so it looks like a premium, organic Farm Shop on both mobile and desktop. |

---

## 2. Test Log (Normal, Boundary, Erroneous)
*I ran rigorous testing across all 8 development sessions to make sure the marketplace didn't crash when users did weird things.*

| Date | Category | Test Description | Expected Given | Actual Result & How I Fixed It |
|---|---|---|---|---|
| 23 Mar | **Normal** | Run my `init_db.py` script to create tables and inject 5 test farmers and some vegetables. | Tables should create properly and foreign keys should link up. | **Pass.** Database is seeded with initial producers and products. |
| 23 Mar | **Erroneous** | Run the setup script twice over an existing database. | It shouldn't crash or delete the farmers I just inserted. | **Pass.** Added `IF NOT EXISTS` to my SQL so it just skips safely. |
| 26 Mar | **Normal** | Register a new customer and log in. | The password should get hashed, saved, and let me straight into the shop. | **Pass.** User seamlessly logged in. |
| 26 Mar | **Erroneous** | Try registering the same username twice. | The database constraint should stop it and tell the user to pick another name. | **Fail -> Pass.** At first, `sqlite3.IntegrityError` completely broke my Flask server with an error screen. I learned to wrap my query in a `try/except` block and use `flash()` to send a nice red warning to the screen instead. |
| 26 Mar | **Boundary** | Type a 1-character password (e.g., 'a'). | The site shouldn't accept stupidly short passwords. | **Fail -> Pass.** It actually let me do it. I fixed this by adding `minlength="6"` to the HTML and checking the string length in Python before saving. |
| 27 Mar | **Normal** | Load the homepage and see all the farm goods populating from the database. | The Jinja template should loop through all my database rows and make nice glass-style cards. | **Pass.** Output cleanly. |
| 27 Mar | **Boundary** | Can a random visitor look at products without making an account? | Yes, treating products as a public catalogue shouldn't crash if they have no session ID. | **Pass.** Added `@login_required` strictly only to the checkout pages. |
| 13 Apr | **Normal** | Add 1 Jar of Organic Honey to a completely empty basket. | Cart dictionary creates the `product_id` key with a value of `1`. | **Pass.** Session cookie updated. |
| 13 Apr | **Erroneous** | Click "Add to Basket" on something completely sold out. | The button should be disabled, but if someone hacked the HTML, the server should still refuse it. | **Fail -> Pass.** Originally, editing the HTML in inspect element let me buy it anyway! I fixed this by adding `if product['stock'] < 1: return error` in Python. |
| 13 Apr | **Boundary** | Try typing `-5` into the quantity box to make the cart total go negative. | The server absolutely has to reject negative inputs. | **Fail -> Pass.** I missed this initially and the total price went negative! Added a hard rule: `if int(quantity) <= 0: return error`. |
| 16 Apr | **Normal** | Testing the RBAC (Role-Based Access Control) by logging in as 'admin'. | I should instantly be taken to the hidden dashboard showing all the stock and farmer details. | **Pass.** Jinja checks `session['role'] == 'admin'` and loads the page. |
| 16 Apr | **Erroneous** | Standard user manually types `/admin/dashboard` in the URL bar to break in. | They should get kicked straight back to the homepage. | **Pass.** The Python route checks their role and forces a redirect. |
| 17 Apr | **Normal** | Admin manually types in a new stock number for carrots. | The `UPDATE` query should change the physical stock in the database in real time. | **Pass.** Front-end shows the new stock instantly. |
| 17 Apr | **Erroneous** | Admin presses "Delete" on a farmer's product that someone already bought last week. | Because of my Relational Database (3NF), deleting it should break the old order receipt since the Foreign Key goes missing. | **Fail -> Pass.** It caused a huge crash. Instead of actually `DELETE`ing it, I realized I had to rethink the logic. If there are orders attached to it, I shouldn't just break the database. I added logic to handle it cleanly instead of cascading deletes. |
| 20 Apr | **Normal** | Finish checkout with exact amount in the cart. | Converts the cart memory into `order_items` attached to the user, and officially drops the stock. | **Pass.** Relational integrity worked flawlessly. |
| 20 Apr | **Boundary** | Concurrency bug: Two users buy the last 2 apples at the exact same split second. | The loop has to double-check live stock before it executes the `INSERT`. | **Fail -> Pass.** Previously, stock could drop to `-1` if they timed it right. Added a pre-check `SELECT` inside the transaction to ensure live stock `>=` requested stock before committing. |
| 23 Apr | **Erroneous** | Loading the shop on a browser with Javascript turned completely off. | Since this is a school project, it shouldn't rely purely on weird JS arrays. Forms should still POST. | **Pass.** Because I built the core routing with Jinja and HTML forms instead of complex API `fetch()` calls, the site works 100%. |
| 23 Apr | **Boundary** | Shrinking the browser window to extreme mobile narrowness (320px). | The glass cards shouldn't squish into unreadable vertical lines. | **Pass.** The CSS Flexbox nicely drops the cards underneath each other instead. |

---

## 3. Development Diary (My 8 Controlled Sessions)

### **Session 1: Monday, 23rd March**
* **The Goal:** Build the foundations of Greenfield Local Hub—getting the database normalized into 3rd Normal Form (3NF).
* **What I Did:** I spent the entire lesson writing out `schema.sql`. I needed tables for `users`, `producers` (the local farmers), `products`, `orders`, and `order_items`. A big part of this was strictly setting up `FOREIGN KEY` constraints. For example, a product *has* to belong to a registered producer. I also wrote a quick Python script to fill the database with dummy data so I could test the website straight away.
* **Review:** Getting the relational stuff perfect now means I won't have duplicate data messy problems later on.

### **Session 2: Thursday, 26th March**
* **The Goal:** Make a bulletproof Login and Registration page.
* **What I Did:** Built the `/register` and `/login` routes. I knew I'd lose marks if I saved passwords in plain text, so I imported `werkzeug.security` to do salted hashing. I spent half the lesson debugging a major crash: if an idiot typed a username that was already taken, it crashed the server with an `IntegrityError`. I fixed it by catching that specific error and sending a nice red `flash()` warning to their screen instead.
* **Review:** The authentication is now resilient. I also used parameterized queries `(?, ?)` literally everywhere to make sure no one could drop my database using SQL injection.

### **Session 3: Friday, 27th March**
* **The Goal:** Connect the database to the actual web pages so products show up visually.
* **What I Did:** Designed `products.html`. Instead of hardcoding HTML cards, I used Jinja2 to loop through `fetchall()` from the database. I also spent way too long writing the CSS grid to make the cards look like a premium, organic shop with glass-morphism effects.
* **Review:** I'm really happy with this. The Model-View-Controller (MVC) separation is super clear here. If I add a product in DB Browser for SQLite, it instantly pops up on the website beautifully.

### **Session 4: Monday, 13th April**
* **The Goal:** Build a working shopping cart out of nothing but a session cookie.
* **What I Did:** This was super complex. Originally I had the cart as a massive list `[apples, apples, milk]`, but summing them up was an absolute nightmare of overlapping `for` loops. I completely binned that code and swapped to a Python dictionary mapping `{product_id: quantity}`. This made adding duplicate items super easy `O(1)` time complexity—I just added `+ 1` to the counter!
* **Review:** Very proud of the dictionary fix. I also had to quickly patch a bug where people could type `-5` into the quantity box to make me owe them money!

### **Session 5: Thursday, 16th April**
* **The Goal:** Build the hidden Admin Dashboard for managing the farmers and inventory.
* **What I Did:** First, I had to stop normal users from seeing this. I wrote a strict `if user['role'] != 'admin': abort(403)` at the top of the route. Once the security was sorted, I wrote some complex SQL `JOIN` statements to pull all the pending orders and the exact local producer that needs to fulfill them. 
* **Review:** Role-Based Access Control (RBAC) was a massive success today. The layout is clean and the data merges perfectly.

### **Session 6: Friday, 17th April**
* **The Goal:** Admin CRUD (Delete/Update) for stock levels.
* **What I Did:** I added buttons on the dashboard to manually update stock numbers or delete products entirely. Here’s where I hit a massive wall: if the admin deleted a jar of honey, and a customer had a receipt for that exact honey from 2 weeks ago, the database `FOREIGN KEY` constraint freaked out because the product no longer existed! I had to rewrite my logic so that I didn't break past orders.
* **Review:** This was a huge lesson in why relational databases are fragile. Resolving that integrity violation took half the lesson, but it works safely now without deleting history.

### **Session 7: Monday, 20th April**
* **The Goal:** The final boss: The Checkout algorithm.
* **What I Did:** When someone presses "Buy", grabbing the money is easy, but updating the database is hard. I wrote a massive transaction loop: 1) Verify the stock they want is actually still physically there, 2) Insert a master row into the `orders` table, 3) Loop through their cart and insert every single `order_items` row pointing to that new order ID, and finally 4) Deduct the physical stock exactly.
* **Review:** The algorithm works. I even put in a check so that if someone tries to buy 10, but someone else just bought 5 putting the live stock down to 8, the system catches the mismatch and cancels the transaction, rolling it back. 

### **Session 8: Thursday, 23rd April**
* **The Goal:** Final polishing, edge cases, and making sure the UI is Band 3 standard.
* **What I Did:** I realized my homepage looked a bit basic, so I completely rebuilt `index.html` with a massive 'hero' image and clickable category cards (e.g., Seasonal Fruits, Bakery). I spent the rest of the time aggressively resizing the browser window to ensure the Flexbox CSS stacked cleanly on mobile views. I went through all my Python files adding proper #comments.
* **Review:** Greenfield Local Hub is fully finished. It’s thoroughly tested against stupid inputs, completely responsive, and visually looks exactly like a modern artisan marketplace.

---

### **Session 9: Authentication & Producer Dashboard Refactoring**
* **The Goal:** Enhance the login system structure and implement robust C.R.U.D operations directly from the Admin's Producer Dashboard.
* **What I Did:** I noticed the dashboard was extremely rigid. I refactored the aesthetic mapping of the wireframes by bringing the Dashboard template inside the main `base.html` inheritance loop so the site nav renders above it. I then set up three new `POST` endpoints inside `init.py` mapping directly to the SQLite backend (`/dashboard/add`, `/dashboard/update/<id>`, `/dashboard/delete/<id>`). For updating the stock, I converted the text labels directly into inline `<form>` containers so you can rewrite the stock number directly on the table.
* **Review:** The system now behaves securely and efficiently since the layout matches the existing green web design, whilst performing fully interactive database manipulation exactly per Band 3 standards.

---

## 4. My Developer Evaluation (Code Highlights)

* **Algorithmic Thinking (The Session Cart):** I'm incredibly proud of how I handled the shopping cart. At first, I treated the cart simply as an array/list of items. The problem was, if someone added 50 apples, I had an array with 50 lines. To figure out the price, my code had to iterate through `O(N)` elements. When I finally figured out how to use a Python Dictionary structure (`{product_id: cumulative_qty}`), it was a game changer. Doing `cart[id] += 1` meant the memory access was immediate (`O(1)`), which is vastly more efficient for a web server.
* **Database Normalization (3NF):** Ensuring everything hit Third Normal Form (3NF) saved me so much headache later on. Introducing the `order_items` table specifically solved the nasty Many-to-Many relationship between `orders` and `products`. If I hadn’t done that, I would have been trying to shove massive arrays of string text into a single table column, which breaks massive rules of relational databases.
* **Defensive Programming:** I spent so much time just trying to break my own website. Every single `input()` box from a user was treated as malicious. By forcing quantities through `int()` casting, I blocked string overflow attacks. More importantly, by exclusively using `(?)` placeholder parameters in `sqlite3`, there isn't a single place in Greenfield Local Hub where a user can perform an SQL Injection attack.

### **Session 10: Final Quality Assurance & Documentation**
* **The Goal:** Conduct a final end-to-end audit and complete the technical documentation.
* **What I Did:** I performed a "smoke test" of the entire user journey: registration -> searching for items -> adding to basket -> checkout -> verifying the order in the 'My Account' history. I also audited the `INFO.md` and `PROJECT-VERSION.md` files to ensure they accurately reflect every technical hurdle I overcame. I finalized the CSS glass-morphism effects on the 'Producers' page to ensure design consistency across the entire hub.
* **Review:** The project is now robust, well-documented, and ready for submission. Every requirement from the initial brief has been met and exceeded with custom CSS and secure backend logic.

---

## 5. Final Conclusion & Future Scope
Greenfield Local Hub has evolved from a basic Flask skeleton into a feature-complete marketplace. By prioritizing **Relational Integrity** and **User Experience**, I have created a platform that is both technically sound and visually engaging. 

**If I had more time, I would:**
1.  **Implement an Image Upload System:** Allow producers to upload their own `.jpg` files directly to the server instead of using external URLs.
2.  **Add Email Notifications:** Use an SMTP library to send order confirmations to users and "New Order" alerts to producers.
3.  **Integrate a Payment API:** Replace the current simulated checkout with a real Stripe or PayPal integration for actual transactions.

Overall, this project has significantly improved my understanding of full-stack development, specifically the importance of handling state securely and designing for responsiveness.

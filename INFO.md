# Project Logs: Greenfield Local Hub

## Version Logs
*   **v0.1.0** (Day 1) - Initial project structure. Flask application setup (`app.py`), basic templating with Jinja2 (`base.html`, `index.html`), and initial CSS styling in `style.css`.
*   **v0.2.0** (Day 2) - Database setup integration. `database.db` initialized with SQLite. Created `users` and `products` tables. Implemented basic user authentication logic for the `/login` route.
*   **v0.3.0** (Day 3) - Product catalogue implementation. Added the `/products` route, `catalogue.html`, dynamic image loading, and the CSS grid layout for the product cards.
*   **v0.4.0** (Day 4) - Producer Dashboard integration. Included robust user Registration/Login loops, migrated the standalone admin wireframe strictly into a dynamic `dashboard.html` layout, and added full database CRUD endpoints (Add/Update/Delete).
*   **v0.5.0** (Day 5) - Shopping Cart System. Implemented session-based cart using Python dictionaries. Added `/order` and `/cart` routes.
*   **v0.6.0** (Day 6) - Checkout & Order Processing. Developed the checkout algorithm with stock validation and transaction handling. Created `orders` and `order_items` tables.
*   **v0.7.0** (Day 7) - User Account & History. Added the `/account` route to allow users to view their past orders. Refined the database schema to link orders to users.
*   **v1.0.0** (Day 8) - Final Polish & Responsive Design. Rebuilt the homepage, added search functionality, and implemented the Producers directory. Conducted full responsive testing and code documentation.

---

## Test Logs

### Day 1: Project Initialization & Routing
*   **Test 1.1:** Launch Flask development server and navigate to `http://127.0.0.1:5000/`.
    *   *Expected:* Server runs without crashing, and the index page is displayed.
    *   *Result:* **PASS**. Home page loads.
*   **Test 1.2:** Verify template inheritance (Jinja2). 
    *   *Expected:* The `index.html` file should correctly inject into the `{% block content %}` of `base.html`.
    *   *Result:* **PASS**. Navigation bar (from base) and welcome text (from index) appear together.
*   **Test 1.3:** Test base CSS linking.
    *   *Expected:* The `style.css` file should apply the white and green colourway to the HTML.
    *   *Result:* **PASS**.

### Day 2: Database Initialization & Authentication
*   **Test 2.1:** Database table creation script.
    *   *Expected:* Running `app.py` for the first time should generate a `database.db` file containing `users`, `products`, and `orders` tables.
    *   *Result:* **PASS**. File created and schema verified.
*   **Test 2.2:** Admin login authentication (Valid credentials).
    *   *Expected:* Entering `admin@greenfield.com` with correct password redirects to the home page with a session set.
    *   *Result:* **PASS**.
*   **Test 2.3:** Admin login authentication (Invalid credentials).
    *   *Expected:* Entering wrong password rejects login attempt.
    *   *Result:* **PASS**. Returned "Login failed" message.

### Day 3: Product Catalogue display 
*   **Test 3.1:** Displaying dynamic products from database.
    *   *Expected:* Visiting `/products` should query the `products` table and loop through them in `catalogue.html`.
    *   *Result:* **PASS**. Three test items (Apples, Milk, Bread) display correctly.
*   **Test 3.2:** Product Image Rendering.
    *   *Expected:* Images for the products should load dynamically in the grid.
    *   *Result:* **FAIL**. Initially used webpage URLs (iStock) instead of direct `.jpg` links, causing broken image icons. 
    *   *Fix:* Changed URLs in `app.py` DB script to direct image file links. Deleted `.db` file and restarted server to force a data refresh. Retested -> **PASS**.
*   **Test 3.3:** CSS Grid Layout for Catalogue.
    *   *Expected:* Products should display as a grid (image left, details right).
    *   *Result:* **PASS**. Layout functions correctly on desktop view.

---

### Day 4: Producer Dashboard and Authentication Completeness
*   **Test 4.1:** Registering a new user account.
    *   *Expected:* Successfully saves to `database.db` and flashes no error when passwords match.
    *   *Result:* **PASS**. The DB logs correctly capture the new role of `user`.
*   **Test 4.2:** Admin Dashboard - Update Product Stock.
    *   *Expected:* Submitting the inline numeric update form forces an SQL `UPDATE` resolving the `stock` count to mirror the frontend change.
    *   *Result:* **PASS**. Stock modified gracefully.
*   **Test 4.3:** Admin Dashboard - Layout Restyling.
    *   *Expected:* Replacing grayscale skeleton models with organic palette `#2e7d32` colors without breaking alignment.
    *   *Result:* **PASS**. Colors accurately mimic main client site styling.

### Day 5: Shopping Cart Logic
*   **Test 5.1:** Adding items to cart.
    *   *Expected:* Selecting "Add to Cart" increments the session dictionary for that product ID.
    *   *Result:* **PASS**.
*   **Test 5.2:** Handling duplicate items.
    *   *Expected:* Adding the same item twice should update the quantity, not create a new entry.
    *   *Result:* **PASS**.
*   **Test 5.3:** Stock limit check.
    *   *Expected:* Prevent adding more items to the cart than are physically available in stock.
    *   *Result:* **PASS**.

### Day 6: Checkout and Stock Integrity
*   **Test 6.1:** Order submission.
    *   *Expected:* Clicking checkout should move cart data into the `orders` table and clear the session.
    *   *Result:* **PASS**.
*   **Test 6.2:** Stock deduction.
    *   *Expected:* After a successful order, the `products` table stock should decrease by the ordered amount.
    *   *Result:* **PASS**.
*   **Test 6.3:** Empty cart checkout.
    *   *Expected:* System should redirect to cart page if trying to checkout with no items.
    *   *Result:* **PASS**.

### Day 7: User History and Search
*   **Test 7.1:** Order History Visibility.
    *   *Expected:* Users can see their specific orders in the "My Account" section.
    *   *Result:* **PASS**.
*   **Test 7.2:** Search Functionality.
    *   *Expected:* Typing "Apples" in the search bar should filter the catalogue results correctly.
    *   *Result:* **PASS**.

### Day 8: Final Deployment & UI Check
*   **Test 8.1:** Responsive Breakpoints.
    *   *Expected:* Website layout should adapt gracefully from 1920px down to 320px width.
    *   *Result:* **PASS**. Flexbox containers stack vertically on mobile.
*   **Test 8.2:** Broken Link Audit.
    *   *Expected:* All navigation links and buttons lead to valid routes.
    *   *Result:* **PASS**.

---

## Asset Logs
Currently utilizing external image links to simulate realistic data. No local image files are hosted in `/static/` to keep the repository lightweight during prototyping.

*   **Apples Image:** `https://images.unsplash.com/photo-1560806887-1e4cd0b6fac6...` (Source: Unsplash / Placeholder)
*   **Bread Image:** `https://images.unsplash.com/photo-1509440159596-0249088772ff...` (Source: Unsplash / Placeholder)
*   **Milk Image:** `https://images.immediate.co.uk/production/volatile/sites/30/2020/02/Glass-and-bottle-of-milk-fe0997a.jpg` (Source: Immediate Media)
*   **Placeholder Default:** `https://via.placeholder.com/150` (Used as a fallback when database image_url is missing)

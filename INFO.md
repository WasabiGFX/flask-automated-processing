# Project Logs: Greenfield Local Hub

## Version Logs
*   **v0.1.0** (Day 1) - Initial project structure. Flask application setup (`app.py`), basic templating with Jinja2 (`base.html`, `index.html`), and initial CSS styling in `style.css`.
*   **v0.2.0** (Day 2) - Database setup integration. `database.db` initialized with SQLite. Created `users` and `products` tables. Implemented basic user authentication logic for the `/login` route.
*   **v0.3.0** (Day 3) - Product catalogue implementation. Added the `/products` route, `catalogue.html`, dynamic image loading, and the CSS grid layout for the product cards.
*   **v0.4.0** (Day 4) - Producer Dashboard integration. Included robust user Registration/Login loops, migrated the standalone admin wireframe strictly into a dynamic `dashboard.html` layout, and added full database CRUD endpoints (Add/Update/Delete).

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

---

## Asset Logs
Currently utilizing external image links to simulate realistic data. No local image files are hosted in `/static/` to keep the repository lightweight during prototyping.

*   **Apples Image:** `https://images.unsplash.com/photo-1560806887-1e4cd0b6fac6...` (Source: Unsplash / Placeholder)
*   **Bread Image:** `https://images.unsplash.com/photo-1509440159596-0249088772ff...` (Source: Unsplash / Placeholder)
*   **Milk Image:** `https://images.immediate.co.uk/production/volatile/sites/30/2020/02/Glass-and-bottle-of-milk-fe0997a.jpg` (Source: Immediate Media)
*   **Placeholder Default:** `https://via.placeholder.com/150` (Used as a fallback when database image_url is missing)

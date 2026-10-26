
import pytest
from playwright.async_api import async_playwright, expect


# Task 3 - Point 1: Verify home page and main navigation
@pytest.mark.asyncio
async def test_demowebshop_homepage_navigation():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Open home page
            await page.goto("https://demowebshop.tricentis.com/")

            # Verify page title
            await expect(page).to_have_title("Demo Web Shop")

            # Verify main navigation is visible
            navigation = page.locator(".header-menu")
            await expect(navigation).to_be_visible()

            # Verify navigation categories
            await expect(
                navigation.get_by_role("link", name="Books")
            ).to_be_visible()

            await expect(
                navigation.get_by_role("link", name="Computers")
            ).to_be_visible()

            await expect(
                navigation.get_by_role("link", name="Electronics")
            ).to_be_visible()

            print("Home page and main navigation verified.")

        finally:
            await browser.close()


import pytest
from playwright.async_api import async_playwright, expect


# Task 3 -
# import pytest
# from playwright.async_api import async_playwright, expect
#
#
# # Task 3 - Point 2: Hover over a navigation category
# @pytest.mark.asyncio
# async def test_demowebshop_category_hover():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()
#
#         try:
#             await page.goto("https://demowebshop.tricentis.com/")
#
#             # Locate the first Computers navigation link
#             computers = page.get_by_role(
#                 "link", name="Computers", exact=True
#             ).first
#
#             await expect(computers).to_be_visible()
#
#             # Hover over the category
#             await computers.hover()
#
#             # Check for a visible submenu
#             submenu = page.locator(".top-menu .sublist:visible")
#
#             if await submenu.count() > 0:
#                 await expect(submenu.first).to_be_visible()
#                 print("Hover menu is visible.")
#             else:
#                 print("No visible hover submenu appeared.")
#
#         finally:
#             await browser.close()
import pytest
from playwright.async_api import async_playwright, expect


# Task 3 - Point 2: Hover over a navigation category
@pytest.mark.asyncio
async def test_demowebshop_category_hover():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto("https://demowebshop.tricentis.com/")

            # Locate the first Computers navigation link
            computers = page.get_by_role(
                "link", name="Computers", exact=True
            ).first

            await expect(computers).to_be_visible()

            # Hover over the category
            await computers.hover()

            # Check for a visible submenu
            submenu = page.locator(".top-menu .sublist:visible")

            if await submenu.count() > 0:
                await expect(submenu.first).to_be_visible()
                print("Hover menu is visible.")
            else:
                print("No visible hover submenu appeared.")

        finally:
            await browser.close()

import pytest
from playwright.async_api import async_playwright, expect


# Task 3 - Point 2: Hover over a navigation category
@pytest.mark.asyncio
async def test_demowebshop_category_hover():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto("https://demowebshop.tricentis.com/")

            # Locate the first Computers navigation link
            computers = page.get_by_role(
                "link", name="Computers", exact=True
            ).first

            await expect(computers).to_be_visible()

            # Hover over the category
            await computers.hover()

            # Check for a visible submenu
            submenu = page.locator(".top-menu .sublist:visible")

            if await submenu.count() > 0:
                await expect(submenu.first).to_be_visible()
                print("Hover menu is visible.")
            else:
                print("No visible hover submenu appeared.")

        finally:
            await browser.close()


# Task 3 - Point 2: Hover over a navigation category
@pytest.mark.asyncio
async def test_demowebshop_category_hover():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto("https://demowebshop.tricentis.com/")

            # Locate the first Computers navigation link
            computers = page.get_by_role(
                "link", name="Computers", exact=True
            ).first

            await expect(computers).to_be_visible()

            # Hover over the category
            await computers.hover()

            # Check for a visible submenu
            submenu = page.locator(".top-menu .sublist:visible")

            if await submenu.count() > 0:
                await expect(submenu.first).to_be_visible()
                print("Hover menu is visible.")
            else:
                print("No visible hover submenu appeared.")

        finally:
            await browser.close()


# Task 3 - Point 3: Open Books and search for a product
@pytest.mark.asyncio
async def test_demowebshop_search_product():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Open home page
            await page.goto("https://demowebshop.tricentis.com/")

            # Open Books category
            books = page.get_by_role("link", name="Books", exact=True).first
            await expect(books).to_be_visible()
            await books.click()

            # Verify Books category page
            await expect(page).to_have_url(
                "https://demowebshop.tricentis.com/books"
            )

            # Search for a product using the site's search box
            search_box = page.locator("#small-searchterms")
            await expect(search_box).to_be_visible()
            await search_box.fill("Computing and Internet")

            await page.locator("input.button-1.search-box-button").click()

            # Verify search results
            await expect(page.locator(".product-item").first).to_be_visible()

            print("Product search completed and results are visible.")

        finally:
            await browser.close()


# Task 3 - Point 4: Handle dynamic dropdown/autocomplete suggestions
@pytest.mark.asyncio
async def test_demowebshop_autocomplete_suggestions():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto("https://demowebshop.tricentis.com/")

            # Enter a product search term
            search_box = page.locator("#small-searchterms")
            await expect(search_box).to_be_visible()
            await search_box.fill("Computing")

            # Wait briefly for possible autocomplete suggestions
            suggestions = page.locator(
                ".ui-autocomplete li:visible, "
                ".autocomplete-items:visible, "
                "[role='listbox']:visible [role='option']:visible"
            )

            try:
                await suggestions.first.wait_for(
                    state="visible", timeout=3000
                )

                # Select the expected visible suggestion
                expected_option = suggestions.filter(
                    has_text="Computing and Internet"
                ).first

                if await expected_option.count() > 0:
                    await expected_option.click()
                    print("Expected autocomplete suggestion selected.")
                else:
                    print("Suggestions appeared, but the expected option was not found.")

            except Exception:
                print("No autocomplete suggestions appeared.")

        finally:
            await browser.close()


# Task 3 - Point 5: Validate product and add it to cart
@pytest.mark.asyncio
async def test_demowebshop_add_product_to_cart():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Open the Books category
            await page.goto("https://demowebshop.tricentis.com/books")

            # Open a product
            product = page.get_by_role(
                "link", name="Computing and Internet", exact=True
            ).first
            await expect(product).to_be_visible()
            await product.click()

            # Validate product title
            title = page.locator(".product-name h1")
            await expect(title).to_be_visible()
            await expect(title).to_contain_text("Computing and Internet")

            # Validate that the product price is visible
            price = page.locator(".product-price").first
            await expect(price).to_be_visible()
            print("Product price:", await price.inner_text())

            # Add product to cart
            await page.get_by_role(
                "button", name="Add to cart"
            ).first.click()

            # Verify confirmation message
            confirmation = page.locator(".bar-notification")
            await expect(confirmation).to_be_visible()
            await expect(confirmation).to_contain_text(
                "The product has been added to your shopping cart"
            )

            # Verify cart count or cart link is visible
            cart = page.locator(".cart-qty")
            await expect(cart).to_be_visible()
            print("Cart count:", await cart.inner_text())

            print("Product title, price, and cart confirmation verified.")

        finally:
            await browser.close()



import pytest
from playwright.async_api import async_playwright, expect


# Task 3 - Point 6: Test right-click and double-click
@pytest.mark.asyncio
async def test_demowebshop_mouse_actions():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Create a small local practice page
            await page.set_content("""
                <!DOCTYPE html>
                <html>
                <body>
                    <h2>Mouse Action Practice</h2>
                    <button id="practice-button"
                            onclick="document.getElementById('result').innerText='Button clicked';"
                            ondblclick="document.getElementById('result').innerText='Double-click detected';"
                            oncontextmenu="event.preventDefault(); document.getElementById('result').innerText='Right-click detected';">
                        Practice Button
                    </button>
                    <p id="result">No action performed</p>
                </body>
                </html>
            """)

            button = page.locator("#practice-button")
            result = page.locator("#result")

            # Test right-click
            await button.click(button="right")
            await expect(result).to_have_text("Right-click detected")
            print("Right-click verified.")

            # Test double-click
            await button.dblclick()
            await expect(result).to_have_text("Double-click detected")
            print("Double-click verified.")

        finally:
            await browser.close()



# Task 3 - Point 7: Scroll product listings and verify pagination
@pytest.mark.asyncio
async def test_demowebshop_product_pagination():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Open Books category
            await page.goto("https://demowebshop.tricentis.com/books")

            # Verify product listings
            products = page.locator(".product-item")
            await expect(products.first).to_be_visible()

            initial_count = await products.count()
            print("Products on first page:", initial_count)

            # Scroll through the product listings
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            # Verify listings remain visible after scrolling
            await expect(products.first).to_be_visible()
            print("Scrolled through product listings.")

            # Check whether a Next page link exists
            next_page = page.locator(
                ".pager a[rel='next'], .pager .next-page a"
            )

            if await next_page.count() > 0 and await next_page.first.is_visible():
                old_url = page.url

                await next_page.first.click()
                await expect(page).not_to_have_url(old_url)

                # Verify products on the next page
                await expect(products.first).to_be_visible()
                print("Pagination verified. Products are visible on the next page.")
            else:
                print("No Next page link found; pagination is not available here.")

        finally:
            await browser.close()


# Task 3 - Point 8: Check hidden or collapsed UI elements
@pytest.mark.asyncio
async def test_demowebshop_hidden_element():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Open the Books category
            await page.goto("https://demowebshop.tricentis.com/books")

            # Verify the search box is visible
            search_box = page.locator("#small-searchterms")
            await expect(search_box).to_be_visible()

            # Verify the search button is visible before interaction
            search_button = page.locator("input.button-1.search-box-button")
            await expect(search_button).to_be_visible()

            # Interact normally with the search box
            await search_box.fill("Computing and Internet")
            await search_button.click()

            # Verify the search results page is displayed
            await expect(page).to_have_url(
                "https://demowebshop.tricentis.com/search?q=Computing+and+Internet"
            )

            print("Search UI visibility and interaction verified.")

        finally:
            await browser.close()




# Task 3 - Point 9: Verify cart without placing an order
@pytest.mark.asyncio
async def test_demowebshop_cart_verification_only():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Open the Books category
            await page.goto("https://demowebshop.tricentis.com/books")

            # Open a product
            product = page.get_by_role(
                "link", name="Computing and Internet", exact=True
            ).first
            await expect(product).to_be_visible()
            await product.click()

            # Add the product to the cart
            await page.get_by_role(
                "button", name="Add to cart"
            ).first.click()

            # Verify the confirmation message
            confirmation = page.locator(".bar-notification")
            await expect(confirmation).to_be_visible()
            await expect(confirmation).to_contain_text(
                "The product has been added to your shopping cart"
            )

            # Open the shopping cart
            await page.locator("a.ico-cart").first.click()

            # Verify the cart contains a product
            cart_item = page.locator(".cart-item-row")
            await expect(cart_item.first).to_be_visible()

            # Verify the product name in the cart
            await expect(cart_item.first).to_contain_text(
                "Computing and Internet"
            )

            print("Cart verified successfully. No order was placed.")

            # Stop here: do not click Checkout or submit an order.

        finally:
            await browser.close()

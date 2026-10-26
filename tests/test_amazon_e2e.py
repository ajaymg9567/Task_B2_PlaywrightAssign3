import pytest
from playwright.async_api import async_playwright, expect

#page loading
@pytest.mark.asyncio
async def test_amazon_homepage_loads():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.amazon.in/")
        await page.wait_for_timeout(3000)
        print("Page title:", await page.title())
        print("Current URL:", page.url)

        assert "amazon.in" in page.url
        await page.wait_for_timeout(3000)
        await browser.close()


#Hover over
@pytest.mark.asyncio
async def test_amazon_account_hover():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.amazon.in/")

        # Hover over Account & Lists
        account_menu = page.locator("#nav-link-accountList")
        await account_menu.hover()

        # Check whether the hover menu appears
        hover_menu = page.locator("#nav-al-container")

        if await hover_menu.is_visible():
            print("Account hover menu appeared successfully.")
        else:
            print("Account hover menu is not available.")

        await browser.close()

# Point 3: Select a dynamic search suggestion
@pytest.mark.asyncio
async def test_amazon_search_suggestion():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.amazon.in/")

        # Enter a search term
        search_box = page.locator("#twotabsearchtextbox")
        await search_box.fill("C++")

        # Wait for dynamic suggestions
        suggestions = page.locator(".s-suggestion")

        try:
            await suggestions.first.wait_for(state="visible", timeout=10000)

            # Select the first visible suggestion by its text
            suggestion_text = await suggestions.first.inner_text()
            print("Selecting suggestion:", suggestion_text)

            await page.get_by_text(
                suggestion_text, exact=True
            ).first.click()

            print("Search suggestion selected successfully.")

        except Exception:
            print("No search suggestions appeared.")

        await page.wait_for_timeout(2000)
        print("Current URL:", page.url)

        await browser.close()


# Point 4: Search for a book using a unique query
@pytest.mark.asyncio
async def test_amazon_search_book():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.amazon.in/")

        # Enter a unique book search query
        search_box = page.locator("#twotabsearchtextbox")
        await search_box.fill("Python Crash Course Eric Matthes book")

        # Submit the search
        await search_box.press("Enter")

        # Verify that search results appear
        results = page.locator(
            'div[data-component-type="s-search-result"]'
        )

        await results.first.wait_for(state="visible", timeout=15000)

        print("Book search completed successfully.")
        print("Search URL:", page.url)
        print("Number of results:", await results.count())
        await browser.close()


# Point 5: Scroll and verify additional page content
@pytest.mark.asyncio
async def test_amazon_scroll_content():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Open Amazon search results
        await page.goto("https://www.amazon.in/")
        search_box = page.locator("#twotabsearchtextbox")
        await search_box.fill("Python Crash Course Eric Matthes book")
        await search_box.press("Enter")

        results = page.locator(
            'div[data-component-type="s-search-result"]'
        )
        await results.first.wait_for(state="visible", timeout=15000)

        # Record initial page content
        initial_count = await results.count()
        initial_height = await page.locator("body").evaluate(
            "(element) => element.scrollHeight"
        )

        print("Initial result count:", initial_count)
        print("Initial page height:", initial_height)

        # Scroll down in increments
        for step in range(5):
            await page.evaluate(
                "() => window.scrollBy(0, window.innerHeight)"
            )

            await page.wait_for_load_state("domcontentloaded")

            print(f"Completed scroll {step + 1}")

        # Check page content after scrolling
        final_count = await results.count()
        final_height = await page.locator("body").evaluate(
            "(element) => element.scrollHeight"
        )

        print("Final result count:", final_count)
        print("Final page height:", final_height)

        if final_count > initial_count:
            print("Additional search results loaded while scrolling.")
        elif final_height > initial_height:
            print("Additional page content is available after scrolling.")
        else:
            print(
                "No additional content detected. "
                "The page may use standard pagination instead of infinite scroll."
            )

        # Verify that scrolling occurred
        scroll_position = await page.evaluate("() => window.scrollY")
        assert scroll_position > 0, "The page did not scroll."
        await browser.close()

# Point 6: Verify product title and price
@pytest.mark.asyncio
async def test_amazon_product_details():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Step 1: Open Amazon India
            await page.goto(
                "https://www.amazon.in/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Step 2: Search for a book
            search_box = page.locator("#twotabsearchtextbox")
            await search_box.wait_for(
                state="visible",
                timeout=20000
            )

            await search_box.fill("Python Essentials")
            await search_box.press("Enter")

            # Step 3: Wait for search results
            await page.wait_for_url(
                "**/s?k=**",
                timeout=30000
            )
            await page.wait_for_timeout(3000)

            print("Search URL:", page.url)

            # Step 4: Find a product ASIN from the search results
            product_cards = page.locator(
                "div.s-result-item[data-asin]"
            )

            card_count = await product_cards.count()
            print("Product cards found:", card_count)

            product_asin = None

            for i in range(card_count):
                card = product_cards.nth(i)

                asin = await card.get_attribute("data-asin")

                if (
                    asin
                    and len(asin) == 10
                    and await card.is_visible()
                ):
                    product_link = card.locator(
                        'a[href*="/dp/"], a[href*="/gp/product/"]'
                    ).first

                    if await product_link.count() > 0:
                        product_asin = asin
                        break

            assert product_asin, (
                "No valid product ASIN found in search results"
            )

            print("Product ASIN:", product_asin)

            # Step 5: Open the product details page directly
            product_url = (
                f"https://www.amazon.in/dp/{product_asin}"
            )

            await page.goto(
                product_url,
                wait_until="domcontentloaded",
                timeout=60000
            )
            await page.wait_for_timeout(3000)

            print("Product page URL:", page.url)
            print("Page title:", await page.title())

            # Step 6: Verify that the product details page opened
            assert (
                "/dp/" in page.url or "/gp/product/" in page.url
            ), "Product details page did not open"

            # Step 7: Verify the product title
            title = page.locator("#productTitle")

            await title.wait_for(
                state="visible",
                timeout=20000
            )

            product_title = (await title.inner_text()).strip()

            assert product_title, "Product title is empty"

            print("Product title:", product_title)

            # Step 8: Verify the product price
            price = page.locator(
                "#corePriceDisplay_desktop_feature_div "
                ".a-price .a-offscreen, "
                "#corePrice_feature_div .a-price .a-offscreen, "
                ".apexPriceToPay .a-offscreen, "
                "#priceblock_ourprice, "
                "#priceblock_dealprice"
            ).first

            await price.wait_for(
                state="visible",
                timeout=20000
            )

            product_price = (await price.inner_text()).strip()

            assert product_price, "Product price is empty"

            print("Product price:", product_price)

            # Step 9: Save screenshot as evidence
            await page.screenshot(
                path="amazon_product_details.png",
                full_page=True
            )

            print(
                "Screenshot saved: amazon_product_details.png"
            )

        finally:
            # Step 10: Close the browser
            await browser.close()


#7
@pytest.mark.asyncio
async def test_amazon_right_click():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.amazon.in/")

        # Locate the Amazon logo
        logo = page.locator("#nav-logo-sprites")
        await logo.wait_for(state="visible", timeout=20000)

        # Right-click the logo
        await logo.click(button="right")

        print("Right-click completed")

        await browser.close()


# 8
@pytest.mark.asyncio
async def test_double_click():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Create a local practice page
        await page.set_content("""
            <html>
                <body>
                    <p id="label">Double-click this text</p>
                </body>
            </html>
        """)

        # Double-click the text
        label = page.locator("#label")
        await label.dblclick()
        await page.wait_for_timeout(2000)
        print("Double-click completed")

        await browser.close()

#9 hidden element
@pytest.mark.asyncio
async def test_hidden_element_visibility():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Create a practice page with a hidden message
        await page.set_content("""
            <button id="show-button" onclick="
                document.getElementById('message').style.display = 'block'
            ">Show Message</button>

            <p id="message" style="display: none;">
                Hello Playwright
            </p>
        """)

        # Verify the message is initially hidden
        message = page.locator("#message")
        assert not await message.is_visible()
        await page.wait_for_timeout(2000)
        # Click the button to reveal the message
        await page.locator("#show-button").click()

        # Verify the message is now visible
        assert await message.is_visible()
        await page.wait_for_timeout(2000)
        print("Hidden element became visible")

        await browser.close()


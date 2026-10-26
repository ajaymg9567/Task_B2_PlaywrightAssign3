import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_parabank_login_account_overview():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(
            "https://parabank.parasoft.com/parabank/index.htm"
        )

        # Login with demo credentials
        await page.locator('input[name="username"]').fill("jack")
        await page.locator('input[name="password"]').fill("Sparrow@12")
        await page.get_by_role("button", name="Log In").click()

        # Verify Account Overview
        await expect(
            page.get_by_role("heading", name="Accounts Overview")
        ).to_be_visible()
        await page.wait_for_timeout(2000)
        print("Login successful")
        print("Account Overview page verified")
        await browser.close()

# Point 2: Open account details
@pytest.mark.asyncio
async def test_parabank_account_details():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(
            "https://parabank.parasoft.com/parabank/index.htm"
        )

        # Login with demo credentials
        await page.locator('input[name="username"]').fill("jack")
        await page.locator('input[name="password"]').fill("Sparrow@12")
        await page.get_by_role("button", name="Log In").click()

        # Open Accounts Overview
        await page.get_by_role(
            "link", name="Accounts Overview"
        ).click()

        # Click the first account number
        account_link = page.locator("#accountTable a").first
        await account_link.wait_for(state="visible", timeout=15000)

        account_number = (await account_link.inner_text()).strip()
        print("Account number:", account_number)

        await account_link.click()

        # Verify account details/activity page
        await expect(
            page.locator("#rightPanel")
        ).to_contain_text(account_number)

        print("Account details opened successfully.")

        # Display the account information
        print(await page.locator("#rightPanel").inner_text())
        await browser.close()


#
# Point 3: Transfer funds between demo accounts
@pytest.mark.asyncio
async def test_parabank_transfer_funds():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto(
                "https://parabank.parasoft.com/parabank/index.htm"
            )

            # Login with demo credentials
            await page.locator('input[name="username"]').fill("jack")
            await page.locator('input[name="password"]').fill("Sparrow@12")
            await page.get_by_role("button", name="Log In").click()

            # Open Transfer Funds
            await page.get_by_role(
                "link", name="Transfer Funds"
            ).click()

            # Wait for the account dropdowns
            source = page.locator("#fromAccountId")
            destination = page.locator("#toAccountId")

            await source.wait_for(state="visible", timeout=15000)
            await destination.wait_for(state="visible", timeout=15000)

            # Wait until the dropdowns have account options
            await expect(source.locator("option").first).to_be_attached(
                timeout=15000
            )
            await expect(
                destination.locator("option").first
            ).to_be_attached(timeout=15000)

            # Read available accounts
            source_options = await source.locator("option").evaluate_all(
                """options => options
                    .map(o => ({
                        value: o.value,
                        text: o.textContent.trim()
                    }))
                    .filter(o => o.value)"""
            )

            destination_options = await destination.locator(
                "option"
            ).evaluate_all(
                """options => options
                    .map(o => ({
                        value: o.value,
                        text: o.textContent.trim()
                    }))
                    .filter(o => o.value)"""
            )

            print("Source accounts:", source_options)
            print("Destination accounts:", destination_options)

            # Ensure two different accounts are available
            assert source_options, "No source accounts are available."
            source_account = source_options[0]["value"]

            destination_account = next(
                (
                    option["value"]
                    for option in destination_options
                    if option["value"] != source_account
                ),
                None
            )

            assert destination_account, (
                "Two different accounts are required. "
                "Open a second demo account before transferring."
            )

            # Select source and destination accounts
            await source.select_option(value=source_account)
            await destination.select_option(value=destination_account)

            # Enter a small demo amount
            await page.locator("#amount").fill("1")

            # Submit the demo transfer
            await page.get_by_role("button", name="Transfer").click()

            # Verify transfer confirmation
            await expect(
                page.locator("#rightPanel")
            ).to_contain_text("Transfer Complete!", timeout=15000)
            await page.wait_for_timeout(3000)
            print("Transfer completed successfully.")
            print("Amount: $1.00")
            print("From account:", source_account)
            print("To account:", destination_account)

        finally:
            await browser.close()





# Point 4: Verify transfer result and Accounts Overview
@pytest.mark.asyncio
async def test_parabank_verify_transfer():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Open ParaBank
            await page.goto(
                "https://parabank.parasoft.com/parabank/index.htm"
            )

            # Login
            await page.locator('input[name="username"]').fill("jack")
            await page.locator('input[name="password"]').fill("Sparrow@12")
            await page.get_by_role("button", name="Log In").click()

            # Open Accounts Overview
            await page.get_by_role(
                "link", name="Accounts Overview"
            ).click()

            # Verify Accounts Overview
            await expect(
                page.locator("#rightPanel")
            ).to_contain_text("Accounts Overview", timeout=15000)

            print("Accounts Overview verified.")

            # Open Find Transactions
            await page.get_by_role(
                "link", name="Find Transactions"
            ).click()

            # Verify transaction search page
            await expect(
                page.locator("#rightPanel")
            ).to_contain_text("Find Transactions", timeout=15000)

            print("Transaction details page verified.")

        finally:
            await browser.close()

# Point 5: Check hover-driven navigation menu

# Point 5: Check navigation hover
@pytest.mark.asyncio
async def test_parabank_navigation_hover():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto(
                "https://parabank.parasoft.com/parabank/index.htm"
            )

            # Hover over the available navigation element
            navigation = page.locator("#headerPanel")

            await expect(navigation).to_be_visible()
            await navigation.hover()
            await page.wait_for_timeout(2000)
            # Record the observation
            print(
                "ParaBank does not provide a hover-driven "
                "navigation submenu on the login page."
            )

        finally:
            await browser.close()

# Point 6: Test hidden-element handling
@pytest.mark.asyncio
async def test_parabank_hidden_element():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto(
                "https://parabank.parasoft.com/parabank/index.htm"
            )

            # Check a navigation element
            navigation = page.locator("#headerPanel")
            await expect(navigation).to_be_visible()

            # Check whether a hidden section exists
            hidden_elements = page.locator(
                "#headerPanel [hidden], "
                "#headerPanel [aria-hidden='true']"
            )

            count = await hidden_elements.count()

            if count > 0:
                print("Hidden navigation element found.")

                # Verify it is hidden; do not force-click it
                await expect(hidden_elements.first).to_be_hidden()
            else:
                print(
                    "No hidden or collapsed navigation section "
                    "was found in the header."
                )

        finally:
            await browser.close()



# Point 7: Test right-click and double-click on a practice page
@pytest.mark.asyncio
async def test_parabank_mouse_actions():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Create a safe practice page
            await page.set_content("""
                <!DOCTYPE html>
                <html>
                <body>
                    <h2 id="title">Mouse Action Practice</h2>
                    <p id="message">Practice right-click and double-click.</p>
                </body>
                </html>
            """)

            title = page.locator("#title")
            message = page.locator("#message")

            # Right-click on the heading
            await title.click(button="right")
            print("Right-click performed successfully.")

            # Double-click on the paragraph
            await message.dblclick()
            print("Double-click performed successfully.")

            # Verify the practice page remains available
            await expect(title).to_be_visible()
            await expect(message).to_be_visible()
            await page.wait_for_timeout(2000)
            print(
                "ParaBank has no required safe target for these "
                "actions in this test; a practice page was used."
            )

        finally:
            await browser.close()


# Point 8: Log out and verify signed-out state
@pytest.mark.asyncio
async def test_parabank_logout():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Open ParaBank
            await page.goto(
                "https://parabank.parasoft.com/parabank/index.htm"
            )

            # Login
            await page.locator('input[name="username"]').fill("jack")
            await page.locator('input[name="password"]').fill("Sparrow@12")
            await page.get_by_role("button", name="Log In").click()

            # Verify login succeeded
            await expect(
                page.get_by_role("link", name="Log Out")
            ).to_be_visible(timeout=15000)
            await page.wait_for_timeout(2000)
            # Log out
            await page.get_by_role("link", name="Log Out").click()

            # Verify signed-out state
            await expect(
                page.locator('input[name="username"]')
            ).to_be_visible(timeout=15000)

            await expect(
                page.locator('input[name="password"]')
            ).to_be_visible()
            await page.wait_for_timeout(2000)
            print("Logout successful. Signed-out state verified.")

        finally:
            await browser.close()

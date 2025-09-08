import os
import pytest
from qtest_page import QTestPage

@pytest.mark.qtest
@pytest.mark.TC_QTEST_0001
def test_qtest_login_and_nav_to_defects(browser):
    """
    Scope: Keep it simple for initial bring-up.
    Steps:
      1. Open qTest login page
      2. Login (QTEST_USERNAME / QTEST_PASSWORD from env)
      3. Navigate to the project 130448 portal
      4. Navigate to 'Defects' section
    Assertions are minimal & heuristic; refine with real DOM once available.
    """
    qtest = QTestPage(browser)

    # Step 1: open
    qtest.open("https://sunlife.qtestnet.com")
    # Step 2: login with env-based credentials
    qtest.login()

    assert qtest.is_logged_in(), "Login did not appear to succeed—check credentials and selectors."

    # Step 3: go to project portal
    qtest.goto_project("130448")

    # Step 4: go to defects
    qtest.goto_defects()

    # Soft assertion: defects tab visible (nav is present)
    assert qtest.defects_visible(), "Defects nav not visible—adjust locator or ensure project permissions."

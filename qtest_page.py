from base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class QTestPage(BasePage):
    """
    Minimal qTest workflow using the existing framework style:
    1) Login
    2) Navigate to a project's Defects section
    Notes:
      - Reads credentials from env: QTEST_USERNAME, QTEST_PASSWORD
      - Uses explicit waits only (no sleep)
      - Keep selectors simple; adjust XPaths if your qTest UI differs
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver, 20)

        self.locators = {
            # Login page
            "username": (By.NAME, "username"),
            "password": (By.NAME, "password"),
            "login_btn": (By.XPATH, "//button[.//span[normalize-space()='Log in'] or normalize-space()='Login' or @type='submit']"),

            # Project portal (generic selectors; adjust to your qTest skin)
            "projects_menu": (By.XPATH, "//a[contains(@href,'/portal/project') or .//span[contains(.,'Projects')]]"),
            # Left nav "Defects" tab inside a project:
            "defects_nav": (By.XPATH, "//a[.//span[normalize-space()='Defects'] or normalize-space()='Defects']"),
        }

    def open(self, url: str):
        self.driver.get(url)

    def login(self, username: str = None, password: str = None):
        username = username or os.getenv("QTEST_USERNAME", "")
        password = password or os.getenv("QTEST_PASSWORD", "")
        # Fill username and password
        self.wait.until(EC.presence_of_element_located(self.locators["username"])).clear()
        self.find_element(*self.locators["username"]).send_keys(username)
        self.wait.until(EC.presence_of_element_located(self.locators["password"])).clear()
        self.find_element(*self.locators["password"]).send_keys(password)
        # Click login
        self.find_element(*self.locators["login_btn"]).click()

    def goto_project(self, project_id: str = "130448"):
        """
        Navigate directly to a project's portal using its ID.
        """
        base = "https://sunlife.qtestnet.com"
        self.driver.get(f"{base}/p/{project_id}/portal/project#tab=testplan")

    def goto_defects(self):
        """
        Assumes we're already inside a project portal. Click the 'Defects' section.
        """
        self.wait.until(EC.presence_of_element_located(self.locators["defects_nav"])).click()
        # Wait until the Defects grid/table appears (very generic condition)
        self.wait.until(lambda d: "defect" in d.current_url.lower() or "defects" in d.page_source.lower())

    # Verifications
    def is_logged_in(self) -> bool:
        # Heuristic: after login, URL should contain '/portal' or projects menu appears
        try:
            self.wait.until(EC.any_of(
                EC.url_contains("/portal"),
                EC.presence_of_element_located(self.locators["projects_menu"])
            ))
            return True
        except Exception:
            return False

    def defects_visible(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self.locators["defects_nav"]))
            return True
        except Exception:
            return False

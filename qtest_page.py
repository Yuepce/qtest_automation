from base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QTestPage(BasePage):
    """
    qTest minimal workflow (hardcoded credentials for quick bring-up):
      1) Login
      2) Navigate to a project's portal
      3) Navigate to Defects
    NOTE: Replace the hardcoded credentials below before committing to any repo.
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver, 20)

        self.locators = {
            # Login page
            "username": (By.NAME, "username"),
            "password": (By.NAME, "password"),
            "login_btn": (By.XPATH, "//button[.//span[normalize-space()='Log in'] or normalize-space()='Login' or @type='submit']"),
            # In-portal hints
            "projects_menu": (By.XPATH, "//a[contains(@href,'/portal/project') or .//span[contains(.,'Projects')]]"),
            # Left nav 'Defects'
            "defects_nav": (By.XPATH, "//a[.//span[normalize-space()='Defects'] or normalize-space()='Defects']"),
        }

    def open(self, url: str):
        self.driver.get(url)

    def login(self, username: str = None, password: str = None):
        """
        Hardcoded quick test credentials (DO NOT commit real credentials).
        Pass username/password explicitly to override if needed.
        """
        username = username or "your.name@sunlife.com"
        password = password or "your_password"

        self.wait.until(EC.presence_of_element_located(self.locators["username"])).clear()
        self.find_element(*self.locators["username"]).send_keys(username)
        self.wait.until(EC.presence_of_element_located(self.locators["password"])).clear()
        self.find_element(*self.locators["password"]).send_keys(password)
        self.find_element(*self.locators["login_btn"]).click()

    def goto_project(self, project_id: str = "130448"):
        base = "https://sunlife.qtestnet.com"
        self.driver.get(f"{base}/p/{project_id}/portal/project#tab=testplan")

    def goto_defects(self):
        self.wait.until(EC.presence_of_element_located(self.locators["defects_nav"])).click()
        # generic readiness check
        self.wait.until(lambda d: "defect" in d.current_url.lower() or "defects" in d.page_source.lower())

    def is_logged_in(self) -> bool:
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

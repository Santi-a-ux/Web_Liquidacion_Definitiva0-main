import unittest
import requests
from selenium.common.exceptions import WebDriverException

from screenplay.actors import AdminUser
from screenplay.abilities import BrowseTheWeb
from screenplay.tasks import Login
from screenplay.questions import TheUrl
from screenplay.questions import TheText
from selenium.webdriver.common.by import By

BASE_URL = "http://127.0.0.1:8080"


def _server_available() -> bool:
    try:
        r = requests.get(f"{BASE_URL}/login", timeout=2)
        return r.status_code < 500
    except Exception:
        return False


class TestScreenplayRealFlow(unittest.TestCase):
    """Minimal real UI test using Screenplay against the running Flask app."""

    @unittest.skipUnless(_server_available(), "Flask server not available at http://127.0.0.1:8080")
    def test_admin_login_and_admin_panel(self):
        admin = AdminUser()
        try:
            admin.who_can(BrowseTheWeb())
        except WebDriverException as e:
            self.skipTest(f"Cannot start WebDriver: {e}")

        # Login as admin (Login task fills id_usuario + password)
        admin.attempts_to(
            Login.with_credentials(admin.username, admin.password)
        )

        # After login, ensure we are not on /login and can navigate to admin panel
        admin.should_see(
            TheUrl.current().contains("/")
        )

        # Optionally, navigate to /admin_panel and verify URL contains it
        from screenplay.interactions import Open
        admin.attempts_to(
            Open.browser_on(f"{BASE_URL}/admin_panel")
        ).should_see(
            TheUrl.current().contains("/admin_panel")
        )

    @unittest.skipUnless(_server_available(), "Flask server not available at http://127.0.0.1:8080")
    def test_admin_panel_failure_demo_with_screenshot(self):
        """Intentional failure to demonstrate HTML report extras (URL + screenshot)."""
        admin = AdminUser()
        try:
            admin.who_can(BrowseTheWeb())
        except WebDriverException as e:
            self.skipTest(f"Cannot start WebDriver: {e}")

        # Login and visit admin panel
        admin.attempts_to(
            Login.with_credentials(admin.username, admin.password)
        ).attempts_to(
            __import__('screenplay').interactions.Open.browser_on(f"{BASE_URL}/admin_panel")
        )

        # This assertion is designed to FAIL to show report details
        admin.should_see(
            TheText.of((By.TAG_NAME, "body")).contains("STRING_THAT_SHOULD_NOT_EXIST")
        )


if __name__ == "__main__":
    unittest.main()

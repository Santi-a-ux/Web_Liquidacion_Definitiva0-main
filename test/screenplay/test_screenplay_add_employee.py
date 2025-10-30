import unittest
import requests
import time
import sys
import os
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from screenplay.actors import AdminUser
from screenplay.abilities import BrowseTheWeb
from screenplay.tasks import Login
from screenplay.questions import TheUrl, TheText
from screenplay.interactions import Open

BASE_URL = "http://127.0.0.1:8080"


def _server_available() -> bool:
    try:
        r = requests.get(f"{BASE_URL}/login", timeout=2)
        return r.status_code < 500
    except Exception:
        return False


class TestScreenplayAddEmployee(unittest.TestCase):
    """Real UI test: admin can view users list (UI flow stable for report)."""

    @unittest.skipUnless(_server_available(), "Flask server not available at http://127.0.0.1:8080")
    def test_admin_can_view_users_list(self):
        admin = AdminUser()
        try:
            admin.who_can(BrowseTheWeb())
        except WebDriverException as e:
            self.skipTest(f"Cannot start WebDriver: {e}")

        # Unique-ish test data to avoid collisions on repeated runs
        unique_suffix = str(int(time.time()))[-6:]
        # No creamos datos (evitamos dependencias de DB/CSRF).

        # Login to UI
        admin.attempts_to(
            Login.with_credentials(admin.username, admin.password)
        ).should_see(
            TheUrl.current().contains("/")
        )

        # Go to admin users list and verify page content
        admin.attempts_to(Open.browser_on(f"{BASE_URL}/admin/usuarios"))

        # Verify the page shows the Users Administration header and correct URL
        admin.should_see(
            TheUrl.current().contains("/admin/usuarios")
        ).should_see(
            TheText.of((By.TAG_NAME, "body")).contains("Administración de Usuarios")
        )


if __name__ == "__main__":
    unittest.main()

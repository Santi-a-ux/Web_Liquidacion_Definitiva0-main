# Pytest collection config for legacy Selenium Python tests in this folder.
# We ignore the converted Selenium WebDriver tests because the project now
# uses Selenium IDE (.side) for this area.

collect_ignore = [
    "test_selenium_login.py",
]

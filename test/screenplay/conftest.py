import os
import platform
import sys
from datetime import datetime

import pytest

try:
    from py.xml import html  # type: ignore
except Exception:
    html = None  # pytest-html v4 may still accept py.xml; guard just in case

# Ensure we can import abilities to access the last Selenium driver
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(os.path.dirname(PROJECT_ROOT), 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Best-effort import; tests still pass if Selenium not used
from typing import Any
try:
    from screenplay.abilities import get_last_driver as _get_last_driver  # type: ignore

    def get_last_driver() -> Any:  # shim for type-checkers
        return _get_last_driver()
except Exception:  # pragma: no cover
    def get_last_driver() -> Any:
        return None


def pytest_configure(config):
    # Report title
    config._metadata = getattr(config, "_metadata", {})  # type: ignore[attr-defined]
    # Minimal environment metadata for the report
    config._metadata.update({
        "Base URL": "http://127.0.0.1:8080",
        "Runner": "pytest + pytest-html",
        "OS": platform.platform(),
        "Python": sys.version.split(" ")[0],
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })


def pytest_html_report_title(report):  # type: ignore[override]
    report.title = "Screenplay Test Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Let pytest process the report first
    outcome = yield
    report = outcome.get_result()

    # Only add extras for the actual test call phase
    if report.when != 'call':
        return

    # Initialize extras list
    report.extra = getattr(report, 'extra', [])

    # Attach current URL and a screenshot on failure, when a driver is available
    try:
        driver = get_last_driver()
        if driver is not None:
            current_url = None
            try:
                current_url = driver.current_url
            except Exception:
                current_url = None

            from pytest_html import extras  # type: ignore

            if current_url:
                report.extra.append(extras.url(current_url, name="Current URL"))

            # Take a screenshot for failures
            if report.failed:
                try:
                    png_b64 = driver.get_screenshot_as_base64()
                    report.extra.append(extras.image(png_b64, mime_type='image/png', extension='png'))
                except Exception:
                    pass
    except Exception:
        # Never break the test run due to reporting
        pass


def pytest_html_results_summary(prefix, summary, postfix):  # type: ignore[override]
    """Inject quick links and embed artifacts content inside the HTML report."""
    artifacts = [
        ("JUnit XML", "reports/screenplay-junit.xml"),
        ("Log (txt)", "reports/screenplay-run.txt"),
        ("Lista de tests", "reports/screenplay-tests.txt"),
    ]

    def _read(path: str, max_chars: int | None = None) -> str:
        try:
            here = os.path.dirname(__file__)
            full = os.path.join(here, path)
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if max_chars and len(content) > max_chars:
                return content[:max_chars] + "\n... [truncated] ...\n"
            return content
        except Exception:
            return "(no disponible)"

    try:
        if html is not None:
            # Links
            links = [html.li(html.a(name, href=href, target="_blank")) for name, href in artifacts]
            prefix.extend([html.h2("Reportes adicionales (Screenplay)"), html.ul(links)])

            # Embedded content: log, test list, junit summary
            run_txt = _read("reports/screenplay-run.txt", max_chars=12000)
            tests_txt = _read("reports/screenplay-tests.txt", max_chars=8000)
            junit_xml = _read("reports/screenplay-junit.xml", max_chars=4000)

            prefix.extend([
                html.details(
                    html.summary(html.strong("Log de ejecución (txt)")),
                    html.pre(run_txt)
                ),
                html.details(
                    html.summary(html.strong("Lista de tests")),
                    html.pre(tests_txt)
                ),
                html.details(
                    html.summary(html.strong("JUnit XML (resumen)")),
                    html.pre(junit_xml)
                ),
            ])
    except Exception:
        # If py.xml is unavailable or incompatible, skip injection gracefully
        pass

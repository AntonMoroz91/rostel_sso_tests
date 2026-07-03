import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import BASE_URL, IMPLICIT_WAIT
import allure


def pytest_addoption(parser):
    """Добавляем возможность запускать тесты в headless-режиме"""
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run Chrome in headless mode")


@pytest.fixture(scope="function")
def driver(request):
    """Фикстура для Chrome с обходом защиты + поддержка headless"""

    chrome_options = Options()

    # ---- ТВОИ СТАРЫЕ НАСТРОЙКИ (всё сохранено) ----
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-gpu")

    # ---- НОВОЕ: поддержка headless (для GitHub Actions) ----
    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")

    # Создаём драйвер
    driver = webdriver.Chrome(options=chrome_options)

    # Скрываем navigator.webdriver через CDP (твоя защита)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ru-RU', 'ru']
            });
        """
    })

    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.get(BASE_URL)

    yield driver

    driver.quit()


# ---- НОВОЕ: Allure-отчёт со скриншотами при падении ----
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            allure.attach(driver.get_screenshot_as_png(),
                          name="screenshot",
                          attachment_type=allure.attachment_type.PNG)
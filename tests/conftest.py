import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import BASE_URL, IMPLICIT_WAIT


@pytest.fixture(scope="function")
def driver():
    """Фикстура для Chrome с обходом защиты"""

    chrome_options = Options()

    # Базовые настройки
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")

    # Обход SSL-ошибок
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-insecure-localhost")

    # Скрываем автоматизацию
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Реалистичный User-Agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Отключаем WebDriver в JS
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-gpu")

    # Создаём драйвер
    driver = webdriver.Chrome(options=chrome_options)

    # Скрываем navigator.webdriver через CDP
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
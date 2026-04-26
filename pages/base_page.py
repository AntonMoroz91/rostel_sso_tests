from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """
    Базовый класс для всех страниц.
    Содержит общие методы для работы с элементами.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # Явное ожидание до 15 секунд

    def find_element(self, locator):
        """
        Поиск элемента с ожиданием его появления в DOM.
        Возвращает WebElement.
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Поиск всех элементов по локатору. Возвращает список."""
        return self.driver.find_elements(*locator)

    def click(self, locator):
        """Клик по элементу после его появления."""
        element = self.find_element(locator)
        element.click()

    def input_text(self, locator, text):
        """
        Очищает поле и вводит текст.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Получение текста элемента."""
        return self.find_element(locator).text

    def is_element_present(self, locator, timeout=5):
        """
        Проверка наличия элемента на странице.
        Возвращает True, если элемент найден за timeout секунд.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        """Возвращает текущий URL страницы."""
        return self.driver.current_url

    def scroll_to_element(self, locator):
        """Скроллит страницу до элемента."""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
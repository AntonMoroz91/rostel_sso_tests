from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AuthPage(BasePage):
    """
    Page Object для страницы авторизации Ростелеком.
    Содержит локаторы и методы для взаимодействия с формой входа.
    """

    # ----- ЛОКАТОРЫ -----

    # Табы выбора способа аутентификации
    TAB_PHONE = (
    By.XPATH, "//div[@data-tab='phone'] | //button[contains(text(), 'Номер')] | //span[contains(text(), 'Номер')]")
    TAB_EMAIL = (
    By.XPATH, "//div[@data-tab='email'] | //button[contains(text(), 'Почта')] | //span[contains(text(), 'Почта')]")
    TAB_LOGIN = (
    By.XPATH, "//div[@data-tab='login'] | //button[contains(text(), 'Логин')] | //span[contains(text(), 'Логин')]")
    TAB_LS = (By.XPATH,
              "//div[@data-tab='ls'] | //button[contains(text(), 'Лицевой счет')] | //span[contains(text(), 'Лицевой')]")

    # Поля ввода
    INPUT_USERNAME = (By.ID, "username")
    INPUT_PASSWORD = (By.ID, "password")

    # Кнопки
    BUTTON_LOGIN = (By.ID, "kc-login")
    BUTTON_LOGOUT = (By.ID, "logout-btn")

    # Ссылки
    LINK_FORGOT_PASSWORD = (By.ID, "forgot_password")
    LINK_REGISTER = (By.ID, "kc-register")

    # Сообщение об ошибке
    ERROR_MESSAGE = (By.ID, "form-error-message")
    ERROR_MESSAGE_ALT = (By.XPATH, "//span[contains(@class, 'rt-input-container__meta--error')]")

    # Заголовок страницы (для проверки загрузки)
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Авторизация')]")

    # ----- МЕТОДЫ -----

    def open(self, url):
        """Открывает страницу по указанному URL."""
        self.driver.get(url)

    def click_phone_tab(self):
        """Клик по табу 'Номер'."""
        self.click(self.TAB_PHONE)

    def click_email_tab(self):
        """Клик по табу 'Почта'."""
        self.click(self.TAB_EMAIL)

    def click_login_tab(self):
        """Клик по табу 'Логин'."""
        self.click(self.TAB_LOGIN)

    def click_ls_tab(self):
        """Клик по табу 'Лицевой счет'."""
        self.click(self.TAB_LS)

    def enter_username(self, username):
        """
        Ввод логина/телефона/почты/ЛС.
        :param username: строка для ввода
        """
        self.input_text(self.INPUT_USERNAME, username)

    def enter_password(self, password):
        """
        Ввод пароля.
        :param password: строка пароля
        """
        self.input_text(self.INPUT_PASSWORD, password)

    def click_login(self):
        """Клик по кнопке 'Войти'."""
        self.click(self.BUTTON_LOGIN)

    def login(self, username, password):
        """
        Комплексный метод для авторизации.
        :param username: логин/телефон/почта
        :param password: пароль
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def click_register(self):
        """Клик по ссылке 'Зарегистрироваться'."""
        self.click(self.LINK_REGISTER)

    def click_forgot_password(self):
        """Клик по ссылке 'Забыл пароль'."""
        self.click(self.LINK_FORGOT_PASSWORD)

    def get_error_message(self):
        """
        Получение текста ошибки авторизации.
        Возвращает пустую строку, если ошибки нет.
        """
        if self.is_element_present(self.ERROR_MESSAGE, timeout=3):
            return self.get_text(self.ERROR_MESSAGE)
        elif self.is_element_present(self.ERROR_MESSAGE_ALT, timeout=3):
            return self.get_text(self.ERROR_MESSAGE_ALT)
        return ""

    def is_logout_button_present(self):
        """
        Проверка, что пользователь авторизован (есть кнопка выхода).
        Используется после успешного входа.
        """
        return self.is_element_present(self.BUTTON_LOGOUT, timeout=10)

    def is_auth_page_loaded(self):
        """Проверка загрузки страницы авторизации."""
        return self.is_element_present(self.INPUT_USERNAME, timeout=10)
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RecoveryPage(BasePage):
    """
    Page Object для страницы восстановления пароля Ростелеком.
    """

    # ----- ЛОКАТОРЫ -----

    # Поля ввода
    INPUT_USERNAME = (By.ID, "username")  # Поле для телефона/почты/логина/ЛС
    INPUT_CAPTCHA = (By.ID, "captcha")

    # Кнопки
    BUTTON_NEXT = (By.ID, "reset")
    BUTTON_BACK = (By.ID, "reset-back")
    BUTTON_CONTINUE = (By.XPATH, "//button[contains(text(), 'Продолжить')]")

    # Табы выбора способа восстановления
    TAB_PHONE = (By.XPATH, "//span[contains(text(), 'Номер')]")
    TAB_EMAIL = (By.XPATH, "//span[contains(text(), 'Почта')]")
    TAB_LOGIN = (By.XPATH, "//span[contains(text(), 'Логин')]")
    TAB_LS = (By.XPATH, "//span[contains(text(), 'Лицевой счет')]")

    # Форма ввода кода (6 полей)
    CODE_INPUT_1 = (By.ID, "rt-code-0")
    CODE_INPUT_2 = (By.ID, "rt-code-1")
    CODE_INPUT_3 = (By.ID, "rt-code-2")
    CODE_INPUT_4 = (By.ID, "rt-code-3")
    CODE_INPUT_5 = (By.ID, "rt-code-4")
    CODE_INPUT_6 = (By.ID, "rt-code-5")

    # Сообщения об ошибках
    ERROR_MESSAGE = (By.ID, "form-error-message")
    ERROR_CAPTCHA = (By.XPATH, "//span[contains(text(), 'Неверный код')]")

    # Форма выбора способа восстановления (SMS / Email)
    OPTION_SMS = (By.XPATH, "//span[contains(text(), 'По SMS на номер')]")
    OPTION_EMAIL = (By.XPATH, "//span[contains(text(), 'По ссылке на почту')]")

    # ----- МЕТОДЫ -----

    def enter_username(self, username):
        """Ввод телефона/почты/логина/ЛС."""
        self.input_text(self.INPUT_USERNAME, username)

    def enter_captcha(self, captcha_text):
        """Ввод капчи."""
        if self.is_element_present(self.INPUT_CAPTCHA, timeout=3):
            self.input_text(self.INPUT_CAPTCHA, captcha_text)

    def click_next(self):
        """Клик по кнопке 'Далее'."""
        self.click(self.BUTTON_NEXT)

    def click_back(self):
        """Клик по кнопке 'Вернуться'."""
        self.click(self.BUTTON_BACK)

    def click_continue(self):
        """Клик по кнопке 'Продолжить'."""
        self.click(self.BUTTON_CONTINUE)

    def click_sms_option(self):
        """Выбор восстановления по SMS."""
        if self.is_element_present(self.OPTION_SMS, timeout=3):
            self.click(self.OPTION_SMS)

    def click_email_option(self):
        """Выбор восстановления по Email."""
        if self.is_element_present(self.OPTION_EMAIL, timeout=3):
            self.click(self.OPTION_EMAIL)

    def get_error_message(self):
        """Получение текста ошибки."""
        if self.is_element_present(self.ERROR_MESSAGE, timeout=2):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_code_form_displayed(self):
        """Проверка, что открылась форма ввода кода."""
        return self.is_element_present(self.CODE_INPUT_1, timeout=10)

    def is_recovery_options_displayed(self):
        """Проверка, что отображаются варианты восстановления (SMS/Email)."""
        return (self.is_element_present(self.OPTION_SMS, timeout=3) or
                self.is_element_present(self.OPTION_EMAIL, timeout=3))
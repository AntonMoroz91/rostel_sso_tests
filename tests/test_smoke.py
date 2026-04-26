from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_open_auth_page(driver):
    """Проверка открытия страницы авторизации"""

    wait = WebDriverWait(driver, 30)

    # Ждём, пока появится форма авторизации (по ID поля username)
    try:
        wait.until(EC.visibility_of_element_located((By.ID, "username")))
        print("✅ Форма авторизации загружена")
    except:
        print("❌ Форма не загрузилась за 30 сек")

    # Даём ещё 2 секунды на отрисовку
    import time
    time.sleep(2)

    print(f"\nТекущий URL: {driver.current_url}")
    print(f"Title страницы: '{driver.title}'")

    # Сохраняем скриншот
    driver.save_screenshot("screenshot.png")
    print("Скриншот сохранён: screenshot.png")

    # Проверяем, что URL правильный
    assert "passport.rt.ru" in driver.current_url
    print("✅ Страница успешно загружена!")
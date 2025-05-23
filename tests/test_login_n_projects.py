import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import LOGIN_URL, PROJECTS_URL, VALID_USERNAME, VALID_PASSWORD, INVALID_USERNAME, INVALID_PASSWORD


def test_login_valid_creds(login_page):
    '''
    Тест проверки успешного входа с валидными учетными данными.

    Шаги:
    - Выполняется HTTP-запрос GET к странице логина для проверки доступности (код 200).
    - Производится попытка входа с валидным логином и паролем.
    - Ожидается смена URL на страницу проектов.
    - Проверяется, что текущий URL совпадает с ожидаемым PROJECTS_URL.

    :param login_page: фикстура страницы логина.
    '''
    response = requests.get(LOGIN_URL)

    assert response.status_code == 200, f"Страница недоступна, код: {response.status_code}"

    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    WebDriverWait(login_page.driver, 10).until(
        EC.url_to_be(PROJECTS_URL),
        message=f"Не дождался смены URL на {PROJECTS_URL}"
    )
    current_url = login_page.driver.current_url
    expected_url = PROJECTS_URL

    assert current_url == expected_url, f"Ожидаемый URL: {expected_url}, реальный URL: {current_url}"


def test_login_invalid_creds(login_page, driver):
    '''
    Тест проверки поведения при входе с некорректными учетными данными.

    Шаги:
    - Пытаемся войти с неправильным логином и паролем.
    - Проверяем наличие сообщения об ошибке "Неверный логин/пароль".
    - Проверяем, что URL остался на странице логина (вход не выполнен).

    :param login_page: фикстура страницы логина.
    :param driver: фикстура WebDriver.
    '''
    login_page.login(INVALID_USERNAME, INVALID_PASSWORD)
    error_message_locator = (By.XPATH, "//div[text()='Неверный логин/пароль. Проверьте данные']")

    assert login_page.is_element(error_message_locator), "Нет сообщения об ошибке при попытке входа с некорректными данными"
    assert driver.current_url == LOGIN_URL, "Возможен вход с некорректными данными"


def test_select_project_type(driver, logged_in_project_page):
    '''
    Тест выбора типа проекта из выпадающего списка на странице проектов.

    Шаги:
    - Ожидаем кликабельность дропдауна выбора типа проекта и кликаем по нему.
    - Ожидаем кликабельность варианта "Внутренний" (или "Internal") и выбираем его.
    - Проверяем, что выбранный вариант отображается корректно.

    :param driver: фикстура WebDriver.
    :param logged_in_project_page: фикстура страницы проектов с авторизацией.
    '''
    PROJECT_TYPE_DROPDOWN_LOCATOR = (By.CSS_SELECTOR, ".Select-control")
    OPTION_INTERNAL_LOCATOR = (By.XPATH, "//div[@class='Select-menu']//div[normalize-space()='Внутренний' or normalize-space()='Internal']")
    SELECTED_VALUE_LOCATOR = (By.CSS_SELECTOR, ".Select-value-label")

    dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(PROJECT_TYPE_DROPDOWN_LOCATOR))
    dropdown.click()

    option = WebDriverWait(logged_in_project_page.driver, 10).until(EC.element_to_be_clickable(OPTION_INTERNAL_LOCATOR))
    option.click()

    selected_value = WebDriverWait(logged_in_project_page.driver, 10).until(EC.visibility_of_element_located(SELECTED_VALUE_LOCATOR))

    assert selected_value.text.strip() in ["Внутренний", "Internal"], f"Ожидаемый тип проекта: 'Внутренний' / 'Internal', реальный '{selected_value.text}'"


def test_input_project_name(logged_in_project_page, driver):
    '''
    Тест ввода названия проекта в соответствующее поле на странице проектов.

    Шаги:
    - Ожидаем видимость поля ввода названия проекта.
    - Вводим текст "Привет".
    - Ожидаем, что введённый текст появится в поле.
    - Проверяем, что значение в поле совпадает с введённым.

    :param logged_in_project_page: фикстура страницы проектов с авторизацией.
    :param driver: фикстура WebDriver.
    '''
    PROJECT_NAME_INPUT_LOCATOR = (By.XPATH, "//input[normalize-space(@placeholder)='Введите название проекта' or normalize-space(@placeholder)='Enter the project name']")

    input_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(PROJECT_NAME_INPUT_LOCATOR))

    input_element.send_keys("Привет")

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_value(PROJECT_NAME_INPUT_LOCATOR, "Привет"),
        message="Не дождался появления названия проекта 'Привет' в поле ввода"
    )

    entered_value = input_element.get_attribute("value")
    assert entered_value == "Привет", f"Вместо ожидаемого значения было получено '{entered_value}'"

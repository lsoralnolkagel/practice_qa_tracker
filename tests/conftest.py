import pytest
from selenium import webdriver

from config import VALID_USERNAME, VALID_PASSWORD, HEADLESS
from classes.page_classes import LoginPage, ProjectsPage


def __create_chrome_options():
    '''
    Создаёт и настраивает опции для запуска браузера Chrome.

    Если в конфигурации установлен режим HEADLESS (без интерфейса),
    добавляет соответствующий аргумент для запуска браузера в фоновом режиме.

    :return: объект ChromeOptions с заданными параметрами.
    '''
    options = webdriver.ChromeOptions()

    if HEADLESS:
        options.add_argument('--headless')
    return options


@pytest.fixture(scope="function")
def driver():
    '''
    Фикстура pytest для инициализации и завершения работы WebDriver.

    - Создаёт экземпляр Chrome с заданными опциями.
    - Устанавливает неявное ожидание элементов в 3 секунды.
    - Передаёт управление тесту через yield.
    - После завершения теста закрывает браузер.

    :return: объект WebDriver.
    '''
    options = __create_chrome_options()
    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(3)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    '''
    Фикстура pytest для создания и подготовки страницы логина.

    - Создаёт объект LoginPage с переданным WebDriver.
    - Открывает страницу логина.
    - Возвращает объект страницы для использования в тестах.

    :param driver: объект WebDriver из фикстуры driver.
    :return: объект LoginPage.
    '''
    page = LoginPage(driver)
    page.get_page()
    return page


@pytest.fixture(scope="function")
def logged_in_project_page(login_page):
    '''
    Фикстура pytest для авторизации пользователя и перехода на страницу проектов.

    - Выполняет вход с валидными данными пользователя.
    - Возвращает объект ProjectsPage с тем же WebDriver.

    :param login_page: объект LoginPage из фикстуры login_page.
    :return: объект ProjectsPage.
    '''
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    return ProjectsPage(login_page.driver)

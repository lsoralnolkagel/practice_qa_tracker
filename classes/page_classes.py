from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import LOGIN_URL, PROJECTS_URL


class BasePage:
    '''
    Базовый класс для работы со страницей в веб-приложении с использованием Selenium WebDriver.
    Предоставляет общие методы для взаимодействия с элементами страницы:
    проверка наличия элемента, ввод текста, клик по элементу, получение текста и значения,
    а также работу с выпадающими списками
    '''
    def __init__(self, driver: WebDriver):
        '''
        Инициализация объекта страницы.

        :param driver: экземпляр WebDriver, управляющий браузером
        '''
        self.driver = driver

    def is_element(self, locator):
        '''
        Проверяет наличие элемента на странице.

        :param locator: кортеж локатора (например, (By.ID, "element_id"))
        :return: True, если элемент найден, иначе False
        '''
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def input_text(self, locator, text):
        '''
        Вводит текст в поле ввода.

        :param locator: кортеж локатора элемента ввода.
        :param text: строка текста для ввода.
        '''
        element = self.driver.find_element(*locator)
        element.send_keys(text)

    def click_element(self, locator):
        '''
        Кликает по элементу.

        :param locator: кортеж локатора элемента для клика.
        '''
        element = self.driver.find_element(*locator)
        element.click()

    def get_element_text(self, locator):
        '''
        Получает текст из элемента.

        :param locator: кортеж локатора элемента.
        :return: текст элемента.
        '''
        return self.driver.find_element(*locator).text

    def get_input_value(self, locator):
        '''
        Получает значение атрибута "value" у элемента ввода.

        :param locator: кортеж локатора элемента ввода.
        :return: значение атрибута "value".
        '''
        return self.driver.find_element(*locator).get_attribute("value")

    def select_variant_by_visible_text(self, locator, text):
        '''
        Выбирает вариант из выпадающего списка по видимому тексту.

        :param locator: кортеж локатора элемента select.
        :param text: видимый текст варианта для выбора.
        '''
        select = Select(self.driver.find_element(*locator))
        select.select_by_visible_text(text)

    def get_selected_variant_text(self, locator):
        '''
        Получает текст выбранного варианта из выпадающего списка.

        :param locator: кортеж локатора элемента select.
        :return: текст выбранного варианта.
        '''
        select = Select(self.driver.find_element(*locator))
        return select.first_selected_option.text


class LoginPage(BasePage):
    '''
    Класс для работы со страницей входа в систему.
    Наследует базовые методы из BasePage и добавляет специфичные для страницы логина элементы и действия.
    '''
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")

    def get_page(self):
        '''
        Открывает страницу логина по заранее заданному URL.

        Использует константу LOGIN_URL, которая должна содержать адрес страницы входа.
        '''
        self.driver.get(LOGIN_URL)

    def login(self, username, password):
        '''
        Выполняет процесс авторизации пользователя.

        :param username: имя пользователя для ввода в поле логина.
        :param password: пароль для ввода в соответствующее поле.
        '''
        self.input_text(self.USERNAME, username)
        self.input_text(self.PASSWORD, password)

        # Ожидание, что в поле USERNAME появится введённый текст
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element_value(self.USERNAME, username)
        )

        # Ожидание, что в поле PASSWORD появится введённый текст
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element_value(self.PASSWORD, password)
        )

        # Клик по кнопке входа в профиль
        self.click_element((By.XPATH, "//button[contains(text(), 'Войти')]"))


class ProjectsPage(BasePage):
    '''
    Класс для работы со страницей проектов.
    Наследует базовые методы из BasePage и добавляет специфичные для страницы действия.
    '''
    HEADER_LOCATOR = (By.CSS_SELECTOR, "header h1")

    def get_page(self):
        '''
        Открывает страницу проектов по заранее заданному URL.

        Использует константу PROJECTS_URL, которая должна содержать адрес страницы c проектами.
        '''
        self.driver.get(PROJECTS_URL)

    def is_projects_page(self):
        '''
        Проверяет, что текущая страница является страницей проектов.

        :return: текст заголовка страницы, если элемент заголовка найден,
                 иначе False.
        '''
        if self.is_element(self.HEADER_LOCATOR):
            return self.get_element_text(self.HEADER_LOCATOR)
        return False

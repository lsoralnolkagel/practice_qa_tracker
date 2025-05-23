import pytest

# список тестов, запускаемых в рамках тестирования
TESTS = [
    "tests/test_login_n_projects.py::test_login_valid_creds",
    "tests/test_login_n_projects.py::test_login_invalid_creds",
    "tests/test_login_n_projects.py::test_select_project_type",
    "tests/test_login_n_projects.py::test_input_project_name"
]


def run_tests_in_order(test_list):
    '''
    Запускает список тестов по порядку и выводит результат выполнения каждого.
    test_list (list): Список строк с путями к тестам в формате 'путь/к_файлу.py::название_теста
    '''

    for test in test_list:

        result = pytest.main([test, "-v"])

        if result == pytest.ExitCode.OK:
            print(f"✅ Тест '{test}' успешно пройден.")
        elif result == pytest.ExitCode.TESTS_FAILED:
            print(f"❌ Тест '{test}' провален.")
        else:
            print(f"⚠️ Тест '{test}' завершён с кодом: {result}")


if __name__ == "__main__":
    run_tests_in_order(TESTS)

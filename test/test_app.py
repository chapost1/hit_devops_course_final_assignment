import environment
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from driver_operations import (
    is_authentication_error_message_displayed,
    grab_authentication_error_mesaage,
    is_counter_container_displayed,
    is_login_container_displayed,
    get_counter_value,
    set_counter_value,
    increment_counter,
    decrement_counter,
    login,
    logout
)


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    options=chrome_options
)

driver.get(environment.APP_URL)


def test_login_with_invalid_credentials():
    login(driver, 'invalid_username', 'invalid_password')
    # validates that the error message is displayed
    is_error_displayed = is_authentication_error_message_displayed(driver)
    assert is_error_displayed == True
    # validates that the error message is correct
    error_message = grab_authentication_error_mesaage(driver)
    assert error_message == 'Invalid username or password'
    # validates that the login container is still displayed
    assert is_login_container_displayed(driver) == True
    # validates that the counter container is not displayed
    assert is_counter_container_displayed(driver) == False


def test_login_with_valid_credentials():
    login(driver, environment.AuthCredentials.username,
          environment.AuthCredentials.password)
    # validates that the error message is not displayed
    is_error_displayed = is_authentication_error_message_displayed(driver)
    assert is_error_displayed == False
    # validates that the counter container is displayed
    assert is_counter_container_displayed(driver) == True
    # validates that the login container is not displayed
    assert is_login_container_displayed(driver) == False


def test_logout():
    # if the counter container is not displayed, login
    if not is_counter_container_displayed(driver):
        login(driver, environment.AuthCredentials.username,
              environment.AuthCredentials.password)
        # after login, validates that the counter container is displayed
        assert is_counter_container_displayed(driver) == True
    # logout
    logout(driver)
    # validates that the counter container is not displayed anymore
    assert is_counter_container_displayed(driver) == False
    # validates that the login container is displayed
    assert is_login_container_displayed(driver) == True


@pytest.mark.parametrize("counter_value", [0, 3, 7])
def test_set_get_counter_value(counter_value: int):
    # if the counter container is not displayed, login
    if not is_counter_container_displayed(driver):
        login(driver, environment.AuthCredentials.username,
              environment.AuthCredentials.password)
        # after login, validates that the counter container is displayed
        assert is_counter_container_displayed(driver) == True
    # set counter value to X
    set_counter_value(driver, counter_value)
    # validates that the counter value is X
    counter_value = get_counter_value(driver)
    assert counter_value == counter_value


def user_session_decorator(test_function):
    def wrapper():
        # login if needed
        if not is_counter_container_displayed(driver):
            login(driver, environment.AuthCredentials.username,
                  environment.AuthCredentials.password)

        counter_value = get_counter_value(driver)

        test_function(counter_value)
        # logout
        logout(driver)
    return wrapper


@user_session_decorator
def test_get_counter_value(counter_value):
    # validates that the counter value is as expected
    assert get_counter_value(driver) == counter_value


@user_session_decorator
def test_increment_counter(counter_value):
    # increment counter
    increment_counter(driver)
    # validates that the counter value is incremented by 1
    assert get_counter_value(driver) == counter_value + 1


@user_session_decorator
def test_decrement_counter(counter_value):
    # increment counter
    increment_counter(driver)
    # validates that the counter value is incremented by 1
    assert get_counter_value(driver) == counter_value + 1
    # decrement counter
    decrement_counter(driver)
    # validates that the counter value is decremented by 1
    assert get_counter_value(driver) == counter_value


@user_session_decorator
def test_counter_value_is_persisted_after_logout(counter_value):
    # increment counter
    increment_counter(driver)
    # validates that the counter value is incremented by 1
    assert get_counter_value(driver) == counter_value + 1
    # logout
    logout(driver)
    # login
    login(driver, environment.AuthCredentials.username,
          environment.AuthCredentials.password)
    # validates that the counter value is persisted
    assert get_counter_value(driver) == counter_value + 1

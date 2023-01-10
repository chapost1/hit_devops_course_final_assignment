import environment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from driver_operations import (
    is_authentication_error_message_displayed,
    grab_authentication_error_mesaage,
    is_counter_container_displayed,
    is_login_container_displayed,
    get_counter_value,
    increment_counter,
    decrement_counter,
    login,
    logout
)


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    options=chrome_options
)

driver.get(environment.APP_URL)



def test_login_with_invalid_credentials():
    login(driver, 'invalid_username', 'invalid_password')
    # validates that the error message is displayed 
    is_error_displayed =  is_authentication_error_message_displayed(driver)
    assert is_error_displayed == True
    # validates that the error message is correct
    error_message = grab_authentication_error_mesaage(driver)
    assert error_message == 'Invalid username or password'
    # validates that the login container is still displayed
    assert is_login_container_displayed(driver) == True
    # validates that the counter container is not displayed
    assert is_counter_container_displayed(driver) == False


def test_login_with_valid_credentials():
    login(driver, environment.AuthCredentials.username, environment.AuthCredentials.password)
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
        login(driver, environment.AuthCredentials.username, environment.AuthCredentials.password)
        # after login, validates that the counter container is displayed
        assert is_counter_container_displayed(driver) == True
    # logout
    logout(driver)
    # validates that the counter container is not displayed anymore
    assert is_counter_container_displayed(driver) == False
    # validates that the login container is displayed
    assert is_login_container_displayed(driver) == True


def user_session_decorator(test_function):
    def wrapper():
        # login if needed
        if not is_counter_container_displayed(driver):
            login(driver, environment.AuthCredentials.username, environment.AuthCredentials.password)
        test_function()
        # logout
        logout(driver)
    return wrapper
    

@user_session_decorator
def test_counter_value_is_zero_on_login():
    # validates that the counter value is 0
    assert get_counter_value(driver) == 0


@user_session_decorator
def test_increment_counter():
    # increment counter
    increment_counter(driver)
    # validates that the counter value is 1
    assert get_counter_value(driver) == 1


@user_session_decorator
def test_decrement_counter():
    # increment counter
    increment_counter(driver)
    # validates that the counter value is 1
    assert get_counter_value(driver) == 1
    # decrement counter
    decrement_counter(driver)
    # validates that the counter value is 0
    assert get_counter_value(driver) == 0


@user_session_decorator
def test_counter_value_is_zero_after_logout():
    # increment counter
    increment_counter(driver)
    # validates that the counter value is 1
    assert get_counter_value(driver) == 1
    # logout
    logout(driver)
    # login
    login(driver, environment.AuthCredentials.username, environment.AuthCredentials.password)
    # validates that the counter value is 0
    assert get_counter_value(driver) == 0

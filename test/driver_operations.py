from selenium.webdriver.common.by import By
import time


def is_login_container_displayed(driver):
    time.sleep(0.1)
    login_container = driver.find_element(by=By.ID, value='login-container')
    return login_container.is_displayed()


def enter_username(driver, username):
    time.sleep(0.1)
    username_field = driver.find_element(by=By.ID, value='username')
    username_field.clear()
    username_field.send_keys(username)
    return driver


def enter_password(driver, password):
    time.sleep(0.1)
    password_field = driver.find_element(by=By.ID, value='password')
    password_field.clear()
    password_field.send_keys(password)
    return driver


def is_authentication_error_message_displayed(driver):
    time.sleep(0.1)
    error_message = driver.find_element(by=By.ID, value='authentication-error')
    return error_message.is_displayed()


def grab_authentication_error_mesaage(driver):
    time.sleep(0.1)
    error_message = driver.find_element(by=By.ID, value='authentication-error')
    return error_message.text


def click_login_button(driver):
    time.sleep(0.1)
    login_button = driver.find_element(by=By.ID, value='login-button')
    login_button.click()
    return driver


def login(driver, username, password):
    enter_username(driver, username)
    enter_password(driver, password)
    click_login_button(driver)
    return driver


def is_counter_container_displayed(driver):
    time.sleep(0.1)
    time.sleep(0.1)
    counter_container = driver.find_element(
        by=By.ID, value='counter-container')
    return counter_container.is_displayed()


def click_logout_button(driver):
    time.sleep(0.1)
    logout_button = driver.find_element(by=By.ID, value='logout-button')
    # logout_button.click() -- this does not work because the button is hidden by the counter container via lower z-index
    driver.execute_script("arguments[0].click();", logout_button)
    return driver


def logout(driver):
    click_logout_button(driver)
    return driver


def get_counter_value(driver):
    time.sleep(0.1)
    counter_value = driver.find_element(by=By.ID, value='counter-value')
    return int(counter_value.text)


def set_counter_value(driver, value):
    time.sleep(0.1)
    driver.execute_script(f"userSession.setCounterValue({value});")


def increment_counter(driver):
    time.sleep(0.1)
    increment_button = driver.find_element(by=By.ID, value='increment-button')
    increment_button.click()
    return driver


def decrement_counter(driver):
    time.sleep(0.1)
    decrement_button = driver.find_element(by=By.ID, value='decrement-button')
    decrement_button.click()
    return driver

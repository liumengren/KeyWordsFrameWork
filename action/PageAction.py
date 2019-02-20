from selenium import webdriver
from config.VarConfig import chromeDriverPath
from config.VarConfig import firefoxDriverPath
from util.ObjectMap import getElement
from util.ClipboardUtil import Clipboard
from util.KeyBoardUtil import KeyboardKeys
from util.DirAndTime import *
from util.WaitUtil import WaitUtil
from selenium.webdriver.chrome.options import Options
import time


driver = None
waitUtil = None


def open_browser(browserName, *arg):
    global driver, waitUtil
    try:
        if browserName.lower() == 'chrome':
            driver = webdriver.Chrome(executable_path=chromeDriverPath)
        else:
            driver = webdriver.Firefox(executable_path=firefoxDriverPath)
        waitUtil = WaitUtil(driver)
    except Exception as e:
        raise e


def visit_url(url, *arg):
    global driver
    try:
        driver.get(url)
    except Exception as e:
        raise e


def close_browser(*arg):
    global driver
    try:
        driver.quit()
    except Exception as e:
        raise e


def sleep(sleepSeconds, *arg):
    try:
        time.sleep(int(sleepSeconds))
    except Exception as e:
        raise e


def clear(locationType, locatorExpression, *arg):
    global driver
    try:
        getElement(driver, locationType, locatorExpression).clear()
    except Exception as e:
        raise e


def input_string(locationType, locatorExpression, inputContent):
    global driver
    try:
        getElement(driver, locationType, locatorExpression).send_keys(inputContent)
    except Exception as e:
        raise e


def click(locationType, locatorExpression, *arg):
    global driver
    try:
        getElement(driver, locationType, locatorExpression).click()
    except Exception as e:
        raise e


def assert_string_in_pagesource(assertString, *arg):
    global driver
    try:
        assert assertString in driver.page_source, "%s not found in page source!" % assertString
    except AssertionError as e:
        raise AssertionError(e)
    except Exception as e:
        raise e


def assert_title(titleStr, *arg):
    global driver
    try:
        assert titleStr in driver.title, "%s not found in title!" % titleStr
    except AssertionError as e:
        raise AssertionError(e)
    except Exception as e:
        raise e


def getTitle(*arg):
    global driver
    try:
        return driver.title
    except Exception as e:
        raise e


def getPageSource(*arg):
    global driver
    try:
        return driver.page_source
    except Exception as e:
        raise e


def switch_to_frame(locationType, frameLocatorExpression, *arg):
    global driver
    try:
        driver.switch_to.frame(getElement(driver, locationType, frameLocatorExpression))
    except Exception as e:
        raise e


def switch_to_default_content(*arg):
    global driver
    try:
        driver.switch_to.default_content()
    except Exception as e:
        raise e


def paste_string(pasteString, *arg):
    try:
        Clipboard.setText(pasteString)
        time.sleep(2)
        KeyboardKeys.twoKey("ctrl", "v")
    except Exception as e:
        raise e


def press_tab_key(*arg):
    try:
        KeyboardKeys.oneKey("tab")
    except Exception as e:
        raise e


def press_enter_key(*arg):
    try:
        KeyboardKeys.oneKey("enter")
    except Exception as e:
        raise e


def maximize_browser():
    global driver
    try:
        driver.maximize_window()
    except Exception as e:
        raise e


def capture_screen(*arg):
    global driver
    currTime = getCurrentTime()
    picNameAndPath = str(createCurrentDateDir()) + "\\" + str(currTime) + ".png"
    try:
        driver.get_screenshot_as_file(picNameAndPath.replace('\\', '\\'))
    except Exception as e:
        raise e
    else:
        return picNameAndPath


def waitPresentOfElementLocated(locationType, locatorExpression, *arg):
    global waitUtil
    try:
        waitUtil.presenceOfElementLocated(locationType, locatorExpression)
    except Exception as e:
        raise e


def waitFrameToBeAvaliableAndSwitchToIt(locationType, locatorExpression, *arg):
    global waitUtil
    try:
        waitUtil.frame_available_and_switch_to_it(locationType, locatorExpression)
    except Exception as e:
        raise e


def waitVisibilityOfElementLocated(locationType, locatorExpression, *arg):
    global waitUtil
    try:
        waitUtil.visibility_element_located(locationType, locatorExpression)
    except Exception as e:
        raise e
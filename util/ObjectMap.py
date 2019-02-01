from selenium.webdriver.support.ui import WebDriverWait


def getElement(driver,locationType,locatorExpression):
    try:
        element = WebDriverWait(driver, 30).until(lambda x: x.find_element(by=locationType, value=locatorExpression))
        return element
    except Exception as e:
        raise e


def getElements(driver,locationType,locatorExpression):
    try:
        elements = WebDriverWait(driver, 30).until(lambda x: x.find_elements(by=locationType, value=locatorExpression))
        return elements
    except Exception as e:
        raise e
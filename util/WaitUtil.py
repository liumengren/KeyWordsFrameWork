from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class WaitUtil(object):
    def __init__(self, driver):
        self.locationDict = {
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "css_selector": By.CSS_SELECTOR,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT
        }
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30)

    def presenceOfElementLocated(self, locatorMethod, locatorExpression, *arg):
        try:
            if self.locationDict.has_key(locatorMethod.lower()):
                element = self.wait.until(EC.presence_of_element_located
                                ((self.locationDict[locatorMethod.lower()], locatorExpression)))
                return element
            else:
                raise TypeError("未找到定位方式，请确认定位方法是否正确")
        except Exception as e:
            raise e

    def frame_available_and_switch_to_it(self, locationType, locatorExpression, *arg):
        try:
            self.wait.until(EC.frame_to_be_available_and_switch_to_it
                            ((self.locationDict[locationType.lower()], locatorExpression)))
        except Exception as e:
            raise e

    def visibility_element_located(self, locationType, locatorExpression, *arg):
        try:
            element = self.wait.until(EC.visibility_of_element_located
                            ((self.locationDict[locationType.lower()], locatorExpression)))
            return element
        except Exception as e:
            raise e


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path="D:\\Browserdriver\\chromedriver.exe")
    driver.get("http://mol.uat.bwoilmarine.com/mybusiness/#/login")
    driver.maximize_window()
    time.sleep(10)
    wu = WaitUtil(driver)
    wu.visibility_element_located("id", "username").send_keys("CargoOwnerMOL@bwoil.com")
    wu.visibility_element_located("id", "password").send_keys("00000000")
    wu.visibility_element_located("xpath", '//span[text()="Login"]/..').click()
    time.sleep(10)
    driver.quit()

# -*- coding: utf-8 -*-
from selenium import webdriver
#from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import login
#display = Display(visible=0, size=(1024, 768))
#display.start()
class TestPautasTestUtp(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox() #Para ir viendo cada paso en firefox
        #self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(30)
        self.base_url = "http://146.83.216.177/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_pautas_test_utp(self):
        driver = login.test_login_utp(self)

        driver.find_element_by_css_selector("#pautas > span").click()
        try: self.assertEqual(u"Nueva Pauta de Evaluación", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        #display.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import login
display = Display(visible=0, size=(1024, 768))
display.start()
class TestVerCursoBonusMayor(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://bakhan.accionstem.cl/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_ver_curso_bonus_mayor(self):
        driver = login.test_login_utp(self)
        self.assertEqual("1ro basico A 2016 Test", driver.find_element_by_css_selector("font").text)
        driver.find_element_by_link_text("Ver Curso").click()
        driver.find_element_by_css_selector("circle.assesment.assesment144").click()
        driver.find_element_by_id("input_grade_teacher").clear()
        driver.find_element_by_id("input_grade_teacher").send_keys("8")
        maxgrade=driver.find_element_by_id("hiddenMaxGrade").get_attribute("value")
        sugerida=driver.find_element_by_id("sugerida").get_attribute("value")
        teacher=driver.find_element_by_id("input_grade_teacher").get_attribute("value")
        final=driver.find_element_by_id("final").get_attribute("value")
        if (sugerida+teacher)>maxgrade:
            try:
                self.assertTrue(maxgrade, final)
            except AssertionError as e:
                self.verificationErrors.append(str(e))


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
        self.assertEqual([], self.verificationErrors)
        display.popen.kill()

if __name__ == "__main__":
    unittest.main()

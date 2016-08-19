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

class TestVercursoVergruposContactos1erMedioA(unittest.TestCase):
    display = Display(visible=0, size=(1024, 768))
    display.start()
    def setUp(self):
        self.driver = webdriver.Firefox() #Para ir viendo cada paso en firefox
        #self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(30)
        self.base_url = "http://146.83.216.177/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_vercurso_vergrupos_contactos1er_medio_a(self):
        driver = login.test_login_utp(self)
        try: self.assertEqual("1ro medio A 2016", driver.find_element_by_xpath("//div[3]/div/div/ul/div/font").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//a[contains(text(),'Ver Curso')])[3]").click()
        try: self.assertEqual("CURSO / 1RO MEDIO A", driver.find_element_by_id("breadcrumb").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("#inicio > span").click()
        try: self.assertEqual("1ro medio A 2016", driver.find_element_by_xpath("//div[3]/div/div/ul/div/font").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//a[contains(text(),'Ver Grupos')])[3]").click()
        try: self.assertEqual("No hay agrupaciones realizadas.", driver.find_element_by_css_selector("#popup > p.response").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("close").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Ver Contactos')])[3]").click()
        try: self.assertEqual("Estudiantes", driver.find_element_by_id("Alumnos").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("td.editablegrid-student_email").click()
        try: self.assertEqual("Apoderados", driver.find_element_by_id("Apoderados").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("inicio").click()
    
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
        display.sendstop()

if __name__ == "__main__":
    unittest.main()

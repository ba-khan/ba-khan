# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import login

class TestVerCursoEditarNombre(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://146.83.216.177/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_ver_curso_editar_nombre(self):
        driver = login.test_login_utp(self)
        self.assertEqual("1ro basico A 2016 Test", driver.find_element_by_css_selector("font").text)
        driver.find_element_by_link_text("Ver Curso").click()
        driver.find_element_by_css_selector("button.editButton").click()
        driver.find_element_by_id("input_nombre").clear()
        driver.find_element_by_id("input_nombre").send_keys(u"prueba máil1")
        nombre=driver.find_element_by_id("input_nombre").get_attribute("value")
        driver.find_element_by_id("button_editar").click()
        try:
            self.assertEqual("Datos mal ingresados o incompletos, revise los campos incompletos o en color rojo", driver.find_element_by_css_selector("#popupEvaluacion > p").text)
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

if __name__ == "__main__":
    unittest.main()
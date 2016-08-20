# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

def test_login_utp(self):
    driver = self.driver
    driver.get(self.base_url + "/")
    driver.find_element_by_id("loginButton").click()

    # ERROR: Caught exception [ERROR: Unsupported command [waitForPopUp | _blank | 30000]]
    # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | name=_blank | ]]
    for i in range(60):
        try:
            driver.switch_to_window(driver.window_handles[1])
            break
        except: pass
        time.sleep(1)
    else: self.fail("time out waiting for the popup")

    for i in range(60):
        try:
            if "" == driver.find_element_by_name("identifier").text: break
        except: pass
        time.sleep(1)
    else: self.fail("time out waiting for the login form")
    driver.find_element_by_name("identifier").clear()
    driver.find_element_by_name("identifier").send_keys("utpbakhan")
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys("clave1234")
    driver.find_element_by_link_text("Sign in").click()
    for i in range(60):
        try:
            if "BakhanUTP2" == driver.find_element_by_css_selector("span.consumer-name").text: break
        except: pass
        time.sleep(1)
    else: self.fail("time out waiting for the authentication")
    driver.find_element_by_link_text("Aceptar").click()

    # ERROR: Caught exception [ERROR: Unsupported command [selectWindow |  | ]]
    driver.switch_to_window(driver.window_handles[0])
    
    for i in range(60):
        try:
            if "HOLA ADMINISTRADOR UTP" == driver.find_element_by_css_selector("span.header-text").text: break
        except: pass
        time.sleep(1)
    else: self.fail("time out waiting for the principal page")
    return driver
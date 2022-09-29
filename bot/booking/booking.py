# This file contains the methods/actions that the bot will take

import os
import time
from selenium import webdriver
import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from prettytable import PrettyTable

#Inherit webdriver.Chrome methods (interact with browser.)
class Booking(webdriver.Chrome):
    #constructor
    def __init__(self, driver_path=const.PATH, teardown=False):
        self.driver_path = driver_path
        #teardown allows us to choose when quitting the browser is applicable
        self.teardown = teardown
        # Add driver location to PATH
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions() #Remove Chrome DevTool listening logs from CLI
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options) #instantiates webdriver.Chrome as well
        self.implicitly_wait(15)
        self.maximize_window()

    #Get booking.com URL
    def land_first_page(self):
        self.get(const.BASE_URL)

    #Change currency to USD on landing page
    def change_currency(self, currency=None):
        currency_element = self.find_element(by=By.CSS_SELECTOR, value='button[data-tooltip-text="Choose your currency"]')
        currency_element.click()
        selected_currency_element = self.find_element(by=By.CSS_SELECTOR, value=f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')
        selected_currency_element.click()
    
    #Send value to detsination input field and click first option from dropdown
    def select_place_to_go(self, destination=None):
        destination_element = self.find_element(by=By.ID, value="ss")
        destination_element.clear()
        destination_element.send_keys(destination)
        first_result = self.find_element(by=By.CSS_SELECTOR, value='li[data-i="0"]')
        first_result.click()
    
    #Click on check-in and check-out dates
    def select_date(self, check_in_date, check_out_date):
        check_in_element = self.find_element(by=By.CSS_SELECTOR, value=f'td[data-date="{check_in_date}"]')
        check_in_element.click()
        check_out_element = self.find_element(by=By.CSS_SELECTOR, value=f'td[data-date="{check_out_date}"]')
        check_out_element.click()

    # Select quantity of adults
    def select_adults(self, count=1):
        selection_element = self.find_element(by=By.ID, value="xp__guests__toggle")
        selection_element.click()

        #decrease adults to min value (1)
        while True:
            decrease_adults_element = self.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Decrease number of Adults"]')
            decrease_adults_element.click()
            adults_value_element = self.find_element(by=By.ID, value="group_adults")
            adults_value = adults_value_element.get_attribute("value")
            if int(adults_value) == 1:
                break
        
        #increase adults value to desired amount
        increase_adults_element = self.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Increase number of Adults"]')
        for i in range(count -1):
            increase_adults_element.click()

    # Select quantity of children
    def select_children(self, count=0):
        selection_element = self.find_element(by=By.ID, value="xp__guests__toggle")
        selection_element.click()

        #decrease children to min value (0)
        while True:
            decrease_children_element = self.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Decrease number of Children"]')
            decrease_children_element.click()
            children_value_element = self.find_element(by=By.ID, value="group_children")
            children_value = children_value_element.get_attribute("value")
            if int(children_value) == 0:
                break

        #increase children value to desired amount
        increase_children_element = self.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Increase number of Children"]')
        for _ in range(count -1):
            increase_children_element.click()
    
        #Set default child age for all children
        for i in range(count -1):
            child_age_element = self.find_element(by=By.CSS_SELECTOR, value=f'select[aria-label="Child {i+1} age"]')
            default_age = child_age_element.find_element(by=By.CSS_SELECTOR, value='option[value="12"]' )
            default_age.click() 
            
    # Select quantity of desired rooms
    def select_rooms(self, count=1):
        selection_element = self.find_element(by=By.ID, value="xp__guests__toggle")
        selection_element.click()

        #decrease rooms to min value (0)
        while True:
            decrease_room_element = self.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Decrease number of Rooms"]')
            decrease_room_element.click()
            room_value_element = self.find_element(by=By.ID, value="no_rooms")
            room_value = room_value_element.get_attribute("value")
            if int(room_value) == 1:
                break

        #increase rooms value to desired amount
        increase_room_element = self.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Increase number of Rooms"]')
        for i in range(count -1):
            increase_room_element.click()

    # Submit search request
    def click_search(self):
        search = self.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]')
        search.click()
    
    # Sometimes a sign-in prompt might appear, which is handled with this method
    def dismiss_sign_in(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info.]')).click()
            )
        except:
            print("No sign in prompt")

    #Bring filtration methods into booking file to create object
    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        #Run filtration methods
        filtration.apply_lowest_price()
        time.sleep(2)
        filtration.apply_star_ratings(3, 4, 5)
        time.sleep(2)
        
    #Print retrieved data in an organized table
    def report_results(self):
        hotel_boxes = self.find_element(by=By.CLASS_NAME, value="d4924c9e74")
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names = ['Hotel Name', 'Hotel Score', 'Hotel Price']
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)
        
    # Quit the Chrome browser
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit() #Shuts down Chrome browser



    
#This file includes a class with methods that will apply 
# filtrations on the initial search results.

from selenium.webdriver.remote.webdriver import WebDriver #Allow autocompletion of "find_element" options
from selenium.webdriver.common.by import By
import time

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    #Click on desired star rating fields 
    def apply_star_ratings(self, *star_values):
        time.sleep(5)
        for star_value in star_values:
            try:
                star_checkbox = self.driver.find_element(by=By.NAME, value=f'class={star_value}')
                star_checkbox.click()
            except:
                print("No star box located")
    
    # Click on sort by button and choose "Price (lowest first)" from the dropdwown
    def apply_lowest_price(self):
        sort_by_button = self.driver.find_element(by=By.CSS_SELECTOR, value='button[data-testid="sorters-dropdown-trigger"]')
        sort_by_button.click()

        self.driver.implicitly_wait(5)
        drop_down = self.driver.find_element(by=By.CSS_SELECTOR, value='div[data-testid="sorters-dropdown"]')
        lowest_price_button = drop_down.find_element(by=By.CSS_SELECTOR, value='button[data-id="price"]')
        lowest_price_button.click()

        
        
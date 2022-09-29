# This file is dedicated to methods that will parse data 
# from the 25 deal boxes in the first page of results.

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement #Allow autocompletion of "find_element" options

class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    #Returns HTML content for the 25 deal boxes.
    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            by=By.CSS_SELECTOR, value='div[data-testid="property-card"]')
    
    def pull_deal_box_attributes(self):
        data_collection = []
        #For every one of the 25 deal boxes, we will extract the hotel name, score and price.
        for deal_box in self.deal_boxes:
            #Pull titles
            hotel_name = deal_box.find_element(by=By.CSS_SELECTOR, value='div[data-testid="title"]').get_attribute('innerHTML').strip()

            #Pull score
            hotel_score = deal_box.find_element(by=By.CLASS_NAME, value="d10a6220b4").get_attribute('innerHTML').strip()

            #Pull prices
            hotel_price = deal_box.find_element(by=By.CLASS_NAME, value="bd73d13072").get_attribute('innerHTML').strip()

            #Append results to multi-dimensiona list that will contain the report info.
            data_collection.append([hotel_name, hotel_score, hotel_price])
        return data_collection



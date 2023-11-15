from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from settings import SettingBNA

class BnaProcess:
    def __init__(self) -> None:
        self.url = "https://www.bna.com.ar/Personas"
        
    def open(self) -> None:
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.driver.implicitly_wait(0.5)
        
    def close(self) -> None:
        self.driver.quit()
        
    def get_all_foreign_bills(self) -> dict:
        return self.__get_dict_from_table("Billetes")
    
    def get_all_foreign_exchanges(self) -> dict:
        return self.__get_dict_from_table("Divisas")
    
    def get_foreign_bills_for(self, requests: list[str]) -> dict:
        bills = self.get_all_foreign_bills()
        return {r: bills[r] for r in requests if r in bills}
    
    def get_foreign_exchanges_for(self, requests: list[str]) -> dict:
        foreign_exchanges = self.get_all_foreign_exchanges()
        return {r: foreign_exchanges[r] for r in requests if r in foreign_exchanges}
            
    def __get_elements_from_prices(self, price: str) -> list[WebElement]:
        self.driver.find_element(by=By.XPATH, 
                                 value="//a[contains(string(), 'Cotización " + price.capitalize() + "')]"
                                ).click()
        return self.driver.find_elements(by=By.XPATH, 
                                  value="//div[@id='" + price.lower() + "']//child::tbody//descendant::tr")
        
    def __get_dict_from_table(self, name: str) -> dict:
        new_dict = {}
        for element in self.__get_elements_from_prices(name):
            coin = element.find_element(by=By.CLASS_NAME, value="tit").get_attribute("innerHTML")
            new_dict[coin] = {}
            
            td_elements = element.find_elements(by=By.TAG_NAME, value="td")
            new_dict[coin]["Purchase"] = td_elements[1].get_attribute("innerHTML")
            new_dict[coin]["Sale"] = td_elements[2].get_attribute("innerHTML")
            
        return new_dict
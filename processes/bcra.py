from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
import time

class BcraProcess:
    def __init__(self) -> None:
        self.url = "https://www.bcra.gob.ar/"
        
    def open(self) -> None:
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.driver.implicitly_wait(0.5)
        
    def close(self) -> None:
        self.driver.quit()
        
    def go_to_exchange_rate_by_date_section(self) -> None:
        self.driver.find_element(by=By.XPATH, value="//a[contains(string(), 'Estadísticas')]").click()
        self.driver.find_element(by=By.XPATH, value="//a[contains(string(), 'Tipos de cambio')]").click()
        self.driver.find_element(by=By.XPATH, value="//a[contains(string(), 'Cotizaciones por fecha')]").click()
        self.driver.implicitly_wait(0.5)
        
    def set_date_in_calendar(self, date: str) -> None:
        self.driver.find_element(by=By.TAG_NAME, value="input").click()
        self.__validate_date_format(date=date)
        date_list = date.split("-")
        self.__set_month(month=self.__get_spanish_month(month=int(date_list[1].strip("0"))))
        self.__set_year(year=int(date_list[2]))
        self.__set_day(day=int(date_list[0].strip("0")))

        self.driver.find_element(by=By.CLASS_NAME, value="btn").click()
        self.driver.implicitly_wait(0.5)
    
    def get_all_exchange_rates(self) -> dict:
        new_dict = {}
        tr_elements = self.driver.find_elements(by=By.XPATH, value="//table//child::tbody//descendant::tr")
        for tr in tr_elements:
            td_elements = tr.find_elements(by=By.TAG_NAME, value="td")
            key = td_elements[0].get_attribute("innerHTML").strip()
            new_dict[key] = {}
            new_dict[key]["col"] = td_elements[1].get_attribute("innerHTML").strip()
            new_dict[key]["col2"] = td_elements[2].get_attribute("innerHTML").strip()
            
        return new_dict
    
    def get_exchange_rates_for(self, requests: list[str]) -> dict:
        exchanges = self.get_all_exchange_rates()
        return {r: exchanges[r] for r in requests if r in exchanges}    
            
    def __set_month(self, month: str) -> None:
        while True:
            time.sleep(1)
            year_month_table_controls = self.driver.find_element(by=By.ID, value="tcalControls")
            year_month_text = year_month_table_controls.find_element(by=By.TAG_NAME, value="th").get_attribute("innerHTML")
            month_text = year_month_text.split()[0]

            if(month_text != month):
                year_month_table_controls.find_element(by=By.ID, value="tcalNextMonth").click()
            else:
                break
            
    def __set_year(self, year: int) -> None:
        while True:
            time.sleep(1)
            year_month_table_controls = self.driver.find_element(by=By.ID, value="tcalControls")
            year_month_text = year_month_table_controls.find_element(by=By.TAG_NAME, value="th").get_attribute("innerHTML")
            year_calendar = int(year_month_text.split()[1])
            if(year_calendar != year):
                if(year_calendar > year):
                    year_month_table_controls.find_element(by=By.ID, value="tcalPrevYear").click()
                else:
                    year_month_table_controls.find_element(by=By.ID, value="tcalNextYear").click()
            else:
                break
            
    def __set_day(self, day: int) -> None:
        days = self.driver.find_elements(by=By.XPATH, value="//table[@id='tcalGrid']//descendant::td")
        for d in days:
            if(int(d.get_attribute("innerHTML")) == day):
                d.click()
                break
            
    def __get_spanish_month(self, month: int) -> str:
        print(month)
        spanish_months = [None, 'Enero','Febrero','Marzo','Abril',
                        'Mayo','Junio','Julio','Agosto',
                        'Septiembre','Octubre','Noviembre','Diciembre']
        return spanish_months[month]
    
    def __validate_date_format(self, date: str) -> None:
        if date != datetime.strptime(date, '%d-%m-%Y').strftime('%d-%m-%Y'):
            raise ValueError
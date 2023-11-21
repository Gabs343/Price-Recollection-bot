import time

from settings import *
from processes.bna import BnaProcess
from processes.bcra import BcraProcess
        
class Main:
    __settings_services: list[SettingService] = []
    __bot_name = "BOT_1"
    __status = "READY"
    
    def __init__(self) -> None:
        for setting in (SettingSap, SettingBNA, SettingBCRA):
            self.__settings_services.append(setting())
    
    @property   
    def settings_services(self) -> list[SettingService]:
        return self.__settings_services
    
    @property   
    def bot_name(self) -> str:
        return self.__bot_name
    
    @property   
    def status(self) -> str:
        return self.__status
        
    def start(self) -> None:
        
        '''
        bna = BnaProcess()
        bna.open()
        print(bna.get_foreign_bills_for(self.get_settings(SettingBNA)["Foreign_Bills"]))
        print(bna.get_foreign_exchanges_for(self.get_settings(SettingBNA)["Foreign_Exchange"]))
        bna.close()
        '''
        
        bcra = BcraProcess()
        bcra.open()
        bcra.go_to_exchange_rate_by_date_section()
        bcra.set_date_in_calendar(self.get_settings(SettingBCRA)["Date"])
        print(bcra.get_exchange_rates_for(self.get_settings(SettingBCRA)["Coins"]))
        bcra.close()
            
    def get_settings(self, setting_type: SettingService) -> dict:
        #gives StopIteration Exception
        service = next(setting for setting in self.settings_services if isinstance(setting, setting_type)) 
        return service.settings
    

if __name__ == "__main__":
    st = time.time()
    main = Main()
    main.start()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    

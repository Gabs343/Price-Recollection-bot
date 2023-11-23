import time

from datetime import datetime
from settings import *
from processes.bna import BnaProcess
from processes.bcra import BcraProcess
from processes.sap import Sap
from log import LogTxt, LogXlsx
        
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
        self.logTxt = LogTxt(name=f'Log-{datetime.now().strftime("%d.%m.%Y_%H%M%S")}')
        self.logXlsx = LogXlsx(name=f'Log-{datetime.now().strftime("%d.%m.%Y_%H%M%S")}')
        self.logTxt.create()
        self.logXlsx.create()
        
        self.data = {}
        
        self.do_bna_procces()
        self.do_bcra_procces()
        
        print(self.data)
        
        self.logTxt.close()
        self.logXlsx.close()
 
        
    def do_bna_procces(self):
        try:
            self.logTxt.write_info(message='The Bna process has begun')
            self.data['bna'] = {}
            settings = self.logTxt.write_and_execute(self.get_settings, SettingBNA)
            
            bna = BnaProcess()
            self.logTxt.write_and_execute(bna.open)
            foreign_bills = self.logTxt.write_and_execute(bna.get_foreign_bills_for, settings['foreignBills'])            
            foreign_exchanges = self.logTxt.write_and_execute(bna.get_foreign_exchanges_for, settings['foreignExchange'])
            self.logTxt.write_and_execute(bna.close)
            
            self.data['bna']['foreignBills'] = foreign_bills
            self.data['bna']['foreignExchange'] = foreign_exchanges
            
            self.logXlsx.write_info(message='Bna Process')
            self.logTxt.write_info(message='Bna process completed')
        except KeyError as e:
            self.logXlsx.write_error(message='Bna Process', detail='Key error')
            self.logTxt.write_error(message=f'Key Error: {e}')
        except StopIteration as e:
            self.logXlsx.write_error(message='Bna Process', detail='Problem with BNA Settings')
            self.logTxt.write_error(message=e)
        except Exception as e:
            self.logXlsx.write_error(message='Bna Process', detail='Unknown error')
            self.logTxt.write_error(message=e)
            
    def do_bcra_procces(self):
        try:
            self.logTxt.write_info(message='The Bcra process has begun')
            self.data['bcra'] = {}
            settings = self.logTxt.write_and_execute(self.get_settings, SettingBCRA)
            
            bcra = BcraProcess()
            self.logTxt.write_and_execute(bcra.open)
            self.logTxt.write_and_execute(bcra.go_to_exchange_rate_by_date_section)
            self.logTxt.write_and_execute(bcra.set_date_in_calendar, settings['date'])
            exchange_rates = self.logTxt.write_and_execute(bcra.get_exchange_rates_for, settings["coins"])
            self.logTxt.write_and_execute(bcra.close)
            
            self.data['bcra']['exchange_rates'] = exchange_rates
            
            self.logXlsx.write_info(message='Bcra Process')
            self.logTxt.write_info(message='Bcra process completed')
        except KeyError as e:
            self.logXlsx.write_error(message='Bna Process', detail='Key error')
            self.logTxt.write_error(message=f'Key Error: {e}')
        except StopIteration as e:
            self.logXlsx.write_error(message="Settings not found", detail="Problem with BCRA Settings")
            self.logTxt.write_error(message=e)
        except Exception as e:
            self.logXlsx.write_error(message="Bcra Process", detail="Unknown error")
            self.logTxt.write_error(message=e)
        
    def do_sap_procces(self):
        try:
            sap = Sap()
            sap.login(credentials=self.get_settings(SettingSap))
            sap.set_transaction("")
            sap.new_register()
        except StopIteration as e:
            self.logXlsx.write_error(message="Settings not found", detail="Problem with SAP Settings")
            self.logTxt.write_error(message=e)
        except Exception as e:
            self.logXlsx.write_error(message="Sap Process", detail="Unknown error")
            self.logTxt.write_error(message=e)
            
    def get_settings(self, setting_type: SettingService) -> dict:
        service = next(setting for setting in self.settings_services if isinstance(setting, setting_type)) 
        return service.settings
    

if __name__ == "__main__":
    st = time.time()
    main = Main()
    main.start()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    

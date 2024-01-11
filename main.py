import time
import sys
from settings import *
from log import *
from processes.bna import BnaProcess
from processes.bcra import BcraProcess
from processes.sap import Sap
from exceptions import ServiceNotFound

class Main:
    __settings_services_classes: tuple = (BNASetting, BCRASetting, SapSetting)
    __logs_services_classes: tuple = (LogTxt, LogXlsx, LogVideo)
    __settings_services: list[SettingService] = []
    __logs_services: list[LogService] = []
    __bot_name = "Price-Recollection"
    __status = "READY"
    __status_callback = None
    __had_error: bool = False
    
    def __init__(self) -> None:
        self.__settings_services = self.__get_settings_services()
        
    @property   
    def settings_services(self) -> list[SettingService]:
        return self.__settings_services
    
    @property   
    def logs_services(self) -> list[LogService]:
        return self.__logs_services
    
    @property   
    def bot_name(self) -> str:
        return self.__bot_name
    
    @property   
    def status(self) -> str:
        return self.__status
    
    @property   
    def status_callback(self) -> str:
        return self.__status_callback
    
    @status_callback.setter
    def status_callback(self, callback) -> None:
        self.__status_callback = callback
        
    def start(self, *args) -> None:
        try:
            self.__execution_begun()

            self.logXlsx: LogXlsx = self.__get_log_service(LogXlsx)
            self.logTxt: LogTxt = self.__get_log_service(LogTxt)
            
            self.data = {}
            
            self.do_bna_procces()
            self.do_bcra_procces()
            
            print(self.data)
            
            self.__execution_completed()
        except:
            pass

        
    def do_bna_procces(self):
        try:
            self.__execute_action(function=self.logTxt.write_info, message='The Bna process has begun')
            self.data['bna'] = {}
            
            setting_service = self.__execute_action(function=self.__get_setting_service, setting_type=BNASetting)

            bna = BnaProcess()
            self.__execute_action(function=bna.open)
            foreign_bills = self.__execute_action(function=bna.get_foreign_bills_for, requests=setting_service.settings['foreignBills'])            
            foreign_exchanges = self.__execute_action(function=bna.get_foreign_exchanges_for, requests=setting_service.settings['foreignExchange'])
            self.__execute_action(function=bna.close)
            
            self.data['bna']['foreignBills'] = foreign_bills
            self.data['bna']['foreignExchange'] = foreign_exchanges
            
            self.__execute_action(function=self.logXlsx.write_info, message='Bna Process')
            self.__execute_action(function=self.logTxt.write_info, message='Bna process completed')
            
        except KeyError as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bna Process', detail='Key error')
            self.__execute_action(function=self.logTxt.write_error, message=f'Key Error: {e}')
            self.__had_error = True
            
        except StopIteration as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bna Process', detail='Problem with BNA Settings')
            self.__execute_action(function=self.logTxt.write_error, message=e)
            self.__had_error = True
            
        except Exception as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bna Process', detail='Unknown error')
            self.__execute_action(function=self.logTxt.write_error, message=e)
            self.__had_error = True

    def do_bcra_procces(self):
        try:
            self.__execute_action(function=self.logTxt.write_info, message='The Bcra process has begun')
            self.data['bcra'] = {}
            setting_service = self.__execute_action(function=self.__get_setting_service, setting_type=BCRASetting)
            
            bcra = BcraProcess()
            self.__execute_action(function=bcra.open)
            self.__execute_action(function=bcra.go_to_exchange_rate_by_date_section)
            self.__execute_action(function=bcra.set_date_in_calendar, date=setting_service.settings['date'])
            exchange_rates = self.__execute_action(function=bcra.get_exchange_rates_for, requests=setting_service.settings["coins"])
            self.__execute_action(function=bcra.close)
            
            self.data['bcra']['exchange_rates'] = exchange_rates
            
            self.__execute_action(function=self.logXlsx.write_info, message='Bcra Process')
            self.__execute_action(function=self.logTxt.write_info, message='Bcra process completed')
            
        except KeyError as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bcra Process', detail='Key error')
            self.__execute_action(function=self.logTxt.write_error, message=f'Key Error: {e}')
            self.__had_error = True

        except StopIteration as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Settings not found', detail='Problem with BCRA Settings')
            self.__execute_action(function=self.logTxt.write_error, message=e)
            self.__had_error = True
            
        except Exception as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bcra Process', detail='Unknown error')
            self.__execute_action(function=self.logTxt.write_error, message=e)
            self.__had_error = True
        
    def do_sap_procces(self):
        try:
            sap = Sap()
            sap.login(credentials=self.__get_setting_service(SapSetting))
            sap.set_transaction("")
            sap.new_register()
            
        except StopIteration as e:
            self.logXlsx.write_error(message="Settings not found", detail="Problem with SAP Settings")
            self.logTxt.write_error(message=e)
            self.__had_error = True
            
        except Exception as e:
            self.logXlsx.write_error(message="Sap Process", detail="Unknown error")
            self.logTxt.write_error(message=e)
            self.__had_error = True

    def pause(self) -> None:
        self.__notify_status(new_status='PAUSED')
            
    def unpause(self) -> None:
        self.__notify_status(new_status='RUNNING')
        
    def stop(self) -> None:
        self.__notify_status(new_status='CLOSING BOT')
        
    def __execution_begun(self) -> None:
        log_name: str = datetime.now().strftime("%d.%m.%Y_%H%M%S")
        self.__logs_services = [log(name=log_name) for log in self.__logs_services_classes]
        logXlsx: LogXlsx = self.__get_log_service(log_type=LogXlsx)
        logXlsx.write_info(message=f'The Bot has begun')
        self.__notify_status(new_status="RUNNING")
             
    def __execution_completed(self):
        self.__notify_status(new_status="READY")
        logXlsx: LogXlsx = self.__get_log_service(log_type=LogXlsx)
        if(self.__had_error):
            logXlsx.write_error(message=f'The Bot has ended')
        else:
            logXlsx.write_info(message=f'The Bot has ended')
        self.__close_logs()
           
    def __notify_status(self, new_status: str) -> None:
        self.__status = new_status
        logTxt: LogTxt = self.__get_log_service(log_type=LogTxt)
        logTxt.write_info(message=f'Bot {new_status}')
        if self.__status_callback:
            self.__status_callback(new_status)
        
    def __get_log_service(self, log_type: LogService) -> LogService:
        try: return next(log for log in self.__logs_services if isinstance(log, log_type))
        except StopIteration:
            raise ServiceNotFound(f'The log service of type {log_type}, cannot be found')
    
    def __get_setting_service(self, setting_type: SettingService) -> SettingService:
        try: return next(service for service in self.__settings_services if isinstance(service, setting_type))
        except StopIteration:
            raise ServiceNotFound(f'The setting service of type {setting_type}, cannot be found')
        
    def __execute_action(self, function, **kwargs):
        logTxt: LogTxt = self.__get_log_service(log_type=LogTxt)
        while self.__status == 'PAUSED':
            if(self.__status=='RUNNING'):
                break
        return logTxt.write_and_execute(function, **kwargs)
    
    def __close_logs(self) -> None:
        for log in self.__logs_services:
            log.close()
    
    def __get_settings_services(self) -> list[SettingService]:
        return [service(bot_name=self.__bot_name) for service in self.__settings_services_classes]
                                
if __name__ == "__main__":
    st = time.time()
    main = Main()
    main.start(sys.argv[1:])
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
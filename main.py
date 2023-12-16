import time
from settings import *
from log import *
from processes.bna import BnaProcess
from processes.bcra import BcraProcess
from processes.sap import Sap

class Main:
    __settings_services: list[SettingService] = []
    __logs_services: list[LogService] = []
    __bot_name = "Price-Recollection"
    __status = "READY"
    __status_callback = None
    
    def __init__(self) -> None:
        for setting in (SettingBot, SettingSap, SettingBNA, SettingBCRA):
            self.__settings_services.append(setting())
            self.callback = None
        
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
        
    def start(self) -> None:
        self.__logs_services = [log() for log in (LogTxt, LogXlsx)]
        self.__notify_status("RUNNING")

        self.logXlsx: LogXlsx = self.__get_log(LogXlsx)
        self.logTxt: LogTxt = self.__get_log(LogTxt)
        
        self.data = {}
        
        self.do_bna_procces()
        self.do_bcra_procces()
        
        print(self.data)
        
        self.close_logs()
        self.__notify_status("READY")
            
    def close_logs(self) -> None:
        for log in self.__logs_services:
            log.close()
        
    def do_bna_procces(self):
        try:
            self.__execute_action(function=self.logTxt.write_info, message='The Bna process has begun')
            self.data['bna'] = {}
            
            settings = self.__execute_action(function=self.__get_setting, setting_type=SettingBNA)

            bna = BnaProcess()
            self.__execute_action(function=bna.open)
            foreign_bills = self.__execute_action(function=bna.get_foreign_bills_for, requests=settings['foreignBills'])            
            foreign_exchanges = self.__execute_action(function=bna.get_foreign_exchanges_for, requests=settings['foreignExchange'])
            self.__execute_action(function=bna.close)
            
            self.data['bna']['foreignBills'] = foreign_bills
            self.data['bna']['foreignExchange'] = foreign_exchanges
            
            self.__execute_action(function=self.logXlsx.write_info, message='Bna Process')
            self.__execute_action(function=self.logTxt.write_info, message='Bna process completed')
            
        except KeyError as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bna Process', detail='Key error')
            self.__execute_action(function=self.logTxt.write_error, message=f'Key Error: {e}')
            
        except StopIteration as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bna Process', detail='Problem with BNA Settings')
            self.__execute_action(function=self.logTxt.write_error, message=e)
            
        except Exception as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bna Process', detail='Unknown error')
            self.__execute_action(function=self.logTxt.write_error, message=e)

    def do_bcra_procces(self):
        try:
            self.__execute_action(function=self.logTxt.write_info, message='The Bcra process has begun')
            self.data['bcra'] = {}
            settings = self.__execute_action(function=self.__get_setting, setting_type=SettingBCRA)
            
            bcra = BcraProcess()
            self.__execute_action(function=bcra.open)
            self.__execute_action(function=bcra.go_to_exchange_rate_by_date_section)
            self.__execute_action(function=bcra.set_date_in_calendar, date=settings['date'])
            exchange_rates = self.__execute_action(function=bcra.get_exchange_rates_for, requests=settings["coins"])
            self.__execute_action(function=bcra.close)
            
            self.data['bcra']['exchange_rates'] = exchange_rates
            
            self.__execute_action(function=self.logXlsx.write_info, message='Bcra Process')
            self.__execute_action(function=self.logTxt.write_info, message='Bcra process completed')
            
        except KeyError as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bcra Process', detail='Key error')
            self.__execute_action(function=self.logTxt.write_error, message=f'Key Error: {e}')

        except StopIteration as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Settings not found', detail='Problem with BCRA Settings')
            self.__execute_action(function=self.logTxt.write_error, message=e)
            
        except Exception as e:
            self.__execute_action(function=self.logXlsx.write_error, message='Bcra Process', detail='Unknown error')
            self.__execute_action(function=self.logTxt.write_error, message=e)
        
    def do_sap_procces(self):
        try:
            sap = Sap()
            sap.login(credentials=self.__get_setting(SettingSap))
            sap.set_transaction("")
            sap.new_register()
            
        except StopIteration as e:
            self.logXlsx.write_error(message="Settings not found", detail="Problem with SAP Settings")
            self.logTxt.write_error(message=e)
            
        except Exception as e:
            self.logXlsx.write_error(message="Sap Process", detail="Unknown error")
            self.logTxt.write_error(message=e)

    def pause(self):
        self.__notify_status(new_status='PAUSED')
            
    def unpause(self):
        self.__notify_status(new_status='RUNNING')
        
    def stop(self):
        self.__notify_status(new_status='CLOSING BOT')
        
    def __notify_status(self, new_status: str) -> None:
        self.__status = new_status
        logTxt: LogTxt = self.__get_log(log_type=LogTxt)
        logTxt.write_info(message=f'Bot {new_status}')
        if self.__status_callback:
            self.__status_callback(new_status)
        
    def __get_log(self, log_type: LogService) -> LogService:
        return next(log for log in self.__logs_services if isinstance(log, log_type))
    
    def __get_setting(self, setting_type: SettingService) -> SettingService:
        service = next(service for service in self.__settings_services if isinstance(service, setting_type))
        return service.settings
    
    def __execute_action(self, function, **kargs):
        logTxt: LogTxt = self.__get_log(log_type=LogTxt)
        if(self.__status == 'PAUSED'):
            while True:
                if(self.__status=='RUNNING'):
                    break
        elif(self.__status == 'RUNNING'):
            return logTxt.write_and_execute(function, **kargs)
    

if __name__ == "__main__":
    st = time.time()
    main = Main()
    main.start()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

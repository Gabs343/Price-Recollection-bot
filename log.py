import os
import logging
import pandas as pd
from datetime import datetime

class LogService:
    def create() -> None: raise NotImplementedError
    def write_info(message: str) -> None: raise NotImplementedError
    def write_error() -> None: raise NotImplementedError
    def close() -> None: raise NotImplementedError
    
    def create_folder(self, path: str) -> None:
        if(not os.path.exists(path)):
            os.makedirs(path)
    
class LogTxt(LogService):
    def __init__(self) -> None:
        super().__init__()
        self.__path: str = f'{os.path.dirname(os.path.abspath(__file__))}\\logs\\logsTxt'
        self.__name: str = f'Log-{datetime.now().strftime("%d.%m.%Y_%H%M%S")}'
        self.__logger: logging.Logger = None
        self.create_folder(path=self.__path)
        self.create()
            
    def create(self) -> None:
        logger_file: str = f'{self.__path}\\{self.__name}.txt'
        formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler: logging.FileHandler = logging.FileHandler(logger_file)
        
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)
        
    def write_info(self, message: str) -> None:
        self.__logger.info(message)
        
    def write_and_execute(self, function, **kargs):
        some_data = None
        self.write_info(message=f'executing function: {function.__name__} with arguments: {kargs}')
        some_data = function(**kargs)
        self.write_info(message=f'function: {function.__name__} finished')
        return some_data
        
    def write_error(self, message: str, detail: str = None) -> None:
        self.__logger.critical(f'{message} - {detail}')

    def close(self) -> None:
        for handler in self.__logger.handlers[:]:
            self.__logger.removeHandler(handler)
            handler.close()
            
    def __str__(self) -> str:
        return "Log Txt"
            
class LogXlsx(LogService):
    def __init__(self) -> None:
        super().__init__()
        self.__path: str = f'{os.path.dirname(os.path.abspath(__file__))}\\logs\\logsXlsx'
        self.__name: str = f'Log-{datetime.now().strftime("%d.%m.%Y_%H%M%S")}'
        self.__row: int = 1
        self.__log: dict = {}
        self.create_folder(path=self.__path)
        self.create()
            
    def create(self, columns: list[str] = None) -> None:
        log_columns: list[str] = ["Time", "Title", "Status", "Detail"]
        if(columns):
            log_columns.extend(columns)
        self.__log = dict.fromkeys(log_columns)
        
        for key in self.__log.keys():
            self.__log[key] = {}
        
    def write_info(self, message: str) -> None:
        self.__log["Time"][self.__row] = datetime.now().strftime("%H:%M:%S")
        self.__log["Title"][self.__row] = message
        self.__log["Status"][self.__row] = "OK"
        self.__row += 1
        
    def write_error(self, message: str, detail: str = None) -> None:
        self.__log["Time"][self.__row] = datetime.now().strftime("%H:%M:%S")
        self.__log["Title"][self.__row] = message
        self.__log["Detail"][self.__row] = detail
        self.__log["Status"][self.__row] = "ERROR"
        self.__row += 1
        
    def write_in_column(self, column: str, message: str):
        self.__log[column][self.__row] = message
        
    def close(self):
        dataframe = pd.DataFrame.from_dict(self.__log, orient="index").T
        dataframe.to_excel(f'{self.__path}\\{self.__name}.xlsx')
        
    def __str__(self) -> str:
        return "Log Xlsx"
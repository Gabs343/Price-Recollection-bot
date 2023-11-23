from datetime import datetime
import logging
import pandas as pd
import os

class Log:
    def create(): raise NotImplementedError
    def write_info(): raise NotImplementedError
    def write_error(): raise NotImplementedError
    def close(): raise NotImplementedError

class LogTxt(Log):
    def __init__(self, name: str) -> None:
        self.__path = '.\\logs\\logsText'
        self.__name = name
        self.__logger = None
        
        if(not os.path.exists(self.__path)):
            os.makedirs(self.__path)
            
    def create(self) -> None:
        logger_file = f'{self.__path}\\{self.__name}.txt'
        self.__logger = logging.getLogger(self.__name)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(logger_file)
        self.__logger.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)
        
    def write_info(self, message: str) -> None:
        self.__logger.info(message)
        
    def write_and_execute(self, function, *args):
        some_data = None
        if(args): 
            self.write_info(message=f'executing function: {function.__name__} with arguments: {args}')
            some_data = function(args[0])
        else:
            self.write_info(message=f'executing function: {function.__name__} with no arguments: {args}') 
            some_data = function()
        self.write_info(message=f'function: {function.__name__} finished')
        return some_data
        
    def write_error(self, message: str) -> None:
        self.__logger.critical(message)

    def close(self) -> None:
        for handler in self.__logger.handlers[:]:
            self.__logger.removeHandler(handler)
            handler.close()
            
class LogXlsx(Log):
    def __init__(self, name: str) -> None:
        self.__path = '.\\logs\\logsXlsx'
        self.__name = name
        self.__row = 1
        if(not os.path.exists(self.__path)):
            os.makedirs(self.__path)
            
    def create(self, columns: list[str] = None) -> None:
        log_columns = ["Time", "Title", "Status", "Detail"]
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
        
    def write_error(self, message: str, detail: str) -> None:
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
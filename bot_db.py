import sqlite3
import ast

class BotDB:
    
    def __init__(self, bot_name: str) -> None:
        self.__bot_name: str = bot_name
    
    def connect(self) -> None:
        self.connection = sqlite3.connect(f'{self.__bot_name}.bd')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        
    def create(self) -> None: raise NotImplementedError
    def __insert(self) -> None: raise NotImplementedError
    def get(self) -> dict: raise NotImplementedError
    def update(self, data: dict) -> None: raise NotImplementedError

class SettingTable(BotDB):
    def __init__(self, bot_name: str, setting_name: str, settings: dict) -> None:
        super().__init__(bot_name=bot_name)
        self.__setting_table: str = setting_name
        self.__settings: dict = settings 
    
    def create(self) -> None:
        self.connect()

        columns: str = ''
        for key, value in self.__settings.items():
            column_type: str = ''
            if(type(value) is int):
                column_type = 'INTEGER'
            elif(type(value) is float):
                column_type = 'REAL'
            elif(type(value) is bool):
                column_type = 'NUMERIC'
            else:
                column_type = 'TEXT'
  
            columns += f'{key} {column_type} NOT NULL,'
        
        query: str = f'''CREATE TABLE IF NOT EXISTS {self.__setting_table} ({columns[:-1]});'''
                
        self.cursor.execute(query)
        
        self.connection.commit()
        self.connection.close()
        
        if(not self.get()): self.__insert() 
    
    def __insert(self) -> None:
        self.connect()
        keys: list[str] = self.__settings.keys()
        items: list[str] = ['?'] * len(keys)
        
        for key, value in self.__settings.items():
            if(type(value) is list or 
               type(value) is tuple or 
               type(value) is dict):
                self.__settings[key] = str(value)
            
        query = f'''INSERT INTO {self.__setting_table} ({','.join(keys)}) VALUES ({','.join(items)})'''
        self.cursor.execute(query, tuple(self.__settings.values()))
        self.connection.commit()
        self.connection.close()
    
    def get(self) -> dict:
        self.connect()
        query = f'SELECT * FROM {self.__setting_table} WHERE ROWID = 1'
        data = self.cursor.execute(query).fetchone()
        self.connection.commit()
        self.connection.close()
             
        if(data != None):
            data = dict(data)
        
            for key, value in data.items():
                if(type(value) is str):
                    if('{' == value[0] and '}' == value[:-1]):
                        data[key] = ast.literal_eval(value)
                    elif('[' == value[0] and ']' == value[:-1]):
                        data[key] = ast.literal_eval(value)
                    elif('(' == value[0] and ')' == value[:-1]):
                        data[key] = ast.literal_eval(value)
            return data
        else: return dict() 
    
    def update(self, data: dict) -> None:
        self.connect()
        
        columns = ''
        for key in self.__settings.keys():
            columns += f'{key} = ?,'
            
        query = f'''UPDATE {self.__setting_table} SET {columns[:-1]} WHERE ROWID = 1'''
        self.cursor.execute(query, tuple(data.values()))
        
        self.connection.commit()
        self.connection.close()
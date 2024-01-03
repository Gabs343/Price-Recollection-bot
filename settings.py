import subprocess
from bot_db import *

class SettingService:
    def __init__(self):
        self.__settings: dict = {}

    @property
    def settings(self) -> dict:
        return self.__settings
        
    @settings.setter
    def settings(self, setting) -> None:
        self.__settings = setting

class BotSetting(SettingService):
    
    __repository: SettingTable
    
    def __init__(self, bot_name: str) -> None:
        super().__init__()
        self.settings = self.get_new_settings()
        self.__repository = SettingTable(bot_name=bot_name, 
                                         setting_name=self.__str__(),
                                         settings=self.settings)
        self.__repository.create()
        self.settings = self.__repository.get()
        
        self.settings = self.__repository.get()
        
    def get_new_settings(self) -> dict:
        settings: dict = dict.fromkeys(['executions', 'good_executions', 'bad_executions'], 0)
        return settings
        
    def update(self) -> None:
        self.__repository.update(data=self.settings)
        
    def __str__(self) -> str:
        return type(self).__name__
    
class TaskManagerSetting(SettingService):
    
    __repository: SettingTable
    
    def __init__(self, bot_name: str):
        super().__init__()
        self.settings = self.get_new_settings()
        self.__repository = SettingTable(bot_name=bot_name, 
                                         setting_name=self.__str__(),
                                         settings=self.settings)
        self.__repository.create()
        self.settings = self.__repository.get()
        
    def get_new_settings(self) -> dict:
        setting: dict = dict.fromkeys(['task_name'])
        setting['task_name'] = 'None'
        setting['start_time'] = 'None'
        return setting
    
    def update(self) -> None:
        self.__repository.update(data=self.settings)
        
    def __get_python_path(self) -> str:
        command: str = 'where python'
        return subprocess.run(command, 
                              shell=True, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE).stdout.decode("utf-8").strip()
        
    def __task_exists(self) -> bool:
        command: str = f'schtasks /query /tn {self.settings["task_name"]}'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    
    def create_scheduled_task(self) -> str:
        if (self.__task_exists()):
            return f'Task "{self.settings["task_name"]}" already exists. Please choose a different name.'
        else:
            task_run: str = f'cmd /c cd {self.__get_path()} && {self.__get_python_path()} main.py'
            command: str = f'schtasks /create /sc daily /tn {self.settings["task_name"]} /tr "{task_run}" /st {self.settings["start_time"]}'
            subprocess.run(command, shell=True)
            return f'Scheduled task "{self.settings["task_name"]}" created successfully.'
        
    def edit_scheduled_task(self) -> str:
        if (self.__task_exists()):
            task_run: str = f'cmd /c cd {self.__get_path()} && {self.__get_python_path()} main.py'
            command: str = f'schtasks /change /tn {self.settings["task_name"]} /tr "{task_run}" /st {self.settings["start_time"]}'
            subprocess.run(command, shell=True)
            return f'Scheduled task "{self.settings["task_name"]}" edited successfully.'
        else:
            return f'Task {self.settings["task_name"]} does not exist. Cannot edit.'
            
    def delete_scheduled_task(self) -> str:
        if (self.__task_exists()):
            command: str = f'schtasks /delete /tn {self.settings["task_name"]} /f'
            subprocess.run(command, shell=True)
            return f'Scheduled task "{self.settings["task_name"]}" deleted successfully.'
        else:
            return f'Task "{self.settings["task_name"]}" does not exist. Cannot delete.'

    
    def __str__(self) -> str:
        return type(self).__name__
    
class SapSetting(SettingService):
    
    __repository: SettingTable
    
    def __init__(self, bot_name: str) -> None:
        super().__init__()
        self.settings = self.get_new_settings()
        self.__repository = SettingTable(bot_name=bot_name, 
                                         setting_name=self.__str__(),
                                         settings=self.settings)
        self.__repository.create()
        self.settings = self.__repository.get()
        
    def get_new_settings(self) -> dict:
        settings: dict = dict.fromkeys(["user", "password", "client", "language", "connection"], 'None')
        return settings
    
    def update(self) -> None:
        self.__repository.update(data=self.settings)
        
    def __str__(self) -> str:
        return type(self).__name__


class BNASetting(SettingService):
    
    __repository: SettingTable
    
    def __init__(self, bot_name: str) -> None:
        super().__init__()
        self.settings = self.get_new_settings()
        self.__repository = SettingTable(bot_name=bot_name, 
                                         setting_name=self.__str__(),
                                         settings=self.settings)
        self.__repository.create()
        self.settings = self.__repository.get()
        
    def get_new_settings(self) -> dict:
        settings: dict = dict.fromkeys(['foreignBills', 'foreignExchange'])
        settings['foreignBills'] = ['Euro', 'Real *']
        settings['foreignExchange'] = ['Dolar U.S.A', 'Libra Esterlina', 'Euro']
        return settings

    def update(self) -> None:
        self.__repository.update(data=self.settings)
        
    def __str__(self) -> str:
        return type(self).__name__

    
class BCRASetting(SettingService):
    
    __repository: SettingTable
    
    def __init__(self, bot_name: str) -> None:
        super().__init__()
        self.settings = self.get_new_settings()
        self.__repository = SettingTable(bot_name=bot_name, 
                                         setting_name=self.__str__(),
                                         settings=self.settings)
        self.__repository.create()
        self.settings = self.__repository.get()
        
    def get_new_settings(self) -> dict:
        settings: dict = dict.fromkeys(["coins", "date"])
        settings["date"] = "15-08-2023"
        settings["coins"] = ["Bolívar Venezolano", "Franco Suizo", "Libra Esterlina"]
        return settings

    def update(self) -> None:
        self.__repository.update(data=self.settings)
        
    def __str__(self) -> str:
        return type(self).__name__
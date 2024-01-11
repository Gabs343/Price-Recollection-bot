import subprocess

class SettingService:
    def __init__(self):
        self.__settings: dict = {}

    @property
    def settings(self) -> dict:
        return self.__settings
        
    @settings.setter
    def settings(self, setting) -> None:
        self.__settings = setting
    
class SapSetting(SettingService):
    
    def __init__(self, bot_name: str) -> None:
        super().__init__()
        self.settings = self.get_new_settings()
        
    def get_new_settings(self) -> dict:
        settings: dict = dict.fromkeys(["user", "password", "client", "language", "connection"], 'None')
        return settings
        
    def __str__(self) -> str:
        return type(self).__name__


class BNASetting(SettingService):
    
    def __init__(self, bot_name: str) -> None:
        super().__init__()
        self.settings = self.get_new_settings()
        
    def get_new_settings(self) -> dict:
        settings: dict = dict.fromkeys(['foreignBills', 'foreignExchange'])
        settings['foreignBills'] = ['Euro', 'Real *']
        settings['foreignExchange'] = ['Dolar U.S.A', 'Libra Esterlina', 'Euro']
        return settings
        
    def __str__(self) -> str:
        return type(self).__name__

    
class BCRASetting(SettingService):
    
    def __init__(self, bot_name: str) -> None:
        super().__init__()
        self.settings = self.get_new_settings()
        
    def get_new_settings(self) -> dict:
        settings: dict = dict.fromkeys(["coins", "date"])
        settings["date"] = "15-08-2023"
        settings["coins"] = ["Bolívar Venezolano", "Franco Suizo", "Libra Esterlina"]
        return settings
        
    def __str__(self) -> str:
        return type(self).__name__
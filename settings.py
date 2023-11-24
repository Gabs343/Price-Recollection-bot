class SettingService: pass
    
class SettingSap(SettingService):
    
    def __init__(self) -> None:
        super().__init__()
        self.__settings = dict.fromkeys(["user", "password", "client", "language", "connection"])
    
    @property
    def settings(self) -> dict:
        return self.__settings
    
    @settings.setter
    def settings(self, setting: dict) -> None:
        self.__settings = setting
        
    def __str__(self) -> str:
        return "Setting sap"

class SettingBNA(SettingService):
    def __init__(self) -> None:
        super().__init__()
        self.__settings = dict.fromkeys(["foreignBills", "foreignExchange"])
        self.__settings["foreignBills"] = ["Euro", "Real *"]
        self.__settings["foreignExchange"] = ["Dolar U.S.A", "Libra Esterlina", "Euro"]

    @property
    def settings(self) -> dict:
        return self.__settings
    
    @settings.setter
    def settings(self, setting: dict) -> None:
        self.__settings = setting
    
    def __str__(self) -> str:
        return "Setting BNA"
    
class SettingBCRA(SettingService):
    def __init__(self) -> None:
        super().__init__()
        self.__settings = dict.fromkeys(["coins", "date"])
        self.__settings["date"] = "15-08-2023"
        self.__settings["coins"] = ["Bolívar Venezolano", "Franco Suizo", "Libra Esterlina"]

    @property
    def settings(self) -> dict:
        return self.__settings
    
    @settings.setter
    def settings(self, setting: dict) -> None:
        self.__settings = setting
    
    def __str__(self) -> str:
        return "Setting BCRA"
    
class SettingBot(SettingService):
    def __init__(self) -> None:
        super().__init__()
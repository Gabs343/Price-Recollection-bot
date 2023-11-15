class SettingService: pass
    
class SettingSap(SettingService):
    
    def __init__(self) -> None:
        self.__settings = dict.fromkeys(["key1"])
    
    @property
    def settings(self) -> dict:
        return self.__settings
    
    @settings.setter
    def settings(self, setting) -> None:
        self.__settings = setting
        
    def __str__(self) -> str:
        return "Setting sap"

class SettingBNA(SettingService):
    def __init__(self) -> None:
        self.__settings = dict.fromkeys(["key1"])

    @property
    def settings(self) -> dict:
        return self.__settings
    
    @settings.setter
    def settings(self, setting) -> None:
        self.__settings = setting
    
    def __str__(self) -> str:
        return "Setting BNA"
    
class SettingBCRA(SettingService):
    def __init__(self) -> None:
        self.__settings = dict.fromkeys(["key1"])

    @property
    def settings(self) -> dict:
        return self.__settings
    
    @settings.setter
    def settings(self, setting) -> None:
        self.__settings = setting
    
    def __str__(self) -> str:
        return "Setting BNA"
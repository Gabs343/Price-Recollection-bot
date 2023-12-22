import os
import subprocess
import win32com.client
import time

class Sap:
    def __init__(self) -> None:
        self.__APP_PATH: str = os.path.join(os.environ['ProgramFiles(x86)'], '\\SAP\\FrontEnd\\SAPgui\\saplogon.exe')
        self.__process = None
        self.__session = None
        self.__wait: int = 1
        self.__pages: int = 1
        
    def login(self, credentials: dict) -> None:
        connection = self.__open_connection(connection=credentials["connection"])

        self._session = connection.Children(0)
        if(type(self.session) != win32com.client.CDispatch):
            self.__process.kill()
            raise Exception("Problem in getting the session")

        self.__session.findById("wnd[0]/usr/txtRSYST-BNAME").text = credentials["user"]
        self.__session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = credentials["password"]
        self.__session.findById("wnd[0]/usr/txtRSYST-MANDT").text = credentials["client"]
        self.__session.findById("wnd[0]/usr/txtRSYST-LANGU").text = credentials["language"]
        self.__session.findById("wnd[0]").sendVKey(0) 
        self.__session.findById("wnd[0]").sendVKey(0)
        
    def set_transaction(self, transaction: str) -> None:
        self.__session.findById("wnd[0]/tbar[0]/okcd").text = transaction
        self.__session.findById("wnd[0]").sendVKey(0)
        time.sleep(self.__wait)
        
    def go_to_main(self) -> None:
        self.go_back(loop=self.__pages)
        self.page = 1
        
    def go_back(self, loop: int = 1) -> None:
        for i in range(loop):
            self.__session.findById("wnd[0]/tbar[0]/btn[15]").press()
            
    def logout(self) -> None:
        self.go_to_main()
        self.__session.findById("wnd[1]/usr/btnSPOP-OPTION1").press()
        
    def new_register(self) -> None:
        self.__session.findById("wnd[0]/tbar[1]/btn[5]").press()
  
    def __open_connection(self, connection: str) -> win32com.client.CDispatch:
        self.__process = subprocess.Popen(self.__APP_PATH)

        time.sleep(4)

        sap_gui = win32com.client.GetObject("SAPGUI")
        if(type(sap_gui) != win32com.client.CDispatch):
            self.__process.kill()
            raise Exception("Problem in getting the SAPGUI object")
        
        app = sap_gui.GetScriptingEngine
        if(type(app) != win32com.client.CDispatch):
            self.__process.kill()
            raise Exception("Problem in getting the scripting Engine")
        
        connection = app.OpenConnection(connection, True)
        if(type(connection) != win32com.client.CDispatch):
            self.__process.kill()
            raise Exception(f'Cannot connect with {connection}')
        
        return connection
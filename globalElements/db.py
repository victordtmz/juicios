import sqlite3
import os
from globalElements import constants

class main:
    def __init__(self) -> None:
        
        self.define_global()

    def define_global(self):
        self.database = 'registros.avd'
        self.tbl_registros = 'registros'
        # self.tbl_detalles = 'detalles'
        # self.OneDrive = os.path.expanduser('~\OneDrive')
        self.OneDrive = constants.ROOT_ENLACE
        self.expediente = []

    def connect(self):
        #expediente (Tipo, Juicio, Activo)
        if self.expediente:
            database = f'{self.OneDrive}\{self.expediente[2]}\{self.expediente[0]}\{self.expediente[1]}\desgloce\\registros.avd'
        # print(database)
            try: 
                self.connection = sqlite3.connect(database)
            except: 
                os.mkdir(f'{self.OneDrive}\{self.expediente[2]}\{self.expediente[0]}\{self.expediente[1]}\desgloce')
                self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()

    def execute(self, sql:str, var:list='', close:bool=True):
        self.connect()
        if var:
            self.cursor.execute(sql, var)
        else:
            self.cursor.execute(sql)
        if close:
            self.connection.close()

    def save(self, sql:str, var=''):
        self.execute(sql, var, False)
        self.connection.close()
        return self.cursor.lastrowid
        


    def select(self, sql:str):
        self.connect()
        records = self.cursor.execute(sql)
        records = records.fetchall()
        self.connection.close()
        return records

    def evaluate_save_record(self, up):
        pass
    # self.create_registros_table = f'''
    #     --sql
    #     CREATE TABLE IF NOT EXISTS {self.tbl_registros} (
    #         id INTEGER PRIMARY KEY,
    #         date_ TEXT,
    #         title TEXT,
    #         description_ TEXT,
    #         file_ TEXT
    #         );'''
    
    
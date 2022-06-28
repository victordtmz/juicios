import sqlite3
import os
from typing import Iterable

class main:
    def __init__(self) -> None:
        self.define_global()

    def define_global(self):
        self.database = 'registros.avd'
        self.tbl_registros = 'registros'
        self.tbl_detalles = 'detalles'
        self.OneDrive = os.path.expanduser('~\OneDrive')
        self.expediente = []


    
        self.create_registros_table = f'''
        --sql
        CREATE TABLE IF NOT EXISTS {self.tbl_registros} (
            id INTEGER PRIMARY KEY,
            date_ TEXT,
            title TEXT,
            description_ TEXT,
            file_ TEXT
            );'''

        self.create_detalles_table = f'''
        --sql
        CREATE TABLE IF NOT EXISTS {self.tbl_detalles} (
            id INTEGER PRIMARY KEY,
            cliente TEXT,
            expediente TEXT,
            fecha_ TEXT,
            honorarios_ REAL,
            telefono TEXT,
            domicilio TEXT,
            domicilio1 TEXT,
            ciudad TEXT,
            estado TEXT,
            cp TEXT,
            descripcion TEXT
            );
        '''
        
        
        

    def connect(self):
        #expediente (Tipo, Juicio, Activo)
        if self.expediente:
            database = f'{self.OneDrive}\enlace\{self.expediente[2]}\{self.expediente[0]}\{self.expediente[1]}\desgloce\\registros.avd'
        # print(database)
            try: 
                self.connection = sqlite3.connect(database)
            except: 
                os.mkdir(f'{self.OneDrive}\enlace\{self.expediente[2]}\{self.expediente[0]}\{self.expediente[1]}\desgloce')
                self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()

    def execute(self, sql:str):
        self.connect()
        self.cursor.execute(sql)
        self.connection.close()

    def select(self, sql:str):
        self.connect()
        records = self.cursor.execute(sql)
        records = records.fetchall()
        self.connection.close()
        return records
    
    def select_detalles(self):
        sql = f''' --sql
        SELECT * FROM {self.tbl_detalles};''' 
        try: 
            record = self.select(sql)[0]
            return record
            
        except: 
            pass
            # self.execute(self.create_detalles_table)
            # record = self.select(sql)[0] 
        # return record
    def save_detalles(self, detalles):
        print(detalles)

        
    

    




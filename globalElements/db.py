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

    def select_dict(self, sql:str):
        self.connect()
        record = self.cursor.execute(sql)
        record = record.fetchall()
        record = self.dict_factory(self.cursor.description, record)
        return record


    def dict_factory(self, description, records):
        all_records = []
        for r in records:
            curr_record = {}
            for index, column in enumerate(description):
                curr_record[column[0]] = r[index]
            all_records.append(curr_record)
        return all_records

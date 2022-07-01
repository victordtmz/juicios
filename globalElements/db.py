import sqlite3
import os
from globalElements import constants

class main:
    def __init__(self) -> None:
        
        self.define_global()

    def define_global(self):
        self.root = constants.ROOT_ENLACE
        self.expediente = []

    def connect(self):
        #expediente (Tipo, Juicio, Activo)
        if self.expediente:
            database = f'{self.root}\{self.expediente[2]}\{self.expediente[0]}\{self.expediente[1]}\desgloce\\registros.avd'
            try: 
                self.connection = sqlite3.connect(database)
            except: 
                os.mkdir(f'{self.root}\{self.expediente[2]}\{self.expediente[0]}\{self.expediente[1]}\desgloce')
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

    def select_labels(self, sql:str):
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

    def select_dict_labels(self, sql):
        self.connect()
        records = self.cursor.execute(sql)
        records = records.fetchall()
        labelsInfo = self.cursor.description
        self.connection.close()
        labels = []
        for label in labelsInfo:
            labels.append(label[0])
        return (records, labels)

    def dict_factory(self, description, records):
        all_records = []
        for r in records:
            curr_record = {}
            for index, column in enumerate(description):
                curr_record[column[0]] = r[index]
            all_records.append(curr_record)
        return all_records

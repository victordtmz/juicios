import sqlite3
import os
from typing import Iterable
from globalElements import db

class main(db.main):
    def __init__(self) -> None:
        super().__init__()

        self.create_table = f'''
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
    
    def select_detalles(self):
        sql = f''' --sql
        SELECT * FROM {self.tbl_detalles};''' 
        try: 
            record = self.select(sql)[0]
            return record
            
        except: 
            pass
            
    def save_detalles(self, detalles):
        print(detalles) 
        if detalles[0]:
            #edit existing record.
            print('Editing')
        else: 
            #Create new record. 
            print('New Record')

    def evaluate_save_record(self, up):
        return super().evaluate_save_record(up) 
        
    

    




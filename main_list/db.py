import sqlite3
import os
from typing import Iterable
from globalElements import db

class main(db.main):
    def __init__(self) -> None:
        super().__init__()
        self.table = 'detalles'

        self.create_table = f'''
        --sql
        CREATE TABLE IF NOT EXISTS {self.table} (
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
        SELECT * FROM {self.table};''' 
        try: 
            record = self.select(sql)[0]
            return record
            
        except: 
            pass
            
    def save_detalles(self, r):
        print(r) 
        

        if r[0]:
            #edit def savexisting record.
            sql = f'''
            --sql
            UPDATE {self.table} SET
            cliente = '{r[1]}',
            expediente = '{r[2]}',
            fecha_ = '{r[3]}',
            honorarios_ = '{r[4]}',
            telefono = '{r[5]}',
            domicilio = '{r[6]}',
            domicilio1 = '{r[7]}',
            ciudad = '{r[8]}',
            estado = '{r[9]}',
            cp = '{r[10]}',
            descripcion = '{r[11]}'
            WHERE id = ?;
            '''
            self.save(sql, (r[0],))
            return 'Record edits saved succesfully', None
        else: 
            #Create new record. 
            self.execute(self.create_table)
            values = list(r)
            values.pop(0)
            values = str(values).replace('[', '')
            values = values.replace(']', '')
            
            sql = f'''
            --sql
            INSERT INTO {self.table} (cliente, expediente,
                fecha_, honorarios_, telefono, domicilio,
                domicilio1, ciudad, estado, cp, descripcion)
            VALUES ({values});
            '''
            id = self.save(sql)
            return 'New record saved succesfully', id


    def evaluate_save_record(self, up):
        return super().evaluate_save_record(up) 
        
    

    




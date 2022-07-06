from select import select
from shelve import DbfilenameShelf
import sqlite3
import os
from this import s
from xml.dom.pulldom import default_bufsize
from globalElements import constants

class juiciosDB:
    def __init__(self) -> None:
        pass
        self.db_root = ''
        # self._db_folder = f'{self.db_root}\desgloce'
        # self._db = f'{self._db_folder}\\registros.avd'
    
    def set_db(self, db_root):
        self.db_root = db_root
        self._db_folder = f'{db_root}\desgloce'
        self._db = f'{self._db_folder}\\registros.avd'

    def connect(self):
        if not self.db_root:
            return
        try: 
            self.connection = sqlite3.connect(self._db)
        except: 
            os.mkdir(self._db_folder)
            self.connection = sqlite3.connect(self._db)
        self.cursor = self.connection.cursor()
        

    def select_dict(self, select_sql:str):
        self.connect()
        record = self.cursor.execute(select_sql)
        record = record.fetchall()
        record = self.dict_records(self.cursor.description, record)
        self.connection.close()
        return record

    def select_one_dict(self, select_sql:str):
        self.connect()
        record = self.cursor.execute(select_sql)
        record = record.fetchone()
        if record:
            record = self.dict_record(self.cursor.description, record)
            self.connection.close()
            return record
        else: return

    
    def dict_records(self, description, records):
        all_records = []
        for r in records:
            curr_record = self.dict_record(description,r)
            # for index, column in enumerate(description):
            #     curr_record[column[0]] = r[index]
            all_records.append(curr_record)
        return all_records

    def dict_record(self, description, record):
        curr_record = {}
        for index, column in enumerate(description):
            curr_record[column[0]] = record[index]
        return curr_record


#g!  DETALLES - MAIN LIST
#g! --------------------------------------------------------------- 
    #TODO: DO NOT DELETE - SAMPLE CODE FOR DB WITH LIST
    # def select_detalles_custom_headers(self):
    #     a = '''--sql'''
    #     sql = f'''
    #     SELECT   
    #         id,
    #         cliente AS 'Cliente',
    #         expediente AS 'Expediente',
    #         fecha_ AS 'Fecha',
    #         honorarios_ AS 'Honorarios',
    #         telefono AS 'Teléfono',
    #         domicilio AS 'Domicilio',
    #         domicilio1 AS 'Domicilio 2',
    #         ciudad AS 'Ciudad',
    #         estado AS 'Estado',
    #         cp AS 'CP',
    #         descripcion AS 'Descripción'
    #         FROM detalles;
    #     '''
    #     record = self.select_dict(sql)
    #     return record

    def select_detalles(self):
        a = '''--sql'''
        sql = f'''SELECT * FROM detalles;'''
        record = self.select_one_dict(sql)
        return record

    def create_table_detalles(self): #MAIN LIST
        a = '''--sql'''
        sql = f'''
        CREATE TABLE IF NOT EXISTS detalles (
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
        self.connect()
        self.cursor.execute(sql)
        self.connection.close()

    def update_record_detalles(self, record:dict):
        a = '''--sql'''
        sql = f'''
        UPDATE detalles SET 
            cliente = '{record['cliente']}',
            expediente = '{record['expediente']}',
            fecha_ = '{record['fecha_']}',
            honorarios_ = '{record['honorarios_']}',
            telefono = '{record['telefono']}',
            domicilio = '{record['domicilio']}',
            domicilio1 = '{record['domicilio1']}',
            ciudad = '{record['ciudad']}',
            estado = '{record['estado']}',
            cp = '{record['cp']}',
            descripcion = '{record['descripcion']}'
            WHERE id = '{record['id']}';
        '''
        self.connect()
        self.cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def insert_record_detalles(self, record:dict):
        a = '''--sql'''
        sql = f'''
        INSERT INTO detalles 
            (cliente, expediente, fecha_, 
            honorarios_, telefono, domicilio,
            domicilio1, ciudad, estado, 
            cp, descripcion)
            VALUES
            ('{record['cliente']}','{record['expediente']}', '{record['fecha_']}',
            '{record['honorarios_']}', '{record['telefono']}', '{record['domicilio']}',
            '{record['domicilio1']}',  '{record['ciudad']}', '{record['estado']}',
            '{record['cp']}', '{record['descripcion']}') ;'''
        self.connect()
        self.cursor.execute(sql)
        self.connection.commit()
        id_ = self.cursor.lastrowid
        self.connection.close()
        return id_


#g!  REGISTROS 
#g! --------------------------------------------------------------- 
    def create_table_registros(self):
        a = '''--sql'''
        sql = f'''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY,
            date_ TEXT,
            title TEXT,
            description_ TEXT,
            file_ TEXT
            );
        '''
        self.connect()
        self.cursor.execute(sql)
        self.connection.close()

    def select_registros_custom_headers(self):
        a = '''--sql'''
        sql = f'''
        SELECT id, 
            date_ AS 'Fecha',
            title AS 'Titulo', 
            description_ AS 'Descripcion', 
            file_ AS 'Archivo'
        FROM registros;
        '''
        record = self.select_dict(sql)
        return record

    def delete_record_registros(self, id_):
        a = '''--sql'''
        sql = '''
        DELETE FROM registros WHERE id = ?;'''
        self.connect()
        self.cursor.execute(sql, (id_,))
        self.connection.commit()
        self.connection.close()

    def insert_record_registros(self, record:dict):
        a = '''--sql'''
        sql = f'''
        INSERT INTO registros 
            (date_, title, description_, file_)
            VALUES
            ('{record['date_']}','{record['title']}', '{record['description_']}','{record['file_']}') ;'''
        self.connect()
        self.cursor.execute(sql)
        self.connection.commit()
        id_ = self.cursor.lastrowid
        self.connection.close()
        return id_

    def update_record_registros(self, record:dict):
        a = '''--sql'''
        sql = f'''
        UPDATE registros SET 
            date_ = '{record['date_']}',
            title = '{record['title']}',
            description_ = '{record['description_']}',
            file_ = '{record['file_']}'
            WHERE id = '{record['id']}';
        '''
        self.connect()
        self.cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    
        

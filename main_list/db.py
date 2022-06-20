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
        

    def connect(self, expediente: Iterable):
        #expediente (Tipo, Juicio, Activo)
        database = f'{database}\enlace\{expediente[2]}\{expediente[0]}\{expediente[1]}\desgloce\\registros.avd'
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    

    




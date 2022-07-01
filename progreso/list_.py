
from PyQt6.QtCore import Qt
from globalElements.models import list

class main(list.main):
    """treeview list with search box
        Args:
            db (sqlite3 db): Database must be instantiated in main and passed to list when oppened. 
        """
    def __init__(self, db):
        super().__init__(db)
        
    def sql_select(self)->str:
        """Returns:
            str: sql to select data from table
        """
        sql = '''
        --sql
        SELECT id, 
            date_ AS 'Fecha',
            title AS 'Titulo', 
            description_ AS 'Descripcion', 
            file_ AS 'Archivo'
        FROM registros;
        '''
        return sql

        
    def configure_list_after_requery(self):
        self.list.setColumnHidden(0, True)
        self.list.setColumnHidden(3, True)
        self.list.setColumnHidden(4, True)
        self.proxy_search.sort(1, Qt.SortOrder.DescendingOrder)
        
    
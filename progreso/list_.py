
from PyQt6.QtCore import Qt
from globalElements.models import list

class main(list.main):
    """treeview list with search box
        Args:
            db (sqlite3 db): Database must be instantiated in main and passed to list when oppened. 
        """
    def __init__(self, db_folder):
        super().__init__()
        self._db_folder = db_folder
        self.db.set_db(self._db_folder)
        
        
    def configure_list_after_requery(self):
        self.list.setColumnHidden(0, True)
        self.list.setColumnHidden(3, True)
        self.list.setColumnHidden(4, True)
        self.proxy_search.sort(1, Qt.SortOrder.DescendingOrder)

    def select_records(self)->dict:
        """Call the correct function from db to collect records

        Returns:
            dict: Dictinary with column name and values to be added
        """
        return self.db.select_registros_custom_headers()
        
    
import sys
from PyQt6.QtWidgets import (QApplication)
from main_list import main
from main_list import edit_form

 

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    mw = main.main()
    mw.show()
    sys.exit(app.exec())
# print("hello")
import sys
import os
from PyQt6.QtWidgets import (QApplication,  QHBoxLayout, 
    QWidget, QVBoxLayout)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression
from globalElements import constants, functions
from globalElements.widgets.widgets import spacer, buttonWidget, labelWidget, standardItem, titleBox, treeView, checkBox,lineEditFilterGroup
# import mainList



class main(QWidget):
    """

    Args:
        QMainWindow (QtWidgget): QtWidget item
    """
    def __init__(self):
        super().__init__()
    
    def __repr__(self) -> str:
        return '''Main Window => Juicios y Trámites'''
    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())


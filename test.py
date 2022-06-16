import sys
from globalElements.widgets.lineEdits import lineEdit
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QWidget, QVBoxLayout)

# edit = lineEdit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = lineEdit()
    print('Hellow World')
    print(mw)
    print(mw.__doc__)
    # mw.show()
    # sys.exit(app.exec())
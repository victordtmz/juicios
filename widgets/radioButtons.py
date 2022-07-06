from PyQt6.QtWidgets import QGroupBox, QRadioButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class activoRadioButtons(QGroupBox):
    def __init__(self, fontSize:int = 12):
        super().__init__()
        font = QFont('Calibri', fontSize,500)
        self.setFont(font)
        self.setTitle('Archivado:')
        self.archivado = QRadioButton('Archivado')
        self.activo = QRadioButton('Activo')
        
        self.layout_ = QHBoxLayout()
        self.setLayout(self.layout_)

        self.layout_.addWidget(self.activo)
        self.layout_.addWidget(self.archivado)

    def getInfo(self):
        if self.activo.isChecked():
            return 'Juicios'
        else: 
            return 'Juicios_archivados'

    def populate(self, text):
        if text == 'Juicios_archivados':
            self.archivado.setChecked(True)
        else:
            self.activo.setChecked(True)
        

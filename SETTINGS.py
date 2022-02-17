import sys
from PyQt5.QtWidgets import QWidget, QRadioButton, QApplication, QPushButton, QMessageBox, QButtonGroup, QGridLayout, QLabel

class SETTINGS(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        self.setLayout(grid)

        self.OUTPUT_FORMAT=QLabel("输出形式：")
        self.math_output = QRadioButton('数学输出',self)
        self.digit_output = QRadioButton('小数输出',self)
        self.digit_output.setChecked(True)
        self.output_format = QButtonGroup(self)
        self.output_format.addButton(self.math_output, 11)
        self.output_format.addButton(self.digit_output, 12)
        grid.addWidget(self.OUTPUT_FORMAT,0,0)
        grid.addWidget(self.math_output,0,1)
        grid.addWidget(self.digit_output,0,2)
        self.digit_output.toggled.connect(self.output_toggled)

        self.ANGLE=QLabel("角度单位：")
        self.rad = QRadioButton('弧度',self)
        self.rad.setChecked(True)
        self.deg = QRadioButton('角度',self)
        self.angle = QButtonGroup(self)
        self.angle.addButton(self.rad, 21)
        self.angle.addButton(self.deg, 22)
        grid.addWidget(self.ANGLE,1,0)
        grid.addWidget(self.rad,1,1)
        grid.addWidget(self.deg,1,2)
        self.rad.toggled.connect(self.angle_toggled)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('设置')    

        self.sym=False
        self.ang="rad"
    
    def output_toggled(self):
            self.sym=False if self.digit_output.isChecked() else True
            # print(self.sym)

    def angle_toggled(self):
            self.ang="rad" if self.rad.isChecked() else "deg"
            # print(self.ang)
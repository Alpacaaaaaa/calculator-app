'''
本文件中定义SETTINGS类，是calculator界面"设置"选项卡弹窗的实现
'''
import sys
from PyQt5.QtWidgets import QWidget, QRadioButton, QButtonGroup, QGridLayout, QLabel, QSpinBox,QPushButton
from PyQt5.QtGui import QColor, QPalette
class SETTINGS(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        self.setLayout(grid)

        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(250,250,250))
        self.setPalette(self.palette)

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

        digit_num = QLabel('有效位数：')
        self.dig_num = QSpinBox()
        self.dig_num.setRange(2,8)
        self.dig_num.setValue(4)
        self.dig_num.setSingleStep(1)
        grid.addWidget(digit_num,2,0)
        grid.addWidget(self.dig_num,2,1)
        self.setWindowTitle('设置')

        self.sym=False
        self.ang="rad"
        self.dig=4

        confirm = QPushButton('确定')
        confirm.clicked.connect(self.conf)
        grid.addWidget(confirm,3,2)
    
    def conf(self):
            self.sym = False if self.digit_output.isChecked() else True
            self.ang = "rad" if self.rad.isChecked() else "deg"
            self.dig = self.dig_num.value()
            self.close()
import numpy as np
import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont

class expression(): #表达式类，用来计算一个形如(a ± b */ c)的表达式的值。
    def __init__(self):
        self.res=0
        self.prev_sym=""
        self.prev_num=0
        self.curr_num=0
        self.curr_sym=""
        self.curr_num_text=""
#利用栈结构来
EXP=expression()
CAL=[]
CAL.append(EXP)

def ERROR_INPUT():
    return None

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.restart=True


    def initUI(self):
        
        grid = QGridLayout()
        self.setLayout(grid)

        self.names = ['Cls', 'Bck', '(', ')', '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '=', '+']
        self.operators = ['(', ')', '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '+', '=']

        positions = [(i+20,j) for i in range(5) for j in range(4)]
        
        for position, name in zip(positions, self.names):
            
            if name == '':
                continue
            button=QPushButton(name,self)
            if name in self.operators:
                button.setShortcut(name)
            
            button.clicked.connect(self.INPUT)
            grid.addWidget(button, *position)

        self.exp=""
        self.label_exp = QLabel(self.exp, self)
        grid.addWidget(self.label_exp, 0, 0, 1, 4)
        self.label_exp.setAlignment(Qt.AlignRight)

        
        self.label_ans = QLabel(self)
        grid.addWidget(self.label_ans, 10, 0, 1, 4)
        self.label_ans.setAlignment(Qt.AlignRight)

        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()

    def INPUT(self):
        global CAL
        if self.restart:
            CAL.clear()
            EXP=expression()
            CAL.append(EXP)
            self.restart=False
            self.exp=""
        
        sender=self.sender().text()
        if sender == "Cls":
            self.restart=True
            self.label_exp.setText("")
            self.label_ans.setText("")

        elif sender in self.operators:
            self.exp=self.exp+sender
            self.restart=False

            if sender=="(":
                temp=expression()
                CAL.append(temp)

            elif sender.isdigit() or sender == '.':
                CAL[-1].curr_num_text+=sender

            elif (sender=="+" or sender=="-" or sender==")" or sender=="="):
                if CAL[-1].curr_num_text!="":
                    CAL[-1].curr_num=float(CAL[-1].curr_num_text)
                sgn=-1 if (CAL[-1].prev_sym=="-") else 1
                if (CAL[-1].curr_sym==""):
                    CAL[-1].res+=CAL[-1].curr_num*sgn

                elif (CAL[-1].curr_sym=="*"):
                    CAL[-1].res=CAL[-1].res+sgn*CAL[-1].curr_num*CAL[-1].prev_num

                elif (CAL[-1].curr_sym=="/"):
                    CAL[-1].res=CAL[-1].res+sgn*CAL[-1].prev_num/CAL[-1].curr_num

                CAL[-1].prev_sym=sender
                CAL[-1].curr_sym=""
                CAL[-1].prev_num=CAL[-1].curr_num=0
                CAL[-1].curr_num_text=""

                if sender == "=":
                    self.restart=True
                elif sender ==")":
                    ans=CAL[-1].res
                    CAL.pop()
                    CAL[-1].curr_num=ans

            elif (sender=="*" or sender=="/"):
                if CAL[-1].curr_num_text!="":
                    CAL[-1].curr_num=float(CAL[-1].curr_num_text)
                if CAL[-1].prev_num==0:
                    CAL[-1].prev_num=CAL[-1].curr_num

                else:
                    if (CAL[-1].curr_sym=="*"):
                        CAL[-1].prev_num=CAL[-1].prev_num*CAL[-1].curr_num
                    elif (CAL[-1].curr_sym=="/"):
                        CAL[-1].prev_num=CAL[-1].prev_num/CAL[-1].curr_num
                CAL[-1].curr_sym=sender
                CAL[-1].curr_num=0
                CAL[-1].curr_num_text=""
            
            self.label_exp.setFont(QFont("Roman Times", *(12,50) if self.restart else (16,75)))
            self.label_exp.setText(self.exp)
            self.label_ans.setFont(QFont("Roman Times", *(16,75) if self.restart else (12,50)))
            self.label_ans.setText("{0}".format(CAL[0].res))
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

import sys
from math import tan, cos, sin, sqrt, log, asin, acos, atan, pi, e

import numpy as np
from io import BytesIO

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSvg import QSvgWidget

from sympy import init_printing

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(231, 175)
        self.function_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.function_lineEdit.setGeometry(QtCore.QRect(100, 30, 113, 20))
        self.function_lineEdit.setObjectName("function_lineEdit")
        self.maximum_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.maximum_lineEdit.setGeometry(QtCore.QRect(100, 60, 113, 20))
        self.maximum_lineEdit.setObjectName("maximum_lineEdit")
        self.minimum_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.minimum_lineEdit.setGeometry(QtCore.QRect(100, 90, 113, 20))
        self.minimum_lineEdit.setObjectName("minimum_lineEdit")
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setGeometry(QtCore.QRect(140, 130, 75, 23))
        self.cancel_button.setObjectName("cancel_button")
        self.ok_button = QtWidgets.QPushButton(Dialog)
        self.ok_button.setGeometry(QtCore.QRect(20, 130, 75, 23))
        self.ok_button.setObjectName("ok_button")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 51, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 90, 71, 16))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.add_functions()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.cancel_button.setText(_translate("Dialog", "Exit"))
        self.ok_button.setText(_translate("Dialog", "OK"))
        self.label.setText(_translate("Dialog", "Function:"))
        self.label_2.setText(_translate("Dialog", "Maximum X:"))
        self.label_3.setText(_translate("Dialog", "Minimum X:"))

    def add_functions(self):
        self.cancel_button.clicked.connect(close_app)
        self.ok_button.clicked.connect(lambda: build_graph(self.function_lineEdit.text(), self.minimum_lineEdit.text(), self.maximum_lineEdit.text()))


def build_graph(function, minimum, maximum):
    global graph, ui
    # print(function, minimum, maximum)
    function = function.replace('ctg(', '-tg(pi/2+').replace('^', '**').replace('tg', 'tan').replace('ln', 'log').replace('arcsin', 'asin').replace('arccos', 'acos').replace('arctan', 'atan').replace('arctg', 'atan')
    print(function)
    try:
        minimum = eval(minimum)
        ui.minimum_lineEdit.setText(str(minimum))
    except Exception:
        ui.minimum_lineEdit.setText("Error.")
        return
    try:
        maximum = eval(maximum)
        ui.maximum_lineEdit.setText(str(maximum))
    except Exception:
        ui.maximum_lineEdit.setText("Error.")
        return
    # print(np.linspace(minimum, maximum, 10))
    try:
        graph.build_plot(function, minimum, maximum)
    except Exception:
        ui.function_lineEdit.setText("Error.")
    # print(function, minimum, maximum)


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        self.left = 0
        self.bottom = 0
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        self.axes = ax
        super(MplCanvas, self).__init__(fig)

    def change_axis(self, left=None, bottom=None):
        if left is not None:
            self.left = left
        if bottom is not None:
            self.bottom = bottom
        self.axes.spines['left'].set_position(('data', self.left))
        self.axes.spines['bottom'].set_position(('data', self.bottom))


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.

    def build_plot(self, function, mn, mx):
        sc = MplCanvas()
        print(111, mn, mx, function)
        x = np.linspace(mn, mx, 10000)
        print(x)
        y = []
        mny, mxy = None, None
        mnx, mxx = None, None
        for el in x:
            print(el, end=' ')
            try:
                value = eval(function.replace('x', '(' + str(el) + ')'))
                # print(value)
                assert type(value) != complex
                y.append(value)
                mny = min(mny, y[-1]) if mny is not None else y[-1]
                mxy = max(mxy, y[-1]) if mxy is not None else y[-1]
                mnx = min(mnx, el) if mnx is not None else el
                mxx = max(mxx, el) if mxx is not None else el
            except Exception:
                y.append(None)
        # y = [eval(function.replace('x', str(el))) for el in x]
        print(y)
        if type(y) == int:
            y = np.linspace(y, y, 100)
        # print(x)
        # print(y)
        print(mny, mxy)
        print(mnx, mxx)
        if 0 < mnx or mxx < 0:
            sc.change_axis(left=mnx)
            print("XXX")
        if 0 < mny or mxy < 0:
            sc.change_axis(bottom=mny)
            print("YYY")
        sc.axes.plot(x, y)
        self.setCentralWidget(sc)
        self.show()


def close_app():
    sys.exit()


def tex2svg(formula, fontsize=12, dpi=300):
    """Render TeX formula to SVG.
    Args:
        formula (str): TeX formula.
        fontsize (int, optional): Font size.
        dpi (int, optional): DPI.
    Returns:
        str: SVG render.
    """

    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize)

    output = BytesIO()
    fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                bbox_inches='tight', pad_inches=0.0)
    plt.close(fig)

    output.seek(0)
    return output.read()


def draw_tex(formula):
    svg = QSvgWidget()
    svg.load(tex2svg(formula))
    svg.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    graph = MainWindow()
    Dialog.show()
    # draw_tex(r"\int \sqrt{\frac{1}{x}}\, dx")
    app.exec_()
    sys.exit()

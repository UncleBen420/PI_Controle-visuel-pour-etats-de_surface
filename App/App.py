# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'App.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import sys
import numpy as np
import qwt

from Model import Model
from ImageGetter import ImageGetter


class GUI_Model_Interface:

    def __init__(self, GUI, image_getter, default_image, model):
        self.GUI = GUI
        self.image_getter = image_getter
        self.default_image = default_image
        self.model = model

    def setImage(self, image):
        image_box = self.GUI.RaVisualisation
        qpixmap = QPixmap(image)
        image_box.setPixmap(qpixmap)

    def analyse(self):
        print(self.GUI.comboBox.currentText())
        self.current_image = self.image_getter.getImage()

        pix = QtGui.QPixmap.fromImage(qwt.toqimage.array_to_qimage(self.current_image))

        image_box = self.GUI.RaVisualisation
        qpixmap = QPixmap(pix)
        image_box.setPixmap(qpixmap)

        self.predictions = self.model.predict(self.current_image)
        self.GUI.textBox.setText(self.predictions)

class Ui_RaAnalyse(object):
    def setupUi(self, RaAnalyse):
        RaAnalyse.setObjectName("RaAnalyse")
        RaAnalyse.resize(800, 425)
        self.centralwidget = QtWidgets.QWidget(RaAnalyse)
        self.centralwidget.setObjectName("centralwidget")
        self.RaVisualisation = QtWidgets.QLabel(self.centralwidget)
        self.RaVisualisation.setGeometry(QtCore.QRect(420, 10, 361, 361))
        self.RaVisualisation.setObjectName("Ra_visualisation")
        self.RaVisualisation.setScaledContents(True)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 100, 281, 51))
        self.pushButton.setObjectName("pushButton_start_analyse")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 60, 211, 21))
        self.comboBox.setObjectName("comboBox_exposition_time")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 30, 181, 17))
        self.label.setObjectName("label_exposition_time")
        self.textBox = QtWidgets.QLineEdit(self.centralwidget)
        self.textBox.setGeometry(QtCore.QRect(50, 170, 331, 192))
        self.textBox.setObjectName("Analysis summary")
        RaAnalyse.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RaAnalyse)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        RaAnalyse.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RaAnalyse)
        self.statusbar.setObjectName("statusbar")
        RaAnalyse.setStatusBar(self.statusbar)

        self.retranslateUi(RaAnalyse)
        QtCore.QMetaObject.connectSlotsByName(RaAnalyse)

    def retranslateUi(self, RaAnalyse):
        _translate = QtCore.QCoreApplication.translate
        RaAnalyse.setWindowTitle(_translate("RaAnalyse", "RaAnalysis"))
        self.pushButton.setText(_translate("RaAnalyse", "Analyse"))
        self.comboBox.setItemText(0, _translate("RaAnalyse", "100"))
        self.comboBox.setItemText(1, _translate("RaAnalyse", "300"))
        self.comboBox.setItemText(2, _translate("RaAnalyse", "600"))
        self.label.setText(_translate("RaAnalyse", "Expostion Time (ms)"))
        self.textBox.setText("")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    RaAnalyse = QtWidgets.QMainWindow()

    ui = Ui_RaAnalyse()

    ui.setupUi(RaAnalyse)
    RaAnalyse.show()

    dig = ImageGetter()
    dm = Model()

    GMI = GUI_Model_Interface(ui, dig, "HES_SO.jpg", dm)
    GMI.setImage(GMI.default_image)
    GMI.setImage("logo-he-arc.svg")
    ui.pushButton.pressed.connect(GMI.analyse)

    sys.exit(app.exec_())

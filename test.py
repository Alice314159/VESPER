# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

sign_list = [">","<","==",">=","<="]
conditon_list = []

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(584, 1980)
        self.BuyConditon1 = QtWidgets.QComboBox(Form)
        self.BuyConditon1.setGeometry(QtCore.QRect(30, 50, 201, 41))
        self.BuyConditon1.setObjectName("BuyConditon1")
        self.BuyConditon1.addItem("")
        self.BuyConditon1.addItem("")
        self.BuyConditon1.addItem("")
        self.BuyConditon1.addItem("")
        self.BuyConditon1.addItem("")
        self.BuyConditon1.addItem("")
        self.BuyConditon1.addItem("")
        self.buySign1 = QtWidgets.QComboBox(Form)
        self.buySign1.setGeometry(QtCore.QRect(260, 50, 121, 41))
        self.buySign1.setObjectName("buySign1")
        self.buySign1.addItem("")
        self.buySign1.addItem("")
        self.buySign1.addItem("")
        self.buySign1.addItem("")
        self.buySign1.addItem("")
        self.buySign1.addItem("")
        self.buyThresh1 = QtWidgets.QLineEdit(Form)
        self.buyThresh1.setGeometry(QtCore.QRect(430, 50, 113, 41))
        self.buyThresh1.setObjectName("buyThresh1")
        self.buySign2 = QtWidgets.QComboBox(Form)
        self.buySign2.setGeometry(QtCore.QRect(260, 150, 121, 41))
        self.buySign2.setObjectName("buySign2")
        self.buySign2.addItem("")
        self.buySign2.addItem("")
        self.buySign2.addItem("")
        self.buySign2.addItem("")
        self.buySign2.addItem("")
        self.buySign2.addItem("")
        self.buyThresh2 = QtWidgets.QLineEdit(Form)
        self.buyThresh2.setGeometry(QtCore.QRect(430, 150, 113, 41))
        self.buyThresh2.setObjectName("buyThresh2")
        self.BuyConditon2 = QtWidgets.QComboBox(Form)
        self.BuyConditon2.setGeometry(QtCore.QRect(30, 150, 201, 41))
        self.BuyConditon2.setObjectName("BuyConditon2")
        self.BuyConditon2.addItem("")
        self.BuyConditon2.addItem("")
        self.BuyConditon2.addItem("")
        self.BuyConditon2.addItem("")
        self.BuyConditon2.addItem("")
        self.BuyConditon2.addItem("")
        self.BuyConditon2.addItem("")
        self.BuyConditon3 = QtWidgets.QComboBox(Form)
        self.BuyConditon3.setGeometry(QtCore.QRect(30, 230, 201, 41))
        self.BuyConditon3.setObjectName("BuyConditon3")
        self.BuyConditon3.addItem("")
        self.BuyConditon3.addItem("")
        self.BuyConditon3.addItem("")
        self.BuyConditon3.addItem("")
        self.BuyConditon3.addItem("")
        self.BuyConditon3.addItem("")
        self.BuyConditon3.addItem("")
        self.buySign3 = QtWidgets.QComboBox(Form)
        self.buySign3.setGeometry(QtCore.QRect(260, 230, 121, 41))
        self.buySign3.setObjectName("buySign3")
        self.buySign3.addItem("")
        self.buySign3.addItem("")
        self.buySign3.addItem("")
        self.buySign3.addItem("")
        self.buySign3.addItem("")
        self.buySign3.addItem("")
        self.buyThresh3 = QtWidgets.QLineEdit(Form)
        self.buyThresh3.setGeometry(QtCore.QRect(430, 230, 113, 41))
        self.buyThresh3.setObjectName("buyThresh3")
        self.buySign4 = QtWidgets.QComboBox(Form)
        self.buySign4.setGeometry(QtCore.QRect(260, 310, 121, 41))
        self.buySign4.setObjectName("buySign4")
        self.buySign4.addItem("")
        self.buySign4.addItem("")
        self.buySign4.addItem("")
        self.buySign4.addItem("")
        self.buySign4.addItem("")
        self.buySign4.addItem("")
        self.buyThresh4 = QtWidgets.QLineEdit(Form)
        self.buyThresh4.setGeometry(QtCore.QRect(430, 310, 113, 41))
        self.buyThresh4.setObjectName("buyThresh4")
        self.BuyConditon4 = QtWidgets.QComboBox(Form)
        self.BuyConditon4.setGeometry(QtCore.QRect(30, 310, 201, 41))
        self.BuyConditon4.setObjectName("BuyConditon4")
        self.BuyConditon4.addItem("")
        self.BuyConditon4.addItem("")
        self.BuyConditon4.addItem("")
        self.BuyConditon4.addItem("")
        self.BuyConditon4.addItem("")
        self.BuyConditon4.addItem("")
        self.BuyConditon4.addItem("")
        self.buyParam = QtWidgets.QGroupBox(Form)
        self.buyParam.setEnabled(False)
        self.buyParam.setGeometry(QtCore.QRect(10, 10, 541, 1951))
        self.buyParam.setObjectName("buyParam")
        self.comboBox = QtWidgets.QComboBox(self.buyParam)
        self.comboBox.setGeometry(QtCore.QRect(20, 390, 201, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(Form)
        self.BuyConditon2.activated['int'].connect(self.BuyConditon2.setCurrentIndex)
        self.buyParam.clicked.connect(self.buyParam.update)
        self.comboBox.activated['int'].connect(self.comboBox.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.BuyConditon1.setItemText(0, _translate("Form", "20日均线"))
        self.BuyConditon1.setItemText(1, _translate("Form", "当日J线"))
        self.BuyConditon1.setItemText(2, _translate("Form", "当日收盘价"))
        self.BuyConditon1.setItemText(3, _translate("Form", "当日开盘价"))
        self.BuyConditon1.setItemText(4, _translate("Form", "当日最高价"))
        self.BuyConditon1.setItemText(5, _translate("Form", "当日最低价"))
        self.BuyConditon1.setItemText(6, _translate("Form", "十日内收盘最高价"))
        self.buySign1.setItemText(0, _translate("Form", "大于"))
        self.buySign1.setItemText(1, _translate("Form", "大于等于"))
        self.buySign1.setItemText(2, _translate("Form", "小于"))
        self.buySign1.setItemText(3, _translate("Form", "小于等于"))
        self.buySign1.setItemText(4, _translate("Form", "等于"))
        self.buySign1.setItemText(5, _translate("Form", "不等于"))
        self.buySign2.setItemText(0, _translate("Form", "大于"))
        self.buySign2.setItemText(1, _translate("Form", "大于等于"))
        self.buySign2.setItemText(2, _translate("Form", "小于"))
        self.buySign2.setItemText(3, _translate("Form", "小于等于"))
        self.buySign2.setItemText(4, _translate("Form", "等于"))
        self.buySign2.setItemText(5, _translate("Form", "不等于"))
        self.BuyConditon2.setItemText(0, _translate("Form", "60日均线"))
        self.BuyConditon2.setItemText(1, _translate("Form", "当日J线"))
        self.BuyConditon2.setItemText(2, _translate("Form", "当日收盘价"))
        self.BuyConditon2.setItemText(3, _translate("Form", "当日开盘价"))
        self.BuyConditon2.setItemText(4, _translate("Form", "当日最高价"))
        self.BuyConditon2.setItemText(5, _translate("Form", "当日最低价"))
        self.BuyConditon2.setItemText(6, _translate("Form", "十日内收盘最高价"))
        self.BuyConditon3.setItemText(0, _translate("Form", "20日均线"))
        self.BuyConditon3.setItemText(1, _translate("Form", "当日J线"))
        self.BuyConditon3.setItemText(2, _translate("Form", "当日收盘价"))
        self.BuyConditon3.setItemText(3, _translate("Form", "当日开盘价"))
        self.BuyConditon3.setItemText(4, _translate("Form", "当日最高价"))
        self.BuyConditon3.setItemText(5, _translate("Form", "当日最低价"))
        self.BuyConditon3.setItemText(6, _translate("Form", "十日内收盘最高价"))
        self.buySign3.setItemText(0, _translate("Form", "大于"))
        self.buySign3.setItemText(1, _translate("Form", "大于等于"))
        self.buySign3.setItemText(2, _translate("Form", "小于"))
        self.buySign3.setItemText(3, _translate("Form", "小于等于"))
        self.buySign3.setItemText(4, _translate("Form", "等于"))
        self.buySign3.setItemText(5, _translate("Form", "不等于"))
        self.buySign4.setItemText(0, _translate("Form", "大于"))
        self.buySign4.setItemText(1, _translate("Form", "大于等于"))
        self.buySign4.setItemText(2, _translate("Form", "小于"))
        self.buySign4.setItemText(3, _translate("Form", "小于等于"))
        self.buySign4.setItemText(4, _translate("Form", "等于"))
        self.buySign4.setItemText(5, _translate("Form", "不等于"))
        self.BuyConditon4.setItemText(0, _translate("Form", "20日均线"))
        self.BuyConditon4.setItemText(1, _translate("Form", "当日J线"))
        self.BuyConditon4.setItemText(2, _translate("Form", "当日收盘价"))
        self.BuyConditon4.setItemText(3, _translate("Form", "当日开盘价"))
        self.BuyConditon4.setItemText(4, _translate("Form", "当日最高价"))
        self.BuyConditon4.setItemText(5, _translate("Form", "当日最低价"))
        self.BuyConditon4.setItemText(6, _translate("Form", "十日内收盘最高价"))
        self.buyParam.setTitle(_translate("Form", "买入参数设置"))
        self.comboBox.setItemText(0, _translate("Form", "20日线"))
        self.comboBox.setItemText(1, _translate("Form", "最新收盘价"))

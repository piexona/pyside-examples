# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gotocelldialog.ui'
#
# Created: Wed Apr 15 01:49:08 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_GoToCellDialog(object):
    def setupUi(self, GoToCellDialog):
        GoToCellDialog.setObjectName("GoToCellDialog")
        GoToCellDialog.resize(254, 71)
        self.verticalLayout = QtGui.QVBoxLayout(GoToCellDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(GoToCellDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(GoToCellDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(GoToCellDialog)
        self.okButton.setEnabled(False)
        self.okButton.setDefault(True)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_2.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(GoToCellDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label.setBuddy(self.lineEdit)

        self.retranslateUi(GoToCellDialog)
        QtCore.QMetaObject.connectSlotsByName(GoToCellDialog)
        GoToCellDialog.setTabOrder(self.lineEdit, self.okButton)
        GoToCellDialog.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, GoToCellDialog):
        GoToCellDialog.setWindowTitle(QtGui.QApplication.translate("GoToCellDialog", "Go to Cell", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GoToCellDialog", "&Cell Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("GoToCellDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("GoToCellDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gotocelldialog2.ui'
#
# Created: Sat Apr 18 12:37:13 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_GoToCellDialog(object):
    def setupUi(self, GoToCellDialog):
        GoToCellDialog.setObjectName("GoToCellDialog")
        GoToCellDialog.resize(254, 69)
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
        self.buttonBox = QtGui.QDialogButtonBox(GoToCellDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.lineEdit)

        self.retranslateUi(GoToCellDialog)
        QtCore.QMetaObject.connectSlotsByName(GoToCellDialog)

    def retranslateUi(self, GoToCellDialog):
        GoToCellDialog.setWindowTitle(QtGui.QApplication.translate("GoToCellDialog", "Go to Cell", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GoToCellDialog", "&Cell Location:", None, QtGui.QApplication.UnicodeUTF8))


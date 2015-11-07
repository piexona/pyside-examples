# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui, QtCore

# import subprocess
# cmd = 'C:/Python27/Scripts/pyside-uic.exe -o gotocelldialog2.py gotocelldialog2.ui'
# subprocess.Popen(cmd, stdout=subprocess.PIPE)

from gotocelldialog2 import Ui_GoToCellDialog

class GoToCellDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        self.ui = Ui_GoToCellDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        # [A-Za-z]를 1개, [1-9]를 1개, [0-9]를0개부터2개까지
        regExp = QtCore.QRegExp(r'[A-Za-z][1-9][0-9]{0,2}')
        self.ui.lineEdit.setValidator(QtGui.QRegExpValidator(regExp, self))
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        #print self.ui.verticalLayout

    # 슬롯데코레이터와 on_오브젝트명_시그널명으로 커넥트를 생략할 수 있음
    @QtCore.Slot()
    def on_lineEdit_textChanged(self):
        # 라인에디트의 조건이 딱 맞을때만 OK버튼이 활성화 된다
    	self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(self.ui.lineEdit.hasAcceptableInput())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = GoToCellDialog()
    dialog.show()
    sys.exit(app.exec_())
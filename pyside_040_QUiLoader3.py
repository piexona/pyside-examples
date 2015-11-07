# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui, QtCore

# import subprocess
# cmd = 'C:/Python27/Scripts/pyside-uic.exe -o gotocelldialog.py gotocelldialog.ui'
# subprocess.Popen(cmd, stdout=subprocess.PIPE)
from gotocelldialog import Ui_GoToCellDialog

class GoToCellDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        self.ui = Ui_GoToCellDialog()
        self.ui.setupUi(self)

        regExp = QtCore.QRegExp(r'[A-Za-z][1-9][0-9]{0,2}')
        self.ui.lineEdit.setValidator(QtGui.QRegExpValidator(regExp, self))

        self.ui.okButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)

        print self.ui.verticalLayout

    # 슬롯데코레이터와 on_오브젝트명_시그널명으로 커넥트를 생략할 수 있음
    # PyQt에서는 QtCore.pyqtSlot()을 사용.
    @QtCore.Slot()
    def on_lineEdit_textChanged(self):
    	self.ui.okButton.setEnabled(self.ui.lineEdit.hasAcceptableInput())



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = GoToCellDialog()
    dialog.show()
    sys.exit(app.exec_())
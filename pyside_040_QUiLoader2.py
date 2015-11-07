# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui

# import subprocess
# cmd = 'C:/Python27/Scripts/pyside-uic.exe -o gotocelldialog.py gotocelldialog.ui'
# subprocess.Popen(cmd, stdout=subprocess.PIPE)
from gotocelldialog import Ui_GoToCellDialog

class GoToCellDialog(QtGui.QDialog, Ui_GoToCellDialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)
        self.setupUi(self)
        print self.verticalLayout


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = GoToCellDialog()
    dialog.show()
    sys.exit(app.exec_())
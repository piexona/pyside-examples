# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui
from PySide.QtUiTools import QUiLoader

class GoToCellDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        loader = QUiLoader()
        self.ui = loader.load('gotocelldialog.ui', self)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        # 자식 위젯 취득하기 1
        print self.ui.verticalLayout.objectName()
        # 자식 위젯 취득하기 2 (타입명, 오브젝트명)
        print self.ui.findChild(QtGui.QPushButton, 'cancelButton').objectName()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    dialog = GoToCellDialog()
    dialog.show()
    sys.exit(app.exec_())
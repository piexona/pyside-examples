# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui, QtCore

# import subprocess
# cmd = 'C:/Python27/Scripts/pyside-uic.exe -o sortdialog.py sortdialog.ui'
# subprocess.Popen(cmd, stdout=subprocess.PIPE)
from sortdialog import Ui_SortDialog

class SortDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        self.ui = Ui_SortDialog()
        self.ui.setupUi(self)
        self.ui.secondaryGroupBox.hide()
        self.ui.tertiaryGroupBox.hide()
        # 폼의 레이아웃에 대한 sizeConstraint속성을 QLayout.SetFixedSize로 설정해,
        # 사용자가 다이얼로그의 크기를 변경할 수 없게 만든다.
        # 레이아웃은 다이얼로그의 크기 조절에 대한 모든 책임을 넘겨받으며,
        # 자식 위젯들이 보이거나 숨겨질 때 다이얼로그가 항상 최적의 크기로 표시될 수
        # 있도록 자동으로 다이얼로그의 크기를 조절하게 된다.
        self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)

        self.setColumnRange('C', 'F')

    @QtCore.Slot(bool)
    def on_moreButton_toggled(self, checked):
        if checked:
            self.ui.moreButton.setText('Advenced <<<')
        else:
            self.ui.moreButton.setText('Advenced >>>')
            
    def setColumnRange(self, first, last):
        self.ui.primaryColumnCombo.clear()
        self.ui.secondaryColumnCombo.clear()
        self.ui.tertiaryColumnCombo.clear()

        self.ui.secondaryColumnCombo.addItem(self.tr('None'))
        self.ui.tertiaryColumnCombo.addItem(self.tr('None'))
        # primaryColumnCombo는 다른 콤보박스보다 작을 수 있기 때문에, 사이즈를 맞춰 주었다.
        self.ui.primaryColumnCombo.setMinimumSize(self.ui.secondaryColumnCombo.sizeHint())

        ch = first
        while ch <= last:
            self.ui.primaryColumnCombo.addItem(ch)
            self.ui.secondaryColumnCombo.addItem(ch)
            self.ui.tertiaryColumnCombo.addItem(ch)
            ch = chr( ord(ch)+1 )

    def comparisonObject(self):
        return


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = SortDialog()
    dialog.show()
    sys.exit(app.exec_())
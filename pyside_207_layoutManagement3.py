# coding: utf-8
from PySide import QtGui


class Dialog(QtGui.QWidget):
    u"""Layout Manager"""
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent=parent)
        self.namedLabel = QtGui.QLabel('Named:')
        self.namedLineEdit = QtGui.QLineEdit()
        self.subFoldersCheckBox = QtGui.QCheckBox('Include subfolders')
        self.leftLayout = QtGui.QGridLayout()
        self.leftLayout.addWidget(self.namedLabel, 0, 0)
        self.leftLayout.addWidget(self.namedLineEdit, 0, 1)
        # QGridLayoutの場合、addWidgetの引数は
        # addWidget(widget, row, column, rowSpan, columnSpan)になる
        self.leftLayout.addWidget(self.subFoldersCheckBox, 1, 0, 1, 2)
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        self.setLayout(self.mainLayout)

        self.setWindowTitle(self.tr('Find files or folders'))


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
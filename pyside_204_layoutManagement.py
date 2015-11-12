# coding: utf-8
from PySide import QtGui


class Dialog(QtGui.QWidget):
    u"""absolute positioning"""
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent=parent)
        namedLabel = QtGui.QLabel('Named:', parent=self)
        namedLabel.setGeometry(9, 9, 50, 25)
        namedLineEdit = QtGui.QLineEdit(parent=self)
        namedLineEdit.setGeometry(65, 9, 200, 25)
        self.setFixedSize(365, 240)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
# coding: utf-8
from PySide import QtGui


class Dialog(QtGui.QWidget):
    u"""Manual positioning"""
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent=parent)
        self.namedLabel = QtGui.QLabel('Named:', parent=self)
        self.namedLineEdit = QtGui.QLineEdit(parent=self)
        self.setMinimumSize( 265, 190)
        self.resize(365, 240)

    def resizeEvent(self, event):
        extraWidth = self.width() - self.minimumWidth()
        extraHeight = self.height() - self.minimumHeight()

        self.namedLabel.setGeometry(9, 9, 50, 25)
        self.namedLineEdit.setGeometry(65, 9, 100 + extraWidth, 25)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
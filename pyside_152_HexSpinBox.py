# coding: utf-8
# author: wie@ppi.co.jp
import sys
from PySide import QtCore, QtGui

class HexSpinBox(QtGui.QSpinBox):
    def __init__(self, parent=None):
        super(HexSpinBox, self).__init__(parent=parent)
        self.setRange(0, 255)
        self.validator = QtGui.QRegExpValidator(QtCore.QRegExp('[0-9A-Fa-f]{1,8}'), self)
        self.setPrefix('num')

    def validate(self, text, pos):
        ret = self.validator.validate(text, pos)
        print ret
        return ret

    def textFromValue(self, value):
        return str(hex(value)).upper()[2:]

    def valueFromText(self, text):
        try:
            return int(text, 16)
        except:
            return 0


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = HexSpinBox()
    window.show()
    sys.exit(app.exec_())

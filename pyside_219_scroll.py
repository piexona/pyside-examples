# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore
from pyside_156_IconEditor import IconEditor

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    iconEditor = IconEditor()
    scrollArea = QtGui.QScrollArea()
    scrollArea.setWidget(iconEditor)
    scrollArea.viewport().setBackgroundRole(QtGui.QPalette.Dark)
    scrollArea.viewport().setAutoFillBackground(True)
    scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    scrollArea.setWindowTitle(scrollArea.tr('Icon Editor'))
    scrollArea.show()
    sys.exit(app.exec_())
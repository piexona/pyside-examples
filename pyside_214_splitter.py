# coding: utf-8
# author: wie@ppi.co.jp

if __name__ == '__main__':
    import sys
    from PySide import QtGui, QtCore

    app = QtGui.QApplication(sys.argv)

    editor1 = QtGui.QTextEdit()
    editor2 = QtGui.QTextEdit()
    editor3 = QtGui.QTextEdit()

    splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
    splitter.addWidget(editor1)
    splitter.addWidget(editor2)
    splitter.addWidget(editor3)

    splitter.show()
    sys.exit(app.exec_())

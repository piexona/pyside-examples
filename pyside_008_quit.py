# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui, QtCore


def main():
    app = QtGui.QApplication(sys.argv)
    button = QtGui.QPushButton('Quit')
    # 애플리케이션을 취득하는 세가지 방법
    # app
    # QtGui.qApp
    # QtCore.QCoreApplication.instance()
    button.clicked.connect(QtCore.QCoreApplication.instance().quit)
    button.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

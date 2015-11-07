# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui
from PySide.QtUiTools import QUiLoader

if __name__ == '__main__':

	import sys
	loader = QUiLoader()
	app = QtGui.QApplication(sys.argv)
	widget = loader.load('gotocelldialog.ui')
	widget.show()
	sys.exit(app.exec_())
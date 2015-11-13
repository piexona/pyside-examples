# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore


class MailClient(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MailClient, self).__init__(parent=parent)
        messagesTreeWidget = QtGui.QTreeWidget()
        textEdit = QtGui.QTextEdit()
        self.rightSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.rightSplitter.addWidget(messagesTreeWidget)
        self.rightSplitter.addWidget(textEdit)
        # setStretchFactor 의 인자는 (0에서 부터 시작하는 인덱스명, 스트레치)
        self.rightSplitter.setStretchFactor(1, 1)

        foldersTreeWidget = QtGui.QTreeWidget()
        self.mainSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.mainSplitter.addWidget(foldersTreeWidget)
        self.mainSplitter.addWidget(self.rightSplitter)
        self.mainSplitter.setStretchFactor(1, 1)
        self.setCentralWidget(self.mainSplitter)

        self.setWindowTitle('Mail Client')
        self.readSettings()

    def writeSettings(self):
        settings = QtCore.QSettings('Software Inc.', 'Mail Client')
        settings.beginGroup('mainWindow')
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('mainSplitter', self.mainSplitter.saveState())
        settings.setValue('rightSplitter', self.rightSplitter.saveState())
        settings.endGroup()

    def readSettings(self):
        settings = QtCore.QSettings('Software Inc.', 'Mail Client')
        settings.beginGroup('mainWindow')
        # PySide 에서는 저장된 값이 QByteArray 로 돌아오므로 변환할 필요가 없음
        self.restoreGeometry(settings.value('geometry'))
        self.mainSplitter.restoreState(settings.value('mainSplitter'))
        self.rightSplitter.restoreState(settings.value('rightSplitter'))
        settings.endGroup()

    def closeEvent(self, event):
        self.writeSettings()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = MailClient()
    window.show()
    sys.exit(app.exec_())
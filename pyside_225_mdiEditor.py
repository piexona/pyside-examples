# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore
import mdiEditor_rc

# import subprocess
# cmd = 'C:/Python27/Lib/site-packages/PySide/pyside-rcc.exe -o mdiEditor_rc.py images/mdiEditor.qrc'
# subprocess.Popen(cmd, stdout=subprocess.PIPE)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.mdiArea = QtGui.QMdiArea()
        self.setCentralWidget(self.mdiArea)
        self.mdiArea.subWindowActivated.connect(self.updateActions)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.setWindowIcon(QtGui.QPixmap(':icon.png'))
        self.setWindowTitle(self.tr('MDI Editor'))
        # 이벤트 루프가 유휴상태에 진입하자마자 곧바로 타임아웃
        # 읽어들어야 할 파일이 클 경우 사용자가 프로그램이 죽었다고 생각할 수 있으므로
        # 윈도우를 먼저 표시하고 처리를 진행
        QtCore.QTimer.singleShot(0, self.loadFiles)

        self.readSettings()

    def loadFiles(self):
        # sys.argv 와 같은 값을 받으나,
        # -style 이나 -font 와 같은 Qt 전용의 명령행 옵션은 QApplication 에 의해
        # 자동으로 인자 목록에서 제거됨
        args = QtGui.QApplication.arguments()
        # 프로그램 실행시 함께 받은 인자를 오픈
        # 여기서 몇개를 빼야 할지는 maya, c++ 등 환경에 따라 바뀔 수 있음
        if args[2:]:
            for arg in args[2:]:
                self.openFile(arg)
            self.mdiArea.cascadeSubWindows()
        else:
            self.newFile()
        # 에디터 윈도우를 활성화 하고, 활성화 시그널을 발생시킴
        self.mdiArea.activateNextSubWindow()

    def newFile(self):
        editor = Editor()
        editor.newFile()
        self.addEditor(editor)

    def open(self):
        editor = Editor.open(self)
        if editor:
            self.addEditor(editor)

    def addEditor(self, editor):
        editor.copyAvailable.connect(self.cutAction.setEnabled)
        editor.copyAvailable.connect(self.copyAction.setEnabled)

        subWindow = self.mdiArea.addSubWindow(editor)
        self.windowMenu.addAction(editor.windowMenuAction())
        self.windowActionGroup.addAction(editor.windowMenuAction())
        subWindow.show()

    def save(self):
        pass

    def saveAs(self):
        pass


    def createActions(self):
        self.newAction = QtGui.QAction(self.tr('%New'), self)
        self.newAction.setIcon(QtGui.QIcon(':/new.png'))
        self.newAction.setShortcut(QtGui.QKeySequence.New)
        self.newAction.setStatusTip(self.tr('Create a new file'))
        self.newAction.triggered.connect(self.newFile)

        self.openAction = QtGui.QAction(self.tr('%Open'), self)
        self.openAction.setIcon(QtGui.QIcon(':/open.png'))
        self.openAction.setShortcut(QtGui.QKeySequence.Open)
        self.openAction.setStatusTip(self.tr('Open an existing file'))
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtGui.QAction(self.tr('%Save'), self)
        self.saveAction.setIcon(QtGui.QIcon(':save.png'))
        self.saveAction.setShortcut(QtGui.QKeySequence.Save)
        self.saveAction.setStatusTip(self.tr('Save the file to disk'))
        self.saveAction.triggered.connect(self.save)

        self.saveAsAction = QtGui.QAction(self.tr('Save &As'), self)
        self.saveAsAction.setStatusTip(self.tr('Save the file under a new name'))
        self.saveAsAction.triggered.connect(self.saveAs)

        self.exitAction = QtGui.QAction(self.tr('E&xit'), self)
        self.exitAction.setShortcut(self.tr('Ctrl+Q'))
        self.exitAction.setStatusTip(self.tr('Exit the application'))
        self.exitAction.triggered.connect(self.close)

        self.cutAction = QtGui.QAction(self.tr('Cu&t'), self)

        self.copyAction = QtGui.QAction(self.tr('&Copy'), self)

        self.pasteAction = QtGui.QAction(self.tr('&Paste'), self)

        self.closeAction = QtGui.QAction(self.tr('Cl&ose'), self)

        self.closeAllAction = QtGui.QAction(self.tr('Close &All'), self)

        self.tileAction = QtGui.QAction(self.tr('&Tile'), self)

        self.cascadeAction = QtGui.QAction(self.tr('&Cascade'), self)

        self.nextAction = QtGui.QAction(self.tr('Ne&xt'), self)

        self.previousAction = QtGui.QAction(self.tr('Pre&vious'), self)

        self.separatorAction = QtGui.QAction(self)
        self.separatorAction.setSeparator(True)

        self.aboutAction = QtGui.QAction(self.tr('&About'), self)
        self.aboutAction.setStatusTip(self.tr("Show the Qt library's About box"))

        self.aboutQtAction = QtGui.QAction(self.tr('About &Qt'), self)
        self.aboutQtAction.setStatusTip(self.tr("Show the Qt library's About box"))

        self.windowActionGroup = QtGui.QActionGroup(self)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr('&File'))
        self.editMenu = self.menuBar().addMenu(self.tr('&Edit'))
        self.windowMenu = self.menuBar().addMenu(self.tr('&Window'))
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu(self.tr('&Help'))

    def createToolBars(self):
        pass

    def createStatusBar(self):
        pass

    @QtCore.Slot()
    def updateActions(self):
        print 'updateActions'
        pass

    def writeSettings(self):
        settings = QtCore.QSettings('Software Inc.', 'MDI Editor')
        settings.beginGroup('mainWindow')
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('state', self.saveState())
        settings.endGroup()

    def readSettings(self):
        settings = QtCore.QSettings('Software Inc.', 'MDI Editor')
        settings.beginGroup('mainWindow')
        self.restoreGeometry(settings.value('geometry'))
        self.restoreState(settings.value('state'))
        settings.endGroup()

    def closeEvent(self, event):
        self.writeSettings()
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.subWindowList():
            event.ignore()
        else:
            event.accept()


class Editor(QtGui.QTextEdit):

    def __init__(self, parent=None):
        super(Editor, self).__init__(parent=parent)
        self.action = QtGui.QAction(self)
        self.action.setCheckable(True)
        self.action.triggered.connect(self.show)
        self.action.triggered.connect(self.setFocus)

        self.isUntitled = True

        self.setWindowIcon(QtGui.QPixmap(':/document.png'))
        self.setWindowTitle('[*]')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def windowMenuAction(self):
        return self.action

    def newFile(self):
        pass


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mdiEditor = MainWindow()
    mdiEditor.show()
    sys.exit(app.exec_())
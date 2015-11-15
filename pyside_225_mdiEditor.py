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

    def activeEditor(self):
        subWindow = self.mdiArea.activeSubWindow()
        if subWindow:
            return subWindow.widget()
        return 0

    def addEditor(self, editor):
        editor.copyAvailable.connect(self.cutAction.setEnabled)
        editor.copyAvailable.connect(self.copyAction.setEnabled)

        # addSubWindow 함수는 QMidSubWindow 하나를 생성한 다음, 매개변수로 전달받은
        # 위젯을 이 하위 윈두우에 붙인 뒤, 이 하위 윈도우의 포인터를 리턴한다
        subWindow = self.mdiArea.addSubWindow(editor)
        # 액션은 에디터에 귀속되어 있으므로 에디터가 닫히면 메뉴에서 자동으로 사라진다.
        self.windowMenu.addAction(editor.windowMenuAction())
        self.windowActionGroup.addAction(editor.windowMenuAction())
        subWindow.show()

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

    def save(self):
        if self.activeEditor():
            self.activeEditor().save()

    def saveAs(self):
        if self.activeEditor():
            self.activeEditor().saveAs()

    def copy(self):
        if self.activeEditor():
            self.activeEditor().copy()

    def cut(self):
        if self.activeEditor():
            self.activeEditor().cut()

    def paste(self):
        if self.activeEditor():
            self.activeEditor().paste()

    def about(self):
        pass

    def createActions(self):
        self.newAction = QtGui.QAction(self.tr('&New'), self)
        self.newAction.setIcon(QtGui.QIcon(':/new.png'))
        self.newAction.setShortcut(QtGui.QKeySequence.New)
        self.newAction.setStatusTip(self.tr('Create a new file'))
        self.newAction.triggered.connect(self.newFile)

        self.openAction = QtGui.QAction(self.tr('&Open'), self)
        self.openAction.setIcon(QtGui.QIcon(':/open.png'))
        self.openAction.setShortcut(QtGui.QKeySequence.Open)
        self.openAction.setStatusTip(self.tr('Open an existing file'))
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtGui.QAction(self.tr('&Save'), self)
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
        self.cutAction.setIcon(QtGui.QIcon(':/images/cut.png'))
        self.cutAction.setShortcut(QtGui.QKeySequence.Cut)
        self.setStatusTip(self.tr('Cut the current selection to the clipboard'))
        self.cutAction.triggered.connect(self.cut)

        self.copyAction = QtGui.QAction(self.tr('&Copy'), self)
        self.copyAction.setIcon(QtGui.QIcon(':/images/copy.png'))
        self.copyAction.setShortcut(QtGui.QKeySequence.Cut)
        self.setStatusTip(self.tr('Cut the current selection to the clipboard'))
        self.cutAction.triggered.connect(self.cut)

        self.pasteAction = QtGui.QAction(self.tr('&Paste'), self)
        self.pasteAction.setIcon(QtGui.QIcon(':/images/paste.png'))
        self.pasteAction.setShortcut(QtGui.QKeySequence.Paste)
        self.pasteAction.setStatusTip(self.tr("Paste the clipboard's contents at "
                                              "the cursor position"))
        self.pasteAction.triggered.connect(self.paste)

        self.closeAction = QtGui.QAction(self.tr('Cl&ose'), self)
        self.closeAction.setShortcut(QtGui.QKeySequence.Close)
        self.closeAction.setStatusTip(self.tr('Close the active window'))
        self.closeAction.triggered.connect(self.mdiArea.closeActiveSubWindow)

        self.closeAllAction = QtGui.QAction(self.tr('Close &All'), self)
        self.closeAllAction.setStatusTip(self.tr('Close all the windows'))
        self.closeAllAction.triggered.connect(self.close)

        self.tileAction = QtGui.QAction(self.tr('&Tile'), self)
        self.tileAction.setStatusTip(self.tr('Tile the windows'))
        self.tileAction.triggered.connect(self.mdiArea.tileSubWindows)

        self.cascadeAction = QtGui.QAction(self.tr('&Cascade'), self)
        self.cascadeAction.setStatusTip(self.tr('Cascade the windows'))
        self.cascadeAction.triggered.connect(self.mdiArea.cascadeSubWindows)

        self.nextAction = QtGui.QAction(self.tr('Ne&xt'), self)
        self.nextAction.setShortcut(QtGui.QKeySequence.NextChild)
        self.nextAction.setStatusTip(self.tr('Move the focus to the next window'))
        self.nextAction.triggered.connect(self.mdiArea.activateNextSubWindow)

        self.previousAction = QtGui.QAction(self.tr('Pre&vious'), self)
        self.previousAction.setShortcut(QtGui.QKeySequence.PreviousChild)
        self.previousAction.setStatusTip(self.tr('Move the focus to the previous '
                                                 'window'))
        self.previousAction.triggered.connect(self.mdiArea.activatePreviousSubWindow)

        self.separatorAction = QtGui.QAction(self)
        self.separatorAction.setSeparator(True)

        self.aboutAction = QtGui.QAction(self.tr('&About'), self)
        self.aboutAction.setStatusTip(self.tr("Show the Qt library's About box"))
        self.aboutAction.triggered.connect(self.about)

        self.aboutQtAction = QtGui.QAction(self.tr('About &Qt'), self)
        self.aboutQtAction.setStatusTip(self.tr("Show the Qt library's About box"))
        self.aboutQtAction.triggered.connect(QtGui.QApplication.aboutQt)

        self.windowActionGroup = QtGui.QActionGroup(self)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr('&File'))
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        self.editMenu = self.menuBar().addMenu(self.tr('&Edit'))
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.pasteAction)

        self.windowMenu = self.menuBar().addMenu(self.tr('&Window'))
        self.windowMenu.addAction(self.closeAction)
        self.windowMenu.addAction(self.closeAllAction)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAction)
        self.windowMenu.addAction(self.cascadeAction)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAction)
        self.windowMenu.addAction(self.previousAction)
        self.windowMenu.addAction(self.separatorAction)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(self.tr('&Help'))
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar(self.tr('File'))
        self.fileToolBar.setObjectName('fileToolBar')
        self.fileToolBar.addAction(self.newAction)
        self.fileToolBar.addAction(self.openAction)
        self.fileToolBar.addAction(self.saveAction)

        self.editToolBar = self.addToolBar(self.tr('Edit'))
        self.editToolBar.setObjectName('editToolBar')
        self.editToolBar.addAction(self.cutAction)
        self.editToolBar.addAction(self.copyAction)
        self.editToolBar.addAction(self.pasteAction)

    def createStatusBar(self):
        readyLabel = QtGui.QLabel(self.tr(' Ready'))
        self.statusBar().addWidget(readyLabel, 1)

    @QtCore.Slot()
    def updateActions(self):
        hasEditor = self.activeEditor() != 0
        hasSelection = self.activeEditor() and self.activeEditor().textCursor().hasSelection()
        self.saveAction.setEnabled(hasEditor)
        self.saveAsAction.setEnabled(hasEditor)
        self.cutAction.setEnabled(hasSelection)
        self.copyAction.setEnabled(hasSelection)
        self.closeAction.setEnabled(hasEditor)
        self.closeAllAction.setEnabled(hasEditor)
        self.tileAction.setEnabled(hasEditor)
        self.cascadeAction.setEnabled(hasEditor)
        self.nextAction.setEnabled(hasEditor)
        self.previousAction.setEnabled(hasEditor)
        self.separatorAction.setEnabled(hasEditor)

        if self.activeEditor():
            self.activeEditor().windowMenuAction().setChecked(True)

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
    documentNumber = 1

    def __init__(self, parent=None):
        super(Editor, self).__init__(parent=parent)
        self.action = QtGui.QAction(self)
        self.action.setCheckable(True)
        self.action.triggered.connect(self.show)
        self.action.triggered.connect(self.setFocus)

        self.isUntitled = True
        self.curFile = ''

        self.setWindowIcon(QtGui.QPixmap(':/document.png'))
        self.setWindowTitle('[*]')

        self.document().contentsChanged.connect(self.documentWasModified)

        # 윈도우를 닫을 때 메모리가 누수되지 않도록 함
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def documentWasModified(self):
        pass

    def windowMenuAction(self):
        return self.action

    def newFile(self):
        self.curFile = self.tr('document%d.txt' % self.documentNumber)
        self.setWindowTitle(self.curFile + '[*]')
        self.action.setText(self.curFile)
        self.isUntitled = True
        Editor.documentNumber += 1

    @classmethod
    def open(cls, parent):
        fileName = QtGui.QFileDialog.getOpenFileName(parent, 'Open', '.')
        if fileName:
            return cls.openFile(fileName, parent)
        return 0

    @staticmethod
    def openFile(fileName, parent):
        editor = Editor(parent)
        if editor.readFile(fileName):
            editor.setCurrentFile(fileName)
            return editor
        else:
            del editor
            return 0

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def closeEvent(self, event):
        if self.okToContinue():
            event.accept()
        else:
            event.ignore()

    def okToContinue(self):
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.isUntitled = False
        self.action.setText(self.strippedName(self.curFile))
        self.document().setModified(False)
        self.setWindowTitle(self.strippedName(self.curfile) + '[*]')
        self.setWindowModified(False)

    def sizeHint(self):
        return QtCore.QSize(72 * self.fontMetrics().width('x'),
                            25 * self.fontMetrics().lineSpacing())

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mdiEditor = MainWindow()
    mdiEditor.show()
    sys.exit(app.exec_())
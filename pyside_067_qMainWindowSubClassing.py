# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui, QtCore

# import subprocess
# cmd = 'C:/Python27/Lib/site-packages/PySide/pyside-rcc.exe -o resource_rc.py images/resource.qrc'
# subprocess.Popen(cmd, stdout=subprocess.PIPE)

from pyside_052_sortDialog import SortDialog
from pyside_042_usingQDialogButtonBox import GoToCellDialog
from pyside_021_FindDialog import FindDialog
from pyside_114_Spreadsheet import Spreadsheet, SpreadsheetCompare

import resource_rc

class MainWindow(QtGui.QMainWindow):
    maxRecentFiles = 5
    recentFiles = []
    curFile = ''
    findDialog = 0

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        self.spreadsheet = Spreadsheet(self)
        self.setCentralWidget(self.spreadsheet)

        self.createActions()
        self.createMenus()
        self.createContextMenu()
        self.createToolBars()
        self.createStatusBar()
        self.readSettings()

        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        self.setCurrentFile('')
        self.updateStatusBar()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    # ----------------------
    # protected
    # ----------------------
    # 타이틀바의 종료 버튼을 눌렀을때 호출되는 슬롯
    # closeEvent를 재정의해서, 정말 윈도우를 종료할 것 인지 여부를 결정하게 함.
    def closeEvent(self, event):
        if self.okToContinue():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()
    # ----------------------
    # private slots
    # ----------------------
    def newFile(self):
        # mainWindow = MainWindow()
        # mainWindow.show()
        if self.okToContinue():
            self.spreadsheet.clear()
            self.setWindowModified(False)

    def open(self):
        if self.okToContinue():
            # getOpenFileName의 인수는 부모, 타이틀, 디렉토리, 파일필터이다.
            # 파일필터를 복수 지정할 때는, 사이에 \n을 붙인다.
            fileName, _ = QtGui.QFileDialog.getOpenFileName(self,
                                                         self.tr('Open Spreadsheet'),
                                                         '.',
                                                         self.tr('Spreadsheet files (*.sp)'))
            if fileName:
                self.loadFile(fileName)

    def save(self):
        if not self.curFile:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        # getSaveFileName는 인수에 추가로 QtGui.QFileDialog.DontConfirmOverwrite를 전달하면,
        # 덮어쓰기확인을 생략한다.
        fileName, _ = QtGui.QFileDialog.getSaveFileName(self,
                                                     self.tr('Save Spreadsheet'),
                                                     '.',
                                                     self.tr('Spreadsheet files (*.sp)'))
        if not fileName:
            return False

        return self.saveFile(fileName)

    def find(self):
        # 윈도우 상호 전환이 가능한 모덜리스 윈도우를 작성
        if not self.findDialog:
            self.findDialog = FindDialog(self)
            self.findDialog.findNext.connect(self.spreadsheet.findNext)
            self.findDialog.findPrevious.connect(self.spreadsheet.findPrevious)
        # show()전에 setModal()을 하게 되면 모덜 윈도우가 됨
        self.findDialog.show()
        self.findDialog.raise_()
        self.findDialog.activateWindow()

    def goToCell(self):
        # 윈도우 상호 전환이 불가능한 모덜 윈도우를 작성
        # show()대신 exec()로 띄우면 모덜 윈도우로 작성됨
        dialog = GoToCellDialog(self)
        if dialog.exec_():
            string = dialog.ui.lineEdit.text().upper()
            self.spreadsheet.setCurrentCell(int(string[1:])-1, ord(string[0])-ord('A'))

    def sort(self):
        dialog = SortDialog(self)
        selectedRanges = self.spreadsheet.selectedRanges()
        print selectedRanges
        dialog.setColumnRange(ord('A')+selectedRanges.leftColumn(),
                              ord('A')+selectedRanges.rightColumn())
        if dialog.exec_():
            compare = SpreadsheetCompare()
            compare.keys[0] = dialog.ui.primaryColumnCombo.currentIndex()
            compare.keys[1] = dialog.ui.secondaryColumnCombo.currentIndex()-1
            compare.keys[2] = dialog.ui.tertiaryColumnCombo.currentIndex()-1
            compare.ascending[0] = dialog.ui.primaryOrderCombo.currentIndex() == 0
            compare.ascending[1] = dialog.ui.secondaryOrderCombo.currentIndex() == 0
            compare.ascending[2] = dialog.ui.tertiaryOrderCombo.currentIndex() == 0
            self.spreadsheet.sort(compare)

    def about(self):
        QtGui.QMessageBox.about(self, self.tr('About Spreadsheet'),
                                self.tr('<h2>Spreadsheet 1.1</h2>'
                                        '<p>Copyright &copy; 2008 Software Inc.'                                   
                                        '<p>Spreadsheet is a small application that '
                                        'demonstrates QAction, QMainWindow, QMenuBar, '
                                        'QStatusBar, QTableWidget, QToolBar, and many other'
                                        'Qt classes.'))

    def openRecentFile(self):
        if self.okToContinue():
            action = self.sender()
            if action:
                self.loadFile(action.data())

    def updateStatusBar(self):
        self.locationLabel.setText(self.spreadsheet.currentLocation())
        self.formulaLabel.setText(self.spreadsheet.currentFormula())

    def spreadsheetModified(self):
        self.setWindowModified(True)
        #self.updateStatusBar()
    # ----------------------
    # private
    # ----------------------
    def createActions(self):
        # -----------------------------------
        # new
        # -----------------------------------
        self.newAction = QtGui.QAction(self.tr('&New'), self)
        self.newAction.setIcon(QtGui.QIcon(':/images/new.png'))
        self.newAction.setShortcut(QtGui.QKeySequence.New)
        self.newAction.setStatusTip(self.tr('Create a new spreadsheet file'))
        self.newAction.triggered.connect(self.newFile)
        # -----------------------------------
        # open
        # -----------------------------------
        self.openAction = QtGui.QAction(self.tr('&Open'), self)
        self.openAction.setIcon(QtGui.QIcon(':/images/open.png'))
        self.openAction.setShortcut(QtGui.QKeySequence.Open)
        self.openAction.setStatusTip(self.tr('Open a spreadsheet file'))
        self.openAction.triggered.connect(self.open)
        # -----------------------------------
        # save
        # -----------------------------------
        self.saveAction = QtGui.QAction(self.tr('&Save'), self)
        self.saveAction.setIcon(QtGui.QIcon(':/images/save.png'))
        self.saveAction.setShortcut(QtGui.QKeySequence.Save)
        self.saveAction.setStatusTip(self.tr('Save a spreadsheet file'))
        self.saveAction.triggered.connect(self.save)
        # -----------------------------------
        # save as
        # -----------------------------------
        self.saveAsAction = QtGui.QAction(self.tr('SaveAs'), self)
        self.saveAsAction.setIcon(QtGui.QIcon(':/images/saveAs.png'))
        self.saveAsAction.setShortcut(QtGui.QKeySequence.SaveAs)
        self.saveAsAction.setStatusTip(self.tr('Save as a spreadsheet file'))
        self.saveAsAction.triggered.connect(self.saveAs)
        # -----------------------------------
        # recently opened files
        # -----------------------------------
        self.recentFileActions = []
        for idx in range(self.maxRecentFiles):
            action = QtGui.QAction(self)
            # 동적인 표시를 위해 기본 비표시로 생성
            action.setVisible(False)
            action.triggered.connect(self.openRecentFile)
            self.recentFileActions.append(action)
        # -----------------------------------
        # close
        # -----------------------------------
        self.closeAction = QtGui.QAction(self.tr('&Close'), self)
        self.closeAction.setShortcut(self.tr('Ctrl+W'))
        self.closeAction.setStatusTip(self.tr('Close this window'))
        self.closeAction.triggered.connect(self.close)
        # -----------------------------------
        # exit
        # -----------------------------------
        self.exitAction = QtGui.QAction(self.tr('E&xit'), self)
        self.exitAction.setShortcut(self.tr('Ctrl+Q'))
        self.exitAction.setStatusTip(self.tr('Exit the application'))
        self.exitAction.triggered.connect(QtGui.qApp.closeAllWindows)
        # -----------------------------------
        # select all
        # -----------------------------------
        self.selectAllAction = QtGui.QAction(self.tr('&All'), self)
        self.selectAllAction.setShortcut(QtGui.QKeySequence.SelectAll)
        self.selectAllAction.setStatusTip(self.tr('Select all the cells in the'
                                             'spreadsheet'))
        self.selectAllAction.triggered.connect(self.spreadsheet.selectAll)
        # -----------------------------------
        # show grid
        # -----------------------------------
        self.showGridAction = QtGui.QAction(self.tr('&Show Grid'), self)
        self.showGridAction.setCheckable(True)
        self.showGridAction.setStatusTip(self.tr('Show or hide the spreadsheet\'s'
                                            'grid'))
        self.showGridAction.toggled[bool].connect(self.spreadsheet.setShowGrid)
        # -----------------------------------
        # aboutQt
        # -----------------------------------
        self.aboutQtAction = QtGui.QAction(self.tr('About &Qt'), self)
        self.aboutQtAction.setStatusTip(self.tr('Show the Qt library\'s About box'))
        self.aboutQtAction.triggered.connect(QtGui.qApp.aboutQt)
        # -----------------------------------
        # cut
        # -----------------------------------
        self.cutAction = QtGui.QAction(self.tr('Cu&t'), self)
        self.cutAction.setIcon(QtGui.QIcon(':/images/cut.png'))
        self.cutAction.setShortcut(QtGui.QKeySequence.Cut)
        self.cutAction.triggered.connect(self.spreadsheet.cut)
        # -----------------------------------
        # copy
        # -----------------------------------
        self.copyAction = QtGui.QAction(self.tr('&Copy'), self)
        self.copyAction.setIcon(QtGui.QIcon(':/images/copy.png'))
        self.copyAction.setShortcut(QtGui.QKeySequence.Copy)
        self.copyAction.triggered.connect(self.spreadsheet.copy)
        # -----------------------------------
        # paste
        # -----------------------------------
        self.pasteAction = QtGui.QAction(self.tr('&Paste'), self)
        self.pasteAction.setIcon(QtGui.QIcon(':/images/paste.png'))
        self.pasteAction.setShortcut(QtGui.QKeySequence.Paste)
        self.pasteAction.triggered.connect(self.spreadsheet.paste)
        # -----------------------------------
        # delete
        # -----------------------------------
        self.deleteAction = QtGui.QAction(self.tr('Delete'), self)
        self.deleteAction.setIcon(QtGui.QIcon(':/images/delete.png'))
        self.deleteAction.setShortcut(QtGui.QKeySequence.Delete)
        self.deleteAction.triggered.connect(self.spreadsheet.del_)
        # -----------------------------------
        # selectRow
        # -----------------------------------
        self.selectRowAction = QtGui.QAction(self.tr('SelectRow'), self)
        self.selectColumnAction = QtGui.QAction(self.tr('SelectColumn'), self)
        # -----------------------------------
        # find
        # -----------------------------------
        self.findAction = QtGui.QAction(self.tr('Find'), self)
        self.findAction.setIcon(QtGui.QIcon(':/images/find_normal.png'))
        self.findAction.setShortcut(QtGui.QKeySequence.Find)
        self.findAction.triggered.connect(self.find)
        # -----------------------------------
        # goToCell
        # -----------------------------------
        self.goToCellAction = QtGui.QAction(self.tr('Go To Cell'), self)
        self.goToCellAction.setShortcut(self.tr('Ctrl+G'))
        self.goToCellAction.triggered.connect(self.goToCell)
        # -----------------------------------
        # recalculate
        # -----------------------------------
        self.recalculateAction = QtGui.QAction(self.tr('&Recalculate'), self)
        self.recalculateAction.setShortcut(self.tr('F9'))
        self.recalculateAction.triggered.connect(self.spreadsheet.recalculate)
        # -----------------------------------
        # sort
        # -----------------------------------
        self.sortAction = QtGui.QAction(self.tr('&Sort'), self)
        self.sortAction.triggered.connect(self.sort)
        # -----------------------------------
        # autoRecalculate
        # -----------------------------------
        self.autoRecalcAction = QtGui.QAction(self.tr('&Auto-Recalculate'), self)
        self.autoRecalcAction.setCheckable(True)
        self.autoRecalcAction.toggled[bool].connect(self.spreadsheet.setAutoRecalculate)
        # -----------------------------------
        # about
        # -----------------------------------
        self.aboutAction = QtGui.QAction(self.tr('About'), self)
        self.aboutAction.triggered.connect(self.about)

    def createMenus(self):
        # -----------------------------------
        # file
        # -----------------------------------
        fileMenu = self.menuBar().addMenu(self.tr('&File'))
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        self.separatorAction = fileMenu.addSeparator()
        for idx in range(self.maxRecentFiles):
            fileMenu.addAction(self.recentFileActions[idx])
        fileMenu.addSeparator()
        fileMenu.addAction(self.closeAction)
        fileMenu.addAction(self.exitAction)
        # -----------------------------------
        # edit
        # -----------------------------------
        editMenu = self.menuBar().addMenu(self.tr('&Edit'))
        editMenu.addAction(self.cutAction)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.deleteAction)

        selectSubMenu = editMenu.addMenu(self.tr('&Select'))
        selectSubMenu.addAction(self.selectRowAction)
        selectSubMenu.addAction(self.selectColumnAction)
        selectSubMenu.addAction(self.selectAllAction)

        editMenu.addSeparator()
        editMenu.addAction(self.findAction)
        editMenu.addAction(self.goToCellAction)
        # -----------------------------------
        # tools
        # -----------------------------------
        toolsMenu = self.menuBar().addMenu(self.tr('&Tools'))
        toolsMenu.addAction(self.recalculateAction)
        toolsMenu.addAction(self.sortAction)
        # -----------------------------------
        # options
        # -----------------------------------
        optionMenu = self.menuBar().addMenu(self.tr('&Options'))
        optionMenu.addAction(self.showGridAction)
        optionMenu.addAction(self.autoRecalcAction)
        # -----------------------------------
        # separator
        # -----------------------------------
        self.menuBar().addSeparator()
        # -----------------------------------
        # help
        # -----------------------------------
        helpMenu = self.menuBar().addMenu(self.tr('&Help'))
        helpMenu.addAction(self.aboutAction)
        helpMenu.addAction(self.aboutQtAction)

    def createContextMenu(self):
        self.spreadsheet.addAction(self.cutAction)
        self.spreadsheet.addAction(self.copyAction)
        self.spreadsheet.addAction(self.pasteAction)
        self.spreadsheet.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def createToolBars(self):
        fileToolBar = self.addToolBar(self.tr('&File'))
        fileToolBar.addAction(self.newAction)
        fileToolBar.addAction(self.openAction)
        fileToolBar.addAction(self.saveAction)

        editToolBar = self.addToolBar(self.tr('&Edit'))
        editToolBar.addAction(self.cutAction)
        editToolBar.addAction(self.copyAction)
        editToolBar.addSeparator()
        editToolBar.addAction(self.findAction)
        editToolBar.addAction(self.goToCellAction)

    def createStatusBar(self):
        self.locationLabel = QtGui.QLabel('W999')
        self.locationLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.locationLabel.setMinimumSize(self.locationLabel.sizeHint())

        self.formulaLabel = QtGui.QLabel()
        self.formulaLabel.setIndent(3)

        self.statusBar().addWidget(self.locationLabel)
        self.statusBar().addWidget(self.formulaLabel, 1)

        self.spreadsheet.currentCellChanged[int, int, int, int].connect(self.updateStatusBar)
        self.spreadsheet.modified.connect(self.spreadsheetModified)

    def readSettings(self):
        # value에서 부울을 취득할때 값을 unicode로 받는 버그가 있음
        def bool(val):
            if val == u'true':
                return True
            elif val == u'false':
                return False
            else:
                return val
        # QSettings의 인자는 기관이름, 응용프로그램 이름
        settings = QtCore.QSettings('Software Inc.', 'Spreadsheet')

        self.restoreGeometry(settings.value('geometry', None), )

        self.recentFiles = settings.value('recentFiles', [])
        self.updateRecentFileActions()
        # 두번째 인자는 값이 존재하지 않을때를 위한 기본값.
        # 응용프로그램이 처음 실행 될 때 등에 사용된다.
        showGrid = bool(settings.value('showGrid', True))
        self.showGridAction.setChecked(showGrid)
        self.showGridAction.toggled.emit(showGrid)

        autoRecalc = bool(settings.value('autoRecalc', True))
        self.autoRecalcAction.setChecked(autoRecalc)
        self.autoRecalcAction.toggled.emit(autoRecalc)


    def writeSettings(self):
        settings = QtCore.QSettings('Software Inc.', 'Spreadsheet')
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('recentFiles', self.recentFiles)
        settings.setValue('showGrid', self.showGridAction.isChecked())
        settings.setValue('autoRecalc', self.autoRecalcAction.isChecked())
        # 디렉토리처럼 관리되기도 한다.
        # settings.beginGroup('findDialog')
        # settings.setValue('matchCase', self.caseCheckBox.isChecked())
        # settings.setValue('searchBackward', self.backwardCheckBox.isChecked())
        # settings.endGroup()

    def okToContinue(self):
        if self.isWindowModified():
            ret = QtGui.QMessageBox.warning(self, self.tr('Spreadsheet'),
                                            self.tr('The document has been modified.\n'
                                                    'Do you want to save your changes?'),
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Yes:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False
        return True

    def loadFile(self, fileName):
        if not self.spreadsheet.readFile(fileName):
            # showMessage의 인수는 메세지, 표시시간(밀리초)
            self.statusBar().showMessage(self.tr('Loading canceled'), 2000)
            return False
        self.setCurrentFile(fileName)
        self.statusBar().showMessage(self.tr('File loaded'), 2000)
        return True

    def saveFile(self, fileName):
        if not self.spreadsheet.writeFile(fileName):
            self.statusBar().showMessage(self.tr('Saving canceled'), 2000)
            return False
        self.setCurrentFile(fileName)
        self.statusBar().showMessage(self.tr('File saved'), 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.setWindowModified(False)
        shownName = self.tr('Untitled')
        if self.curFile:
            shownName = self.strippedName(self.curFile)
            while self.recentFiles.count(self.curFile):
                self.recentFiles.remove(self.curFile)
            self.recentFiles.insert(0, self.curFile)
            self.updateRecentFileActions()
        # osx이외의 플렛폼에서는 문서가 아직 저장되지 않음을 *로 표시
        # 별표가 보여야 할 곳에 [*]를 넣어두고 windowModified를 최신값으로 유지하면 됨.
        # '%s'%문법을 사용해서 2중으로 translate하면 텍스트가 비어져 버리는 버그가 있으므로 format사용할것.
        self.setWindowTitle(self.tr('{0}[*] - {1}'.format(shownName, self.tr('Spreadsheet'))))
        print 'MainWindow::setCurrentFile called.', self.curFile, self.recentFiles

    def updateRecentFileActions(self):
        self.recentFiles = filter(QtCore.QFile.exists, self.recentFiles)
        for j in range(self.maxRecentFiles):
            if j < len(self.recentFiles):
                text = self.tr('&{0:d} {1}'.format(j+1, self.strippedName(self.recentFiles[j])))
                self.recentFileActions[j].setText(text)
                self.recentFileActions[j].setData(self.recentFiles[j])
                self.recentFileActions[j].setVisible(True)
            else:
                self.recentFileActions[j].setVisible(False)
        self.separatorAction.setVisible(bool(self.recentFiles))

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()





        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    splash = QtGui.QSplashScreen()
    splash.setPixmap(QtGui.QPixmap(':/images/icon.png'))
    splash.show()
    topRight = QtCore.Qt.Alignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
    splash.showMessage(splash.tr('Setting up the main window'), topRight, QtCore.Qt.white)
    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())
# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore
from pyside_156_IconEditor import IconEditor


class DockWidget(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(DockWidget, self).__init__(parent=parent)
        iconEditor = IconEditor()
        self.setCentralWidget(iconEditor)

        # toolBar 를 참조하는 변수가 사라질때 툴바도 사라진다
        self.fontToolBar = QtGui.QToolBar('font')
        # 객체이름은 디버깅과 일부 테스트 도구에서 사용되고
        # dockWidget 과 toolBar 의 경우, 객체명을 지정하지 않으면, saveState 와 restoreState 를 이용할 수 없다.
        # 메인윈도우의 스테이트를 저장, 로드하면 툴바와 도킹윈도우 상태를 되될릴 수 있다.
        self.fontToolBar.setObjectName('fontToolBar')
        # 허용 도킹 영역을 지정하지 않을경우, 네 개의 도킹 영역 모두를 이용하게 됨
        self.fontToolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea | QtCore.Qt.BottomToolBarArea)
        self.addToolBar(self.fontToolBar)
        self.fontToolBar.addAction(QtGui.QAction('File', self))
        comboBox = QtGui.QComboBox()
        self.fontToolBar.addWidget(comboBox)

        treeWidget = QtGui.QTreeWidget()
        self.shapesDockWidget = QtGui.QDockWidget('Shapes')
        self.shapesDockWidget.setObjectName('shapesDockWidget')
        # addWidget 이 아닌 setWidget 으로 자식 위젯을 받음
        self.shapesDockWidget.setWidget(treeWidget)
        self.shapesDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.shapesDockWidget)

        self.readSettings()

    def writeSettings(self):
        settings = QtCore.QSettings('Software Inc.', 'Icon Editor')
        settings.beginGroup('mainWindow')
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('state', self.saveState())
        settings.endGroup()

    def readSettings(self):
        settings = QtCore.QSettings('Software Inc.', 'Icon Editor')
        settings.beginGroup('mainWindow')
        self.restoreGeometry(settings.value('geometry'))
        self.restoreState(settings.value('state'))
        settings.endGroup()

    def closeEvent(self, event):
        self.writeSettings()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = DockWidget()
    mainWindow.show()
    sys.exit(app.exec_())
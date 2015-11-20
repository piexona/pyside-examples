# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore

# event 는 QEvent 에서 파생된다
# Ctrl, Alt, Shift 등의 수식키 (Modifier)는 굳이 따로 체크 안해도,
# keyPressEvent 내에서 QKeyEvent.modifiers() 로 체크가 가능


class CodeEditor(QtGui.QWidget):

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Home:
            if event.modifiers() and QtCore.Qt.ControlModifier:
                print 'Ctrl + Home'
            else:
                print 'Home'
        elif event.key() == QtCore.Qt.Key_End:
            print 'End'
        elif event.key() == QtCore.Qt.Key_Tab:
            print 'Tab'
        else:
            return QtGui.QWidget.keyPressEvent(self, event)

    # tab 키와 backTab (Shift+Tab) 키는 특별히 keyPressEvent 보다 먼저 처리해,
    # 포커스를 다음 위젯으로 넘기기 위해 사용한다.
    # tab 으로 들여쓰기를 하려면 재정의가 필요하다.
    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            print 'event >> Tab'
            # True 를 리턴하여 이 이벤트를 직접 처리했음을 Qt 에 알린다.
            # False 를 리턴하면 Qt 는 이 이벤트를 부모 위젯에까지 전파한다.
            return True
        else:
            return QtGui.QWidget.event(self, event)

    # 키 바인딩을 위한 또다른 세련된 방법은 QAction 을 사용하는 것이다.
    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent=parent)
        self.homeAction = QtGui.QAction(self.tr('Home Action'), self)
        self.homeAction.setShortcut('Ctrl+Q')
        self.homeAction.triggered.connect(self.homePressed)

    @QtCore.Slot()
    def homePressed(self):
        print 'home pressed'


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(parent=None)
        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)
        # 활성화 되야 키 이벤트를 받는다
        # self.editor.setFocus()
        # self.editor.setFocusPolicy(QtCore.Qt.StrongFocus)
        fileMenu = QtGui.QMenu('File')
        fileMenu.addAction(self.editor.homeAction)
        # 메뉴바를 보일 필요가 없다면, QAction 이 키바인딩을 위해 내부적으로 사용하는 클래스인
        # QShortcut 을 사용할 수 있다.
        self.menuBar().addMenu(fileMenu)
        self.menuBar().hide()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
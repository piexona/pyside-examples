# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore

class CustomerInfoDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CustomerInfoDialog, self).__init__(parent=parent)
        self.firstNameEdit = QtGui.QLineEdit()
        self.lastNameEdit = QtGui.QLineEdit()
        self.cityEdit = QtGui.QLineEdit()
        self.phoneNumberEdit = QtGui.QLineEdit()
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.firstNameEdit)
        self.mainLayout.addWidget(self.lastNameEdit)
        self.mainLayout.addWidget(self.cityEdit)
        self.mainLayout.addWidget(self.phoneNumberEdit)
        self.setLayout(self.mainLayout)
        # 이벤트 필터가 등록되면 각 위젯으로 보내질 이벤트는
        # 우선적으로 모니터링 수행 객체의 eventFilter 함수에 전달된다.
        self.firstNameEdit.installEventFilter(self)
        self.lastNameEdit.installEventFilter(self)
        self.cityEdit.installEventFilter(self)
        self.phoneNumberEdit.installEventFilter(self)

    def eventFilter(self, target, event):
        if target == self.firstNameEdit or target == self.lastNameEdit or\
           target == self.cityEdit or target == self.phoneNumberEdit:
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Space:
                    self.focusNextChild()
                    # True 를 리턴해서, 이 이벤트를 우리가 직접 처리했음을 Qt 에게 알린다.
                    # 만약 False 를 리턴한다면, 이벤트를 원래 목적지로 전송하게 되어
                    # 공백을 입력하게 된다.
                    return True
        return super(CustomerInfoDialog, self).eventFilter(target, event)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dialog = CustomerInfoDialog()
    dialog.show()
    # app.exec_() 를 호출하면 Qt의 이벤트 루프가 시작된다
    sys.exit(app.exec_())
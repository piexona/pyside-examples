# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore

class FindDialog(QtGui.QDialog):
    # =====================================
    # Signals
    # =====================================
    # QtCore.Qt.CaseSensitivity는 enum타입으로서
    # QtCore.Qt.CaseSensitive나 QtCore.Qt.CaseInsensitive값을 갖는다.
    findNext = QtCore.Signal(str, QtCore.Qt.CaseSensitivity)
    findPrevious = QtCore.Signal(str, QtCore.Qt.CaseSensitivity)
    # =====================================
    # Private
    # =====================================
    _label = None
    _lineEdit = None
    _caseCheckBox = None
    _backwardCheckBox = None
    _findButton = None
    _closeButton = None
    # =====================================
    # Public
    # =====================================
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)

        # tr은 해당 문자열이 다른 나라의 언어로 번역될 수 있음을 표시하는 것
        # &는 그 바로 뒤의 문자가 단축키임을 나타냄 이 경우에는 Alt+W이고 실제로 동작함
        self.label = QtGui.QLabel(self.tr('Find &what:'))
        self.lineEdit = QtGui.QLineEdit()
        self.label.setBuddy(self.lineEdit)

        self.caseCheckBox = QtGui.QCheckBox(self.tr('Match &case'))
        self.backwardCheckBox = QtGui.QCheckBox(self.tr('Search &backward'))

        self.findButton = QtGui.QPushButton(self.tr('&Find'))
        self.findButton.setDefault(True)
        self.findButton.setEnabled(False)

        self.closeButton = QtGui.QPushButton(self.tr('Close'))

        self.lineEdit.textChanged[str].connect(self._slot_enableFindButton)
        self.findButton.clicked.connect(self._slot_findClicked)
        self.closeButton.clicked.connect(self.close)

        self.topLeftLayout = QtGui.QHBoxLayout()
        self.topLeftLayout.addWidget(self.label)
        self.topLeftLayout.addWidget(self.lineEdit)

        self.leftLayout = QtGui.QVBoxLayout()
        self.leftLayout.addLayout(self.topLeftLayout)
        self.leftLayout.addWidget(self.caseCheckBox)
        self.leftLayout.addWidget(self.backwardCheckBox)

        self.rightLayout = QtGui.QVBoxLayout()
        self.rightLayout.addWidget(self.findButton)
        self.rightLayout.addWidget(self.closeButton)
        self.rightLayout.addStretch()

        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.setLayout(self.mainLayout)

        self.setWindowTitle(self.tr(r'Find'))
        # sizeHint는 위젯의 이상적인 크기를 리턴하는 함수
        # setFixedHeight로 세로창크기를 고정시킴
        self.setFixedHeight(self.sizeHint().height())

    # =====================================
    # Private slots
    # =====================================
    @QtCore.Slot()
    def _slot_findClicked(self):
        text = self.lineEdit.text()
        cs = self.caseCheckBox.isChecked()

        if self.backwardCheckBox.isChecked():
            self.findPrevious.emit(text, cs)
        else:
            self.findNext.emit(text, cs)

    @QtCore.Slot(str)
    def _slot_enableFindButton(self, text):
        self.findButton.setEnabled(bool(text))
        

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = FindDialog()
    dialog.show()
    sys.exit(app.exec_())
# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore


class Ticker(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Ticker, self).__init__(parent=parent)
        self.myText = 'Ticker'
        self.offset = 0
        self.myTimerId = 0

    def text(self):
        return self.myText

    def setText(self, newText):
        self.myText = newText
        self.update()
        self.updateGeometry()

    def sizeHint(self):
        return self.fontMetrics().size(0, self.text())

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        textWidth = self.fontMetrics().width(self.text())
        if textWidth < 1:
            return
        x = -self.offset
        # 텍스트를 화면 가득 채우기 위해 반복 출력
        while x < self.width():
            painter.drawText(x, 0, textWidth, self.height(),
                             QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, self.text())
            x += textWidth

    def showEvent(self, event):
        # 30 밀리초 마다 동작하는 이벤트를 생성
        self.myTimerId = self.startTimer(30)

    def timerEvent(self, event):
        if event.timerId() == self.myTimerId:
            self.offset += 1
            if self.offset >= self.fontMetrics().width(self.text()):
                self.offset = 0
            self.scroll(-1, 0)
        else:
            QtGui.QWidget.timerEvent(event)

    def hideEvent(self, event):
        self.killTimer(self.myTimerId)
        self.myTimer = 0



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    win = Ticker()
    win.show()
    sys.exit(app.exec_())
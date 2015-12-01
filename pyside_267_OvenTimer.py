# coding: utf-8
# author: wie@ppi.co.jp
import math
from PySide import QtGui, QtCore


class OvenTimer(QtGui.QWidget):
    DegreesPerMinute = 7.0
    DegreesPerSecond = DegreesPerMinute / 60
    MaxMinute = 45
    MaxSeconds = MaxMinute * 60
    UpdateInterval = 5

    def __init__(self, parent=None):
        super(OvenTimer, self).__init__(parent=parent)
        finishTime = QtCore.QDateTime.currentDateTime()
        self.updateTimer = QtCore.QTimer(self)
        self.updateTimer.timeout.connect(self.update)
        self.finishTimer = QtCore.QTimer(self)
        # 한번만 타임아웃 시킬 것 이므로 싱글샷을 호출한다
        self.finishTimer.setSingleShot(True)
        self.finishTimer.timeout.connect(self.timeout)
        # 타이머가 중지되면 업데이트 타이머도 멈추게 한다
        self.finishTimer.timeout.connect(self.updateTimer.stop)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.setFont(font)

        self.setDuration(3)

    @staticmethod
    def bound(_min, val, _max):
        if val < _min:
            val = _min
        elif val > _max:
            val = _max
        return val

    def setDuration(self, secs):
        secs = OvenTimer.bound(0, secs, self.MaxSeconds)
        self.finishTime = QtCore.QDateTime.currentDateTime().addSecs(secs)

        if secs > 0:
            self.updateTimer.start(self.UpdateInterval * 1000)
            self.finishTimer.start(secs * 1000)
        else:
            self.updateTimer.stop()
            self.finishTimer.stop()
        self.update()

    def duration(self):
        secs = QtCore.QDateTime.currentDateTime().secsTo(self.finishTime)
        if secs < 0:
            secs = 0
        return secs

    def draw(self, painter):
        # 논리좌표가 (-50, -50, 100, 100)이므로, 이 삼각형은 상단중앙에 표시된다.
        triangle = [
            QtCore.QPoint(-2, -49),
            QtCore.QPoint(2, -49),
            QtCore.QPoint(0, -47)
        ]
        # foreground()は無くなったのでwindowText()を使用
        thickPen = QtGui.QPen(self.palette().windowText(), 1.5)
        thinPen = QtGui.QPen(self.palette().windowText(), 0.5)
        niceBlue = QtGui.QColor(150, 150, 200)
        painter.setPen(thinPen)
        painter.setBrush(self.palette().windowText())
        # 삼각형을 하드코딩해도, 크기조절이 자동으로 이루어 지는 것이
        # 윈도우/뷰포트 매커니즘의 편리한 점이다.
        painter.drawPolygon(QtGui.QPolygon(triangle))
        # 바깥쪽 원을 그린다.
        coneGradient = QtGui.QConicalGradient(0, 0, -90.0)
        coneGradient.setColorAt(0.0, QtCore.Qt.darkGray)
        coneGradient.setColorAt(0.2, niceBlue)
        coneGradient.setColorAt(0.5, QtCore.Qt.white)
        coneGradient.setColorAt(1.0, QtCore.Qt.darkGray)
        painter.setBrush(coneGradient)
        painter.drawEllipse(-46, -46, 92, 92)
        # 안쪽 원을 그린다.
        haloGradient = QtGui.QRadialGradient(0, 0, 20, 0, 0)
        haloGradient.setColorAt(0.0, QtCore.Qt.black)
        haloGradient.setColorAt(0.8, QtCore.Qt.darkGray)
        haloGradient.setColorAt(0.9, QtCore.Qt.white)
        haloGradient.setColorAt(1.0, QtCore.Qt.black)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(haloGradient)
        painter.drawEllipse(-20, -20, 40, 40)


    def timeout(self):
        print 'timeout'
        pass

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        side = min(self.width(), self.height())
        # 항상 가장 큰 정사각형의 뷰포트가 되도록 설정
        painter.setViewport((self.width() - side) / 2, (self.height() - side) / 2,
                            side, side)
        # 논리좌표의 범위를 설정. 여기서는 (0,0)가 중앙에 오도록 설정하였다.
        # 윈도우(논리좌표)는 뷰포트(물리좌표)를 가득채우도록 매핑된다.
        painter.setWindow(-50, -50, 100, 100)
        self.draw(painter)

    def mousePressEvent(self, event):
        point = event.pos() - self.rect().center()
        theta = math.atan2(-point.x(), -point.y()) * 180.0 / math.pi
        self.setDuration(self.duration() + int(theta / self.DegreesPerSecond))
        self.update()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    win = OvenTimer()
    win.show()
    sys.exit(app.exec_())
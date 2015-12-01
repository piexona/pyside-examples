# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore


class Painter(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Painter, self).__init__(parent=parent)

    def paintEvent(self, event):
        #########################
        # 타원
        #########################
        painter = QtGui.QPainter(self)
        # 안티앨리어싱 설정
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        # QPen 설정 여기서 사용된 인자는 (색, 굵기, 선타입, 조인타입)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.DashDotLine, QtCore.Qt.RoundCap))
        # QBrush 설정 (색, 브러시스타일)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.darkGray, QtCore.Qt.SolidPattern))
        # (x좌표, y좌표, 넓이, 높이)
        painter.drawEllipse(50, 50, 100, 50)

        #########################
        # 파이
        #########################
        # QPen 설정 여기서 사용된 인자는 (색, 굵기, 선타입, 끝모양, 조인타입)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 4, QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.DiagCrossPattern))
        # 마지막 두 인자는 1/16도 (degree) 단위로 표현된 값이다.
        painter.drawPie(50, 150, 100, 50, 60 * 16, 270 * 16)

        #########################
        # 3차 베이어 곡선
        #########################
        path = QtGui.QPainterPath()
        path.moveTo(80, 320)
        path.cubicTo(200, 80, 320, 80, 480, 320)
        painter.setPen(QtGui.QPen(QtCore.Qt.darkRed, 1))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.NoBrush))
        painter.drawPath(path)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    win = Painter()
    win.show()

    sys.exit(app.exec_())
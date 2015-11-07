# coding: utf-8
# author: wie@ppi.co.jp
import sys
from PySide import QtCore, QtGui

class IconEditor(QtGui.QWidget):
    curColor = None
    image = None
    zoom = None
    defaultBackgroundColor = QtGui.qRgba(0, 0, 0, 0)

    # =============================
    # public
    # =============================

    def __init__(self, parent=None):
        super(IconEditor, self).__init__(parent=parent)
        self.setAttribute(QtCore.Qt.WA_StaticContents)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)

        self.curColor = QtGui.QColor(0, 0, 0, 255)
        # 확대 인자
        self.zoom = 16
        # 16x16픽셀의 32비트 ARGB포멧(반투명을 지원하는 포멧)을 설정하고 그 내부를 투명한 색상으로 채움
        self.image = QtGui.QImage(16, 16, QtGui.QImage.Format_ARGB32)
        self.image.fill(self.defaultBackgroundColor)

    @property
    def penColor(self):
        return self.curColor

    @penColor.setter
    def setPenColor(self, newColor):
        self.curColor = newColor

    @property
    def iconImage(self):
        return self.image

    @iconImage.setter
    def setIconImage(self, newImage):
        self.image = newImage.convertToFormat(QtCore.QImage.Format_ARGB32)
        # 위젯을 다시 그림
        self.update()
        # 이 위젯을 포함하는 모든 레이아웃들에게 위젯의 크기 힌트가 변경되었음을 통지
        self.updateGeometry()

    @property
    def zoomFactor(self):
        return self.zoom

    @zoomFactor.setter
    def setZoomFactor(self, newZoom):
        if newZoom < 1:
            newZoom = 1

        if newZoom != self.zoom:
            self.zoom = newZoom
            self.update()
            self.updateGeometry()

    def sizeHint(self):
        size = self.zoom * self.image.size()
        if self.zoom >= 3:
            size += QtCore.QSize(1, 1)
        return size

    # =============================
    # protected
    # =============================

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.__setImagePixel(event.pos(), True)
        elif event.button() == QtCore.Qt.RightButton:
            self.__setImagePixel(event.pos(), False)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.__setImagePixel(event.pos(), True)
        elif event.buttons() == QtCore.Qt.RightButton:
            self.__setImagePixel(event.pos(), False)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.zoom >= 3:
            painter.setPen(self.palette().windowText().color())
            for i in range(self.image.width() + 1):
                painter.drawLine(self.zoom * i, 0, self.zoom * i, self.zoom * self.image.height())
                for j in range(self.image.height() + 1):
                    painter.drawLine(0, self.zoom * j, self.zoom * self.image.width(), self.zoom * j)

            for i in range(self.image.width()):
                for j in range(self.image.height()):
                    rect = self.__pixelRect(i, j)
                    if event.region().intersected(rect):
                        color = QtGui.QColor.fromRgba(self.image.pixel(i, j))
                        if color.alpha() < 255:
                            painter.fillRect(rect, QtCore.Qt.white)
                        painter.fillRect(rect, color)


    # =============================
    # private
    # =============================

    def __setImagePixel(self, pos, opaque):
        i = pos.x() / self.zoom
        j = pos.y() / self.zoom
        if self.image.rect().contains(i, j):
            if opaque:
                self.image.setPixel(i, j, self.penColor.rgba())
            else:
                self.image.setPixel(i, j, self.defaultBackgroundColor)
            self.update(self.__pixelRect(i, j))

    def __pixelRect(self, i, j):
        if self.zoom >= 3:
            return QtCore.QRect(self.zoom * i + 1, self.zoom * j + 1, self.zoom - 1, self.zoom - 1)
        else:
            return QtCore.QRect(self.zoom * i, self.zoom * j, self.zoom, self.zoom)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = IconEditor()
    win.show()
    sys.exit(app.exec_())
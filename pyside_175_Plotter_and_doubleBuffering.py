# coding: utf-8
# author: wie@ppi.co.jp
import math
from PySide import QtGui, QtCore


class Plotter(QtGui.QWidget):
    """Plotter and Double buffering examples"""

    margin = 50

    def __init__(self, *args, **kwargs):
        super(Plotter, self).__init__(*args, **kwargs)

        self.curveMap = {1: [(0, 1), (1, 1), (3, 4)],
                         2: [(4, 5), (8, 9), (10, 1)]}
        self.rubberBandRect = QtCore.QRect()
        self.pixmap = None
        # 참고로 윈도우기본색상은 QPalette.Window
        # 버튼기본색상은 QPalette.Button 인데, QPalette.Dark 는 이보다 더 어두운 색
        # 배경색은 기본적으로 부모위젯을 물려받는데, 배경색을 바꾸려면 setAutoFillBackground 를 호출해야함
        self.setBackgroundRole(QtGui.QPalette.Dark)
        self.setAutoFillBackground(True)
        # 이 위젯의 크기가 더 커질수도, 작아질수도 있음을 이 위젯을 관리하는 레이아웃 매니저에게 알림
        # 기본 크기정책은 QtGui.QSizePolicy.Preferred
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        # 위젯이 포커스를 받을수 있게함 포커스를 갖게 되면 키입력에 대한 이벤트를 받게 됨
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.rubberBandIsShown = False

        # 여기선 버튼을 일부러 레이아웃에 넣지 않고 직접 관리한다.
        self.zoomInButton = QtGui.QToolButton(self)
        self.zoomInButton.setText('+')
        # self.zoomInButton.setIcon(QtGui.QIcon(':/images/zoomIn.png'))
        # 자신의 사이즈 힌트를 참고로 크기를 조정한다.
        self.zoomInButton.adjustSize()
        self.zoomInButton.clicked.connect(self.zoomIn)

        self.zoomOutButton = QtGui.QToolButton(self)
        self.zoomOutButton.setText('-')
        # self.zoomOutButton.setIcon(QtGui.QIcon(':/images/zoomOut.png'))
        self.zoomOutButton.adjustSize()
        self.zoomOutButton.clicked.connect(self.zoomOut)

        self.zoomStack = []
        self.curZoom = 0
        self.setPlotSettings(PlotSettings())

    def setPlotSettings(self, settings):
        self.zoomStack = []
        self.curZoom = 0
        self.zoomStack.append(settings)
        self.zoomInButton.hide()
        self.zoomOutButton.hide()
        self.refreshPixmap()

    def setCurveData(self, _id, data):
        self.curveMap[_id] = data
        self.refreshPixmap()

    def clearCurve(self, _id):
        del self.curveMap[_id]
        self.refreshPixmap()

    def minimumSizeHint(self, *args, **kwargs):
        return QtCore.QSize(6 * self.margin, 4 * self.margin)

    def sizeHint(self, *args, **kwargs):
        return QtCore.QSize(12 * self.margin, 8 * self.margin)

    @QtCore.Slot()
    def zoomIn(self):
        self.curZoom += 1
        self.zoomInButton.setEnabled(self.curZoom < len(self.zoomStack) - 1)
        self.zoomOutButton.setEnabled(True)
        self.zoomOutButton.show()
        self.refreshPixmap()

    @QtCore.Slot()
    def zoomOut(self):
        self.curZoom -= 1
        self.zoomOutButton.setEnabled(self.curZoom > 0)
        self.zoomInButton.setEnabled(True)
        self.zoomInButton.show()
        self.refreshPixmap()

    def paintEvent(self, event):
        # 미리 작성된 pixmap 을 위젯의 (0, 0)위치에 복사
        painter = QtGui.QStylePainter(self)
        painter.drawPixmap(0, 0, self.pixmap)

        if self.rubberBandIsShown:
            painter.setPen(self.palette().light().color())
            painter.drawRect(self.rubberBandRect.normalized().adjusted(0, 0, -1, -1))

            if self.hasFocus():
                option = QtGui.QStyleOptionFocusRect()
                option.initFrom(self)
                option.backgroundColor = self.palette().dark().color()
                # self.style().drawPrimitive(QtGui.QStyle.PE_FrameFocusRect, option, painter, self)
                painter.drawPrimitive(QtGui.QStyle.PE_FrameFocusRect, option)

    def resizeEvent(self, event):
        x = self.width() - (self.zoomInButton.width() + self.zoomOutButton.width() + 10)
        self.zoomInButton.move(x, 5)
        self.zoomOutButton.move(x + self.zoomInButton.width() + 5, 5)
        self.refreshPixmap()

    def mousePressEvent(self, event):
        rect = QtCore.QRect(self.margin, self.margin,
                            self.width() - 2 * self.margin, self.height() - 2 * self.margin)

        if event.button() == QtCore.Qt.LeftButton:
            if rect.contains(event.pos()):
                self.rubberBandIsShown = True
                self.rubberBandRect.setTopLeft(event.pos())
                self.rubberBandRect.setBottomRight(event.pos())
                self.updateRubberBendRegion()
                self.setCursor(QtCore.Qt.CrossCursor)

    def mouseMoveEvent(self, event):
        if self.rubberBandIsShown:
            self.updateRubberBendRegion()
            self.rubberBandRect.setBottomRight(event.pos())
            self.updateRubberBendRegion()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.rubberBandIsShown:
            self.rubberBandIsShown = False
            self.updateRubberBendRegion()
            self.unsetCursor()

            rect = self.rubberBandRect.normalized()
            if rect.width() < 4 or rect.height() < 4:
                return
            rect.translate(-self.margin, -self.margin)

            prevSettings = self.zoomStack[self.curZoom]
            settings = PlotSettings()
            dx = prevSettings.spanX() / (self.width() - 2 * self.margin)
            dy = prevSettings.spanY() / (self.height() - 2 * self.margin)
            settings.minX = prevSettings.minX + dx * rect.left()
            settings.maxX = prevSettings.minX + dx * rect.right()
            settings.minY = prevSettings.maxY - dy * rect.bottom()
            settings.maxY = prevSettings.maxY - dy * rect.top()
            settings.adjust()

            self.zoomStack = self.zoomStack[:self.curZoom + 1]
            self.zoomStack.append(settings)
            self.zoomIn()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Plus:
            self.zoomIn()
        elif event.key() == QtCore.Qt.Key_Minus:
            self.zoomOut()
        elif event.key() == QtCore.Qt.Key_Left:
            self.zoomStack[self.curZoom].scroll(-1, 0)
            self.refreshPixmap()
        elif event.key() == QtCore.Qt.Key_Right:
            self.zoomStack[self.curZoom].scroll(+1, 0)
            self.refreshPixmap()
        elif event.key() == QtCore.Qt.Key_Down:
            self.zoomStack[self.curZoom].scroll(0, -1)
            self.refreshPixmap()
        elif event.key() == QtCore.Qt.Key_Up:
            self.zoomStack[self.curZoom].scroll(0, +1)
            self.refreshPixmap()
        else:
            QtGui.QWidget.keyPressEvent(event)

    def wheelEvent(self, event):
        numDegrees = event.delta() / 8
        numTicks = numDegrees / 15

        if event.orientation() == QtCore.Qt.Horizontal:
            self.zoomStack[self.curZoom].scroll(numTicks, 0)
        else:
            self.zoomStack[self.curZoom].scroll(0, numTicks)

        self.refreshPixmap()

    def updateRubberBendRegion(self):
        rect = self.rubberBandRect.normalized()
        self.update(rect.left(), rect.top(), rect.width(), 1)
        self.update(rect.left(), rect.top(), 1, rect.height())
        self.update(rect.left(), rect.bottom(), rect.width(), 1)
        self.update(rect.right(), rect.top(), 1, rect.height())

    def refreshPixmap(self):
        if not self.width() or not self.height():
            return
        self.pixmap = QtGui.QPixmap(self.size())
        self.pixmap.fill(self, 0, 0)
        painter = QtGui.QPainter(self.pixmap)
        painter.initFrom(self)
        self.drawGrid(painter)
        self.drawCurves(painter)
        self.update()

    def drawGrid(self, painter):
        rect = QtCore.QRect(self.margin, self.margin,
                            self.width() - self.margin * 2,
                            self.height() - self.margin * 2)
        if not rect.isValid():
            return

        settings = self.zoomStack[self.curZoom]
        quiteDark = self.palette().dark().color()
        light = self.palette().light().color()

        for i in range(settings.numXTicks + 1):
            x = rect.left() + (i * (rect.width() - 1) / settings.numXTicks)
            label = settings.minX + (i * settings.spanX() / settings.numXTicks)

            painter.setPen(quiteDark)
            painter.drawLine(x, rect.top(), x, rect.bottom())
            painter.setPen(light)
            painter.drawLine(x, rect.bottom(), x, rect.bottom() + 5)
            painter.drawText(x - 50, rect.bottom() + 5, 100, 20,
                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop,
                             unicode(round(label, 3)))

        for j in range(settings.numYTicks + 1):
            y = rect.bottom() - (j * (rect.height() - 1) / settings.numYTicks)
            label = settings.minY + (j * settings.spanY() / settings.numYTicks)
            painter.setPen(light)
            painter.drawLine(rect.left() - 5, y, rect.left(), y)
            # drawText 의 인자는 x, y, width, height, alignment, text
            painter.drawText(rect.left() - self.margin, y - 10, self.margin - 5, 20,
                             QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
                             unicode(round(label, 3)))

        painter.drawRect(rect.adjusted(0, 0, -1, -1))

    def drawCurves(self, painter):
        colorForIds = [QtCore.Qt.red, QtCore.Qt.green, QtCore.Qt.blue,
                       QtCore.Qt.cyan, QtCore.Qt.magenta, QtCore.Qt.yellow]

        settings = self.zoomStack[self.curZoom]

        rect = QtCore.QRect(self.margin, self.margin,
                            self.width() - 2 * self.margin,
                            self.height() - 2 * self.margin)

        if not rect.isValid():
            return

        painter.setClipRect(rect.adjusted(+1, +1, -1, -1))

        for k, v in self.curveMap.iteritems():
            _id = k
            data = map(lambda (x, y): QtCore.QPointF(x, y), v)
            polyline = QtGui.QPolygonF(len(data))

            for j in range(len(data)):
                dx = data[j].x() - settings.minX
                dy = data[j].y() - settings.minY
                x = rect.left() + (dx * (rect.width() - 1) / settings.spanX())
                y = rect.bottom() - (dy * (rect.height() - 1) / settings.spanY())
                polyline[j] = QtCore.QPointF(x, y)

            painter.setPen(colorForIds[int(_id) % 6])
            painter.drawPolyline(polyline)


class PlotSettings:

    def __init__(self):
        self.minX = 0.0
        self.maxX = 10.0
        self.numXTicks = 5
        self.minY = 0.0
        self.maxY = 10.0
        self.numYTicks = 5

    def scroll(self, dx, dy):
        stepX = self.spanX() / self.numXTicks
        self.minX += dx * stepX
        self.maxX += dx * stepX

        stepY = self.spanY() / self.numYTicks
        self.minY += dy * stepY
        self.maxY += dy * stepY

    def adjust(self):
        self.adjustAxis(self.minX, self.maxX, self.numXTicks)
        self.adjustAxis(self.minY, self.maxY, self.numYTicks)

    def spanX(self):
        return self.maxX - self.minX

    def spanY(self):
        return self.maxY - self.minY

    def adjustAxis(self, _min, _max, numTicks):
        minTicks = 4
        grossStep = (_max - _min) / minTicks
        step = math.pow(10.0, math.floor(math.log10(grossStep)))

        if 5 * step < grossStep:
            step *= 5
        elif 2 * step < grossStep:
            step *= 2

        numTicks = int(math.ceil(_max / step) - math.floor(_min / step))
        if numTicks < minTicks:
            numTicks = minTicks
        _min = math.floor(_min / step) * step
        _max = math.floor(_max / step) * step




if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    win = Plotter()

    win.show()

    sys.exit(app.exec_())
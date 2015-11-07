# coding: utf-8
# author: wie@ppi.co.jp

#topic/wie edits2


# master edits

from PySide import QtGui, QtCore


class Plotter(QtGui.QWidget):
    """Plotter and Double buffering examples"""

    def __init__(self, parent=None):
        super(Plotter, self).__init__(parent)

        self.zoomInButton
        self.zoomOutButton
        self.curveMap
        self.zoomStack
        self.curZoom
        self.rubberBandIsShown
        self.rubberBandRect
        self.pixmap


    def setPlotSettings(self, settings):
        pass

    def setCurveData(self, _id, data):
        pass

    def clearCurve(self, _id):
        pass

    def minimumSizeHint(self, *args, **kwargs):
        size = None
        return size

    def sizeHint(self, *args, **kwargs):
        size = None
        return size

    @QtCore.Slot()
    def zoomIn(self):
        pass

    @QtCore.Slot()
    def zoomOut(self):
        pass

    def paintEvent(self, event):
        pass

    def resizeEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def keyPressEvent(self, event):
        pass

    def wheelEvent(self, event):
        pass

    def updateRubberBendRegion(self):
        pass

    def refreshPixmap(self):
        pass

    def drawGrid(self, painter):
        pass

    def drawCurves(self, painter):
        pass


class PlotSettings:

    def __init__(self):
        self.minY = None
        self.maxY = None
        self.minX = None
        self.maxX = None
        self.numXTicks = None
        self.numYTicks = None

    def scroll(self, dx, dy):
        pass

    def adjust(self):
        pass

    def spanX(self):
        return self.maxX - self.minX

    def spanY(self):
        return self.maxY - self.minY

    def adjustAxis(self, _min, _max, numTicks):
        pass


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    win = Plotter()

    win.show()

    sys.exit(app.exec_())
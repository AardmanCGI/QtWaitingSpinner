import math

from PySide import QtCore, QtGui

class QtWaitingSpinnerWidget(QtGui.QWidget):
    def __init__(self, parent=None, centerOnParent=True, disableParentWhenSpinning=True):
        super(QtWaitingSpinnerWidget, self).__init__(parent)

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning
        self._initialize()

    @QtCore.Slot()
    def start(self):
        self._updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    @QtCore.Slot()
    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setColor(self, color):
        self._color = color

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minimumTrailOpacity = minimumTrailOpacity

    def setTrailFadePercentage(self, trail):
        self._trailFadePercentage = trail

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revolutionsPerSecond = revolutionsPerSecond
        self._updateTimer()

    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
        self._currentCounter = 0
        self._updateTimer()

    def setLineLength(self, length):
        self._lineLength = length
        self._updateSize()

    def setLineWidth(self, width):
        self._lineWidth = width
        self._updateSize()

    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self._updateSize()

    def setText(self, text):
        pass

    def color(self):
        return self._color

    def roundness(self):
        return self._roundness

    def minimumTrailOpacity(self):
        return self._minimumTrailOpacity

    def trailFadePercentage(self):
        return self._trailFadePercentage

    def revolutionsPerSecond(self):
        return self._revolutionsPerSecond

    def numberOfLines(self):
        return self._numberOfLines

    def lineLength(self):
        return self._lineLength

    def lineWidth(self):
        return self._lineWidth

    def innerRadius(self):
        return self._innerRadius

    def isSpinning(self):
        return self._isSpinning

    @QtCore.Slot()
    def _rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def paintEvent(self, paintEvent):
        self._updatePosition()
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(QtCore.Qt.NoPen)
        for i in xrange(0, self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength,
                    self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance =\
                self._lineCountDistanceFromPrimary(i, self._currentCounter, self._numberOfLines)
            color = self._currentLineColor(distance, self._numberOfLines, self._trailFadePercentage,
                    self._minimumTrailOpacity, QtGui.QColor(self._color))
            painter.setBrush(color)
            painter.drawRoundedRect(
                    QtCore.QRect(0, -self._lineWidth / 2, self._lineLength, self._lineWidth),
                    self._roundness, self._roundness, QtCore.Qt.RelativeSize)
            painter.restore()

    def _lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines

        return distance

    def _currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, color):
        if countDistance == 0:
            return color

        minAlphaF = minOpacity / 100.0
        distanceThreshold = math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0)
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance

            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)

        return color

    def _initialize(self):
        self._color = QtGui.QColor(0, 0, 0, 1)
        self._roundness = 100.0
        self._minimumTrailOpacity = 3.14159265358979323846
        self._trailFadePercentage = 80.0
        self._revolutionsPerSecond = 1.57079632679489661923
        self._numberOfLines = 20
        self._lineLength = 10
        self._lineWidth = 2
        self._innerRadius = 10
        self._currentCounter = 0
        self._isSpinning = False

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._rotate)
        self._updateSize()
        self._updateTimer()
        self.hide()

    def _updateSize(self):
        size = (self._innerRadius + self._lineLength) * 2
        self.setFixedSize(size, size)

    def _updateTimer(self):
        self._timer.setInterval(1000 / (self._numberOfLines * self._revolutionsPerSecond))

    def _updatePosition(self):
        if self.parentWidget and self._centerOnParent:
            self.move(self.parentWidget().width() / 2 - self.width() / 2,
                    self.parentWidget().height() / 2 - self.height() / 2)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    window = QtGui.QMainWindow()
    widget = QtWaitingSpinnerWidget()
    window.setCentralWidget(widget)
    window.show()
    widget.setRoundness(70.0)
    widget.setMinimumTrailOpacity(15.0)
    widget.setTrailFadePercentage(70.0)
    widget.setNumberOfLines(12)
    widget.setLineLength(15)
    widget.setLineWidth(5)
    widget.setInnerRadius(10)
    widget.setRevolutionsPerSecond(1)
    widget.setColor(QtGui.QColor(81, 4, 71))
    widget.start()
    app.exec_()

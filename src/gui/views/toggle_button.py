from qt_core import *
class ToggleButton(QCheckBox):
    def __init__(self, checkedColor=QColor(60, 200, 180), uncheckedColor=QColor(200, 100, 120)):
        super().__init__()
        self.setFixedHeight(24)
        self._handlePositionMultiplier = 0.0
        self._checkedColor = checkedColor
        self._uncheckedColor = uncheckedColor

        # -- ANIMATION --
        self._animation = QPropertyAnimation(self, b"handlePositionMultiplier")
        self._animation.setEasingCurve(QEasingCurve.InOutCubic)
        self._animation.setDuration(200)
        self.stateChanged.connect(self._onStateChanged)

    def _onStateChanged(self, state):
        self._animation.stop()
        self._animation.setEndValue(1 if state else 0)
        self._animation.start()

    # --  INTERATIONS --
    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.contentsRect()
        radius = rect.height() / 2

        if self.isChecked():
            painter.setBrush(QBrush(self._checkedColor.lighter(150)))
        else:
            painter.setBrush(QBrush(self._uncheckedColor.lighter(150)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        travel = rect.width() - 2 * radius
        posX = rect.x() + radius + travel * self._handlePositionMultiplier
        posY = rect.center().y()
        handleRadius = radius * 0.8

        painter.setBrush(QBrush(Qt.darkGray))
        painter.drawEllipse(QPointF(posX, posY), handleRadius, handleRadius)

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)    

    # -- CONTROLLER -- 
    def getHandlePositionMultiplier(self):
        return self._handlePositionMultiplier

    def setHandlePositionMultiplier(self, value):
        self._handlePositionMultiplier = value
        self.update()

    handlePositionMultiplier = Property(
        float,
        getHandlePositionMultiplier,
        setHandlePositionMultiplier
    )
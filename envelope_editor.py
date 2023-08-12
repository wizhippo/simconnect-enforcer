import sys

from PySide6.QtCore import Qt, QPointF, Slot, Signal
from PySide6.QtGui import QPainter, QMouseEvent, QColor, QPen
from PySide6.QtWidgets import QFrame, QApplication

DISTANCE_THRESHOLD = 0.05


class EnvelopeEditor(QFrame):
    updated = Signal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = [QPointF(0, 0.5), QPointF(1, 0.5)]
        self.dragging = None
        self.highlighted_x = None

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        self.draw_dashed_line(painter)
        self.draw_envelope(painter)
        self.draw_highlighted_dot(painter)

    def draw_dashed_line(self, painter: QPainter):
        pen = QPen(QColor(128, 128, 128))
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(0, self.height() / 2, self.width(), self.height() / 2)

    def draw_envelope(self, painter: QPainter):
        pen = QPen(QColor(0, 128, 255), 2)
        painter.setPen(pen)
        for i in range(len(self.points) - 1):
            p1, p2 = self.to_widget_coords(self.points[i]), self.to_widget_coords(self.points[i + 1])
            painter.drawLine(p1, p2)
        for point in self.points:
            painter.setBrush(QColor(255, 0, 0) if point == self.dragging else QColor(255, 255, 255))
            painter.drawEllipse(self.to_widget_coords(point), 5, 5)

    def draw_highlighted_dot(self, painter: QPainter):
        if self.highlighted_x is not None:
            widget_x = self.highlighted_x * self.width()
            y_value = self.interpolate_y_value(self.highlighted_x)
            widget_y = (1 - y_value) * self.height()
            painter.setBrush(QColor(0, 255, 0))
            painter.drawEllipse(QPointF(widget_x, widget_y), 7, 7)

    def to_widget_coords(self, point: QPointF) -> QPointF:
        return QPointF(point.x() * self.width(), (1 - point.y()) * self.height())

    def to_logic_coords(self, point: QPointF) -> QPointF:
        return QPointF(point.x() / self.width(), 1 - point.y() / self.height())

    def point_near(self, pt1: QPointF, pt2: QPointF) -> bool:
        return abs(pt1.x() - pt2.x()) < DISTANCE_THRESHOLD and abs(pt1.y() - pt2.y()) < DISTANCE_THRESHOLD

    def adjust_point(self, point: QPointF, x: float, y: float):
        if point != self.points[0] and point != self.points[-1]:
            point.setX(x)
        point.setY(max(0, min(1, y)))
        self.points.sort(key=lambda p: p.x())
        self.emit_updated_signal()
        self.update()

    def emit_updated_signal(self):
        self.updated.emit([(p.x(), p.y()) for p in self.points])

    def mousePressEvent(self, event: QMouseEvent):
        logic_pos = self.to_logic_coords(event.position())
        for point in self.points:
            if self.point_near(point, logic_pos):
                if event.button() == Qt.LeftButton:
                    self.dragging = point
                elif event.button() == Qt.RightButton:
                    self.delete_point(point)
                return
        if event.button() == Qt.LeftButton:
            new_point = QPointF(*logic_pos.toTuple())
            self.points.append(new_point)
            self.points.sort(key=lambda p: p.x())
            self.dragging = new_point  # Set the dragging point to the new point
            self.emit_updated_signal()
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.dragging:
            return
        logic_pos = self.to_logic_coords(event.position())
        if self.points[0].x() < logic_pos.x() < self.points[-1].x():
            self.adjust_point(self.dragging, *logic_pos.toTuple())

    def mouseReleaseEvent(self, _):
        self.dragging = None
        self.update()

    def delete_point(self, point_to_remove: QPointF):
        if point_to_remove in (self.points[0], self.points[-1]):
            return
        self.points.remove(point_to_remove)
        self.emit_updated_signal()
        self.update()

    def interpolate_y_value(self, x_value: float) -> float:
        for i in range(len(self.points) - 1):
            p1, p2 = self.points[i], self.points[i + 1]
            if p1.x() <= x_value <= p2.x():
                return p1.y() + (x_value - p1.x()) * (p2.y() - p1.y()) / max(p2.x() - p1.x(), 1e-6)
        return 0.5

    def highlight_dot(self, x_value: float):
        self.highlighted_x = x_value
        self.update()

    @Slot(list)
    def setPoints(self, points):
        if type(points) == list:
            if len(points) == 1:
                self.points = [QPointF(0, points[0]), QPointF(1, points[0])]
            else:
                self.points = list(map(lambda p: QPointF(p[0], p[1]), points))
        else:
            self.points = [QPointF(0, points), QPointF(1, points)]
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EnvelopeEditor()
    window.setWindowTitle('Envelope Editor')
    window.resize(600, 400)
    window.show()
    window.highlight_dot(0.67)
    sys.exit(app.exec())

import sys

from PySide6 import QtWidgets, QtGui, QtCore


class MiniMapView(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setFixedHeight(50)
        self.setMouseTracking(True)
        self.dragging = False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(30, 30, 30))

        if not self.editor.points:
            return

        waveform_pen = QtGui.QPen(QtGui.QColor("lime"), 1)
        painter.setPen(waveform_pen)

        points = self.editor.points
        total_width = points[-1].x()
        height = self.height()

        for i in range(len(points) - 1):
            x1 = points[i].x() / total_width * self.width()
            x2 = points[i + 1].x() / total_width * self.width()
            y1 = height / 2 - points[i].y() / 400 * (height / 2)
            y2 = height / 2 - points[i + 1].y() / 400 * (height / 2)
            painter.drawLine(x1, y1, x2, y2)

        view = self.editor.view
        view_start = self.editor.pan_x / self.editor.total_content_width() * self.width()
        view_width = view.width() / self.editor.total_content_width() * self.width()

        view_rect = QtCore.QRectF(view_start, 0, view_width, self.height())
        highlight_pen = QtGui.QPen(QtGui.QColor("cyan"), 2)
        highlight_brush = QtGui.QBrush(QtGui.QColor(0, 255, 255, 40))
        painter.setPen(highlight_pen)
        painter.setBrush(highlight_brush)
        painter.drawRect(view_rect)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.dragging = True
            self.jump_to_position(event.position())

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.jump_to_position(event.position())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.dragging = False

    def mouseDoubleClickEvent(self, event):
        self.editor.save_state()
        self.editor.target_zoom_x = self.width() / self.editor.points[-1].x()
        self.editor.target_pan_x = 0
        self.editor.update_scrollbar()
        self.editor.view.refresh_views()

    def jump_to_position(self, pos):
        total_width = self.editor.total_content_width()
        logical_x = (pos.x() / self.width()) * total_width
        center_x = logical_x - (self.editor.view.width() / 2) / self.editor.zoom_x
        self.editor.target_pan_x = center_x * self.editor.zoom_x
        self.editor.update_scrollbar()
        self.editor.view.refresh_views()


class WaveformView(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.dragging_point = False
        self.panning = False
        self.selecting = False
        self.last_pan_pos = None
        self.selection_start_x = None
        self.selection_end_x = None

        self.velocity_x = 0
        self.velocity_y = 0
        self.inertia_timer = QtCore.QTimer()
        self.inertia_timer.timeout.connect(self.apply_inertia)

    def refresh_views(self):
        self.update()
        self.parent().minimap.update()

    def paintEvent(self, event):
        editor = self.parent()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(self.rect(), QtGui.QColor("black"))

        zero_pen = QtGui.QPen(QtGui.QColor("white"), 1)
        painter.setPen(zero_pen)
        painter.drawLine((0 * editor.zoom_x) - editor.pan_x, 0,
                         (0 * editor.zoom_x) - editor.pan_x, self.height())
        painter.drawLine(0, self.map_y(0, editor), self.width(), self.map_y(0, editor))

        self.draw_grid(painter, editor)

        waveform_pen = QtGui.QPen(QtGui.QColor("lime"), 2)
        painter.setPen(waveform_pen)

        for i in range(len(editor.points) - 1):
            p1 = self.map_point(editor.points[i], editor)
            p2 = self.map_point(editor.points[i + 1], editor)
            painter.drawLine(p1, p2)

        brush = QtGui.QBrush(QtGui.QColor("red"))
        painter.setBrush(brush)

        for point in editor.points:
            mapped = self.map_point(point, editor)
            painter.drawEllipse(mapped, 5, 5)

        if self.selecting and self.selection_start_x is not None and self.selection_end_x is not None:
            rect = QtCore.QRectF(
                QtCore.QPointF(min(self.selection_start_x, self.selection_end_x), 0),
                QtCore.QPointF(max(self.selection_start_x, self.selection_end_x), self.height())
            )
            painter.setPen(QtGui.QPen(QtGui.QColor("cyan"), 1, QtCore.Qt.DashLine))
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRect(rect)

    def map_point(self, point, editor):
        x = (point.x() * editor.zoom_x) - editor.pan_x
        y = self.map_y(point.y(), editor)
        return QtCore.QPointF(x, y)

    def map_y(self, y_value, editor):
        center = self.height() / 2
        return center - (y_value * editor.zoom_y) - editor.pan_y

    def map_from_screen(self, pos, editor):
        x = (pos.x() + editor.pan_x) / editor.zoom_x
        center = self.height() / 2
        y = (center - pos.y() - editor.pan_y) / editor.zoom_y
        return QtCore.QPointF(x, y)

    def find_closest_point(self, pos, editor):
        return min(range(len(editor.points)),
                   key=lambda idx: abs(editor.points[idx].x() - pos.x()),
                   default=None)

    def mousePressEvent(self, event):
        editor = self.parent()

        if event.button() == QtCore.Qt.LeftButton:
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                self.selecting = True
                self.selection_start_x = event.position().x()
                self.selection_end_x = event.position().x()
            else:
                # Check distance to nearest point
                logical_pos = self.map_from_screen(event.position(), editor)
                idx = self.find_closest_point(logical_pos, editor)
                if idx is not None:
                    mapped = self.map_point(editor.points[idx], editor)
                    distance = (mapped - event.position()).manhattanLength()

                    if distance < 15:  # threshold (in pixels)
                        editor.save_state(include_points=True)
                        self.dragging_point = True
                    else:
                        # too far, treat as panning
                        self.panning = True
                        self.last_pan_pos = event.position()

        elif event.button() == QtCore.Qt.MiddleButton:
            self.panning = True
            self.last_pan_pos = event.position()

    def mouseMoveEvent(self, event):
        editor = self.parent()
        pos = event.position()

        if self.dragging_point and not self.panning and not self.selecting:
            logical_pos = self.map_from_screen(pos, editor)
            idx = self.find_closest_point(logical_pos, editor)
            if idx is not None:
                snap_y = 25
                snapped_y = round(logical_pos.y() / snap_y) * snap_y
                editor.points[idx].setY(snapped_y)
                self.refresh_views()

        if self.panning and self.last_pan_pos:
            delta = pos - self.last_pan_pos
            editor.pan_x -= delta.x()
            editor.pan_y -= delta.y()
            editor.target_pan_x = editor.pan_x
            editor.update_scrollbar()
            self.velocity_x = delta.x()
            self.velocity_y = delta.y()
            self.last_pan_pos = pos
            self.refresh_views()

        if self.selecting:
            self.selection_end_x = pos.x()
            self.refresh_views()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.selecting:
                self.finish_rubberband_zoom()

            # Always stop dragging and selecting cleanly
            self.dragging_point = False
            self.selecting = False
            self.panning = False
            self.last_pan_pos = None

        elif event.button() == QtCore.Qt.MiddleButton:
            self.panning = False
            self.last_pan_pos = None

            if abs(self.velocity_x) > 0.5 or abs(self.velocity_y) > 0.5:
                self.inertia_timer.start(16)

    def finish_rubberband_zoom(self):
        editor = self.parent()
        editor.save_state()

        if self.selection_start_x is None or self.selection_end_x is None:
            return

        start_x = min(self.selection_start_x, self.selection_end_x)
        end_x = max(self.selection_start_x, self.selection_end_x)

        if abs(end_x - start_x) < 10:
            return

        logical_start = (start_x + editor.pan_x) / editor.zoom_x
        logical_end = (end_x + editor.pan_x) / editor.zoom_x

        selected_width = logical_end - logical_start
        if selected_width <= 0:
            return

        new_zoom = editor.view.width() / selected_width
        new_pan = logical_start * new_zoom

        editor.target_zoom_x = new_zoom
        editor.target_pan_x = new_pan

        editor.update_scrollbar()
        self.selection_start_x = None
        self.selection_end_x = None
        self.refresh_views()

    def apply_inertia(self):
        editor = self.parent()

        if abs(self.velocity_x) < 0.1 and abs(self.velocity_y) < 0.1:
            self.inertia_timer.stop()
            self.velocity_x = 0
            self.velocity_y = 0

            total_width = editor.total_content_width()
            view_width = self.width()
            max_pan_x = max(0, total_width - view_width)

            if editor.pan_x < 0:
                editor.pan_x += (-editor.pan_x) * 0.2
            if editor.pan_x > max_pan_x:
                editor.pan_x -= (editor.pan_x - max_pan_x) * 0.2

            editor.target_pan_x = editor.pan_x
            editor.update_scrollbar()
            self.refresh_views()
            return

        editor.pan_x -= self.velocity_x
        editor.pan_y -= self.velocity_y
        editor.target_pan_x = editor.pan_x
        editor.update_scrollbar()

        self.velocity_x *= 0.9
        self.velocity_y *= 0.9
        self.refresh_views()

    def draw_grid(self, painter, editor):
        grid_pen = QtGui.QPen(QtGui.QColor(100, 100, 100), 1, QtCore.Qt.DashLine)
        painter.setPen(grid_pen)
        font = QtGui.QFont()
        font.setPointSize(8)
        painter.setFont(font)

        x_spacing = 100
        y_spacing = 50

        width = self.width()
        height = self.height()
        center = height / 2

        start_x = (editor.pan_x / editor.zoom_x) // x_spacing * x_spacing
        end_x = (editor.pan_x + width) / editor.zoom_x

        x = start_x
        while x < end_x:
            screen_x = (x * editor.zoom_x) - editor.pan_x
            painter.drawLine(screen_x, 0, screen_x, height)
            painter.drawText(screen_x + 2, height - 4, f"{int(x)}")
            x += x_spacing

        top_logical = (center - 0) / editor.zoom_y
        bottom_logical = (center - height) / editor.zoom_y

        y = (bottom_logical // y_spacing) * y_spacing
        while y <= top_logical:
            screen_y = self.map_y(y, editor)
            painter.drawLine(0, screen_y, width, screen_y)
            painter.drawText(2, screen_y - 2, f"{int(y)}")
            y += y_spacing

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.parent().update_zoom_y()


class WaveformEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.zoom_x = 1.0
        self.zoom_y = 1.0
        self.target_zoom_x = self.zoom_x
        self.pan_x = 0
        self.pan_y = 0
        self.target_pan_x = self.pan_x
        self.auto_zoom_y_enabled = True

        self.points = [QtCore.QPointF(x, 0) for x in range(0, 5000, 50)]

        self.undo_stack = []
        self.redo_stack = []

        self.view = WaveformView(self)
        self.minimap = MiniMapView(self)
        self.scrollbar = QtWidgets.QScrollBar(QtCore.Qt.Orientation.Horizontal)
        self.scrollbar.setSingleStep(20)
        self.scrollbar.valueChanged.connect(self.on_scrollbar_changed)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.view)
        layout.addWidget(self.minimap)
        layout.addWidget(self.scrollbar)

        self.anim_timer = QtCore.QTimer()
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(16)

        self.update_scrollbar()

    def save_state(self, include_points=False):
        state = {
            'pan_x': self.pan_x,
            'zoom_x': self.zoom_x,
        }
        if include_points:
            state['points'] = [QtCore.QPointF(p.x(), p.y()) for p in self.points]
        self.undo_stack.append(state)
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            state = self.undo_stack.pop()
            self.redo_stack.append({
                'pan_x': self.pan_x,
                'zoom_x': self.zoom_x,
                'points': [QtCore.QPointF(p.x(), p.y()) for p in self.points]
            })

            self.pan_x = state['pan_x']
            self.zoom_x = state['zoom_x']
            self.target_pan_x = self.pan_x
            self.target_zoom_x = self.zoom_x
            if 'points' in state:
                self.points = [QtCore.QPointF(p.x(), p.y()) for p in state['points']]
            self.update_scrollbar()
            self.view.refresh_views()

    def redo(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append({
                'pan_x': self.pan_x,
                'zoom_x': self.zoom_x,
                'points': [QtCore.QPointF(p.x(), p.y()) for p in self.points]
            })

            self.pan_x = state['pan_x']
            self.zoom_x = state['zoom_x']
            self.target_pan_x = self.pan_x
            self.target_zoom_x = self.zoom_x
            if 'points' in state:
                self.points = [QtCore.QPointF(p.x(), p.y()) for p in state['points']]
            self.update_scrollbar()
            self.view.refresh_views()

    def total_content_width(self):
        return (self.points[-1].x() if self.points else self.width()) * self.zoom_x

    def update_scrollbar(self):
        total_width = self.total_content_width()
        page_step = self.view.width()
        max_scroll = max(0, total_width - page_step)
        self.scrollbar.setRange(0, int(max_scroll))
        self.scrollbar.setPageStep(int(page_step))
        self.scrollbar.setValue(int(self.pan_x))
        self.minimap.update()

    def on_scrollbar_changed(self, value):
        self.pan_x = value
        self.target_pan_x = value
        self.view.refresh_views()

    def wheelEvent(self, event):
        if abs(event.angleDelta().x()) > abs(event.angleDelta().y()):
            self.pan_x -= event.angleDelta().x() * 0.2
            self.target_pan_x = self.pan_x
        elif event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            factor = 1.1 if event.angleDelta().y() > 0 else 0.9
            self.zoom_y = max(0.1, min(self.zoom_y * factor, 100.0))
            self.auto_zoom_y_enabled = False
            self.view.refresh_views()
        elif event.modifiers() == QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.pan_y -= event.angleDelta().y() * 0.2
        else:
            pos = event.position()
            old_x = (pos.x() + self.pan_x) / self.zoom_x
            factor = 1.1 if event.angleDelta().y() > 0 else 0.9
            new_zoom = max(0.1, min(self.zoom_x * factor, 10.0))
            new_pan = old_x * new_zoom - pos.x()
            self.target_zoom_x = new_zoom
            self.target_pan_x = new_pan

        self.update_scrollbar()
        self.view.refresh_views()

    def update_animation(self):
        changed = False
        if abs(self.zoom_x - self.target_zoom_x) > 0.001:
            self.zoom_x += (self.target_zoom_x - self.zoom_x) * 0.2
            changed = True
        if abs(self.pan_x - self.target_pan_x) > 0.5:
            self.pan_x += (self.target_pan_x - self.pan_x) * 0.2
            changed = True
        if changed:
            self.update_scrollbar()
            self.view.refresh_views()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_scrollbar()

    def get_logical_y_range(self):
        if not self.points:
            return 1
        return max(abs(p.y()) for p in self.points)

    def update_zoom_y(self):
        if not self.auto_zoom_y_enabled:
            return

        max_logical_y = self.get_logical_y_range()
        if max_logical_y == 0:
            max_logical_y = 1

        half_height = self.view.height() / 2
        self.zoom_y = half_height / (max_logical_y * 1.1)
        self.view.refresh_views()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waveform Editor")
        self.editor = WaveformEditor()
        self.setCentralWidget(self.editor)

        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+0"), self, self.reset_zoom)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self, self.undo)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Shift+Z"), self, self.redo)

    def reset_zoom(self):
        self.editor.auto_zoom_y_enabled = True
        self.editor.update_zoom_y()

    def undo(self):
        self.editor.undo()

    def redo(self):
        self.editor.redo()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

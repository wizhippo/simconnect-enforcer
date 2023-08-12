import math
import sys

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsView, \
    QGraphicsScene


class UIVector(QWidget):
    vector_updated = Signal(float, float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.magnitude = 0
        self.angle_deg = 0

        # Graphics view
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.graphics_view)
        self.setLayout(layout)

    @Slot(float, float)
    def update_vector(self, magnitude, angle_deg):
        self.magnitude = magnitude
        self.angle_deg = angle_deg
        self.update()

    def paintEvent(self, event):
        # Calculate the end point
        angle_rad = math.radians(90 - self.angle_deg)  # 0 degrees should be North
        end_x = self.magnitude * math.cos(angle_rad)
        end_y = -self.magnitude * math.sin(angle_rad)  # Negate since y is flipped in the scene

        # Clear and draw the vector
        self.scene.clear()

        # Draw circle
        self.scene.addEllipse(-1, -1, 2, 2, QPen(Qt.black, 0.01))

        # Adjust pen thickness based on magnitude. For example, base thickness is 0.02 and it scales with magnitude.
        line_thickness = 0.02 + self.magnitude * 0.05

        # Draw vector
        self.scene.addLine(0, 0, end_x, end_y, QPen(Qt.red, line_thickness))

        # Ensure the view is correctly scaled
        self.graphics_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UIVector()
    window.resize(500, 500)
    window.show()
    sys.exit(app.exec())

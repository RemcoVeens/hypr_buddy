import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMenu
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QPixmap, QAction
from hyprpy import Hyprland


class DesktopBuddy(QMainWindow):
    def __init__(self, character_img: str = "static/demo_char.png"):
        super().__init__()

        self.setWindowTitle("Desktop Buddy")
        self.setGeometry(100, 100, 100, 100)  # Initial position and size

        # Set window flags for frameless, always-on-top, and transparent background
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.BypassWindowManagerHint  # Hint for window managers like Hyprland
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # --- Sprite Setup ---
        self.sprite_label = QLabel(self)
        self.pixmap = QPixmap(character_img)
        if self.pixmap.isNull():
            print("Error: Could not load sprite image. Please check the path.")
            self.pixmap = QPixmap(100, 100)
            self.pixmap.fill(
                Qt.GlobalColor.red
            )  # Fill with red for visibility if image fails

        self.sprite_label.setPixmap(
            self.pixmap.scaled(
                100,
                100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.sprite_label.resize(self.pixmap.width(), self.pixmap.height())
        self.setFixedSize(self.sprite_label.size())  # Set window size to sprite size
        self.hyprctl = Hyprland()

        # --- Animation Setup ---
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.animate_sprite)
        self.speed = 1  # Pixels per step
        self.direction = 1  # 1 for right, -1 for left
        self.animation_timer.start(50)  # Update every 50 milliseconds

        # --- Mouse Interaction ---
        self.dragging = False
        self.offset = QPoint()

    def animate_sprite(self):
        # Simple horizontal movement
        current_pos = self.pos()
        new_x = current_pos.x() + self.speed * self.direction

        # Reverse direction if hitting screen edges
        screen_rect = self.screen().geometry()
        if new_x + self.width() > screen_rect.width() or new_x < 0:
            self.direction *= -1

        self.move(new_x, current_pos.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        quit_action = QAction("Quit Buddy", self)
        quit_action.triggered.connect(self.close)
        context_menu.addAction(quit_action)
        context_menu.exec(event.globalPosition().toPoint())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    buddy = DesktopBuddy()
    buddy.show()

    sys.exit(app.exec())

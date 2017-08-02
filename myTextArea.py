from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QPoint


class TextArea(QTextEdit):
    def __init__(self):
        QTextEdit.__init__(self)
        self.setMouseTracking(True)
        self.se = None

    def mousePressEvent(self, event):
        point = QPoint(event.x(), event.y())
        cursor = self.cursorForPosition(point)
        for val in self.se.getCursorPoints():
            if val[0] < cursor.position() < val[1]:
                print(self.se.getComments()[val])

        self.setTextCursor(cursor)

    def mouseMoveEvent(self, event):
        point = QPoint(event.x(), event.y())
        cursor = self.cursorForPosition(point)
        for val in self.se.getCursorPoints():
            if val[0] < cursor.position() < val[1]:
                print(self.se.getComments()[val])

    def setSE(self, se):
        self.se = se

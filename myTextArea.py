from PyQt5.QtWidgets import QTextEdit, QToolTip
from PyQt5.QtCore import QPoint, QTimer


class TextArea(QTextEdit):
    """Class that implements QTextEdit class"""
    def __init__(self):
        QTextEdit.__init__(self)
        self.setMouseTracking(True)
        self.se = None
        self.categoryGrid = None

        self.textEditContainer = []

        self.setStyleSheet('QTextEdit {font-family: Segoe UI; font-size: 14pt;}')

    def mousePressEvent(self, event):
        """Overrides native method and adds possibility
        to show comments for selected word when click"""
        point = QPoint(event.x(), event.y())
        cursor = self.cursorForPosition(point)
        font = cursor.blockCharFormat().font()

        if len(self.textEditContainer) > 0:
            for value in self.textEditContainer:
                value.deleteLater()

            self.textEditContainer.clear()

        for val in self.se.getCursorPoints():
            if val[0] < cursor.position() < val[1]:
                textEdit = QTextEdit()
                textEdit.insertPlainText(self.se.getComments()[val])
                textEdit.setMaximumWidth(300)
                self.categoryGrid.addWidget(textEdit)

                self.se.selectedTextDemark(val)

                self.textEditContainer.append(textEdit)

        self.setTextCursor(cursor)
        QTextEdit.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        """Overrides native method and adds possibility
        to show comments for selected word when move mouse above
        the word or expression"""
        point = QPoint(event.x(), event.y())
        cursor = self.cursorForPosition(point)
        hint = ''
        timer = QTimer()

        for val in self.se.getCursorPoints():
            if val[0] < cursor.position() < val[1]:
                hint += self.se.getComments()[val] + '\n'
                QToolTip.showText(event.globalPos(), hint)
                timer.singleShot(1500, QToolTip.hideText)

        QTextEdit.mouseMoveEvent(self, event)

    def setSE(self, se):
        self.se = se

    def setCategoryGrid(self, grid):
        self.categoryGrid = grid

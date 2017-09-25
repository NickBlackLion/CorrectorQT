from PyQt5.QtWidgets import QTextEdit, QToolTip
from PyQt5.QtCore import QPoint, QTimer
import logging
import copy


class TextArea(QTextEdit):
    """Class that implements QTextEdit class"""
    def __init__(self):
        QTextEdit.__init__(self)
        self.setMouseTracking(True)
        self.se = None
        self.categoryGrid = None

        self.textEditContainer = []
        self.worked = {}
        self.fixedPoints = []

        self.setStyleSheet('QTextEdit {font-family: Segoe UI; font-size: 14pt;}')
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.currentTextLength = 0

    def mousePressEvent(self, event):
        """Overrides native method and adds possibility
        to show comments for selected word when click"""
        point = QPoint(event.x(), event.y())
        cursor = self.cursorForPosition(point)
        position = copy.copy(cursor.position())

        if len(self.textEditContainer) > 0:
            for value in self.textEditContainer:
                value.deleteLater()

            self.textEditContainer.clear()

        if self.se.getCursorPoints() is not None and len(self.se.getCursorPoints()) > 0:
            for step, val in enumerate(self.se.getCursorPoints()):
                keys = val.split(';')
                coordinates = keys[1].strip('()')
                coordinates = coordinates.split(',')
                coordinate1 = int(coordinates[0])
                coordinate2 = int(coordinates[1])
                if coordinate1 < position < coordinate2:
                    self.fixedPoints.append(val)
                    self.currentTextLength = len(self.toPlainText())
                    textEdit = QTextEdit()
                    textEdit.insertPlainText(self.se.getComments()[val])
                    textEdit.setMaximumWidth(300)
                    self.categoryGrid.addWidget(textEdit)

                    self.se.selectedTextDemark(val, coordinate1)

                    self.textEditContainer.append(textEdit)

        QTextEdit.mousePressEvent(self, event)

        """def mouseMoveEvent(self, event):
        Overrides native method and adds possibility
        to show comments for selected word when move mouse above
        the word or expression
        point = QPoint(event.x(), event.y())
        cursor = self.cursorForPosition(point)
        hint = ''
        timer = QTimer()

        if self.se.getCursorPoints() is not None and len(self.se.getCursorPoints()) > 0:
            for val in self.se.getCursorPoints():
                if val[0] < cursor.position() < val[1]:
                    if self.se.getComments()[val] is not None:
                        hint += self.se.getComments()[val] + '\n'
                        QToolTip.showText(event.globalPos(), hint)
                        timer.singleShot(1500, QToolTip.hideText)

        QTextEdit.mouseMoveEvent(self, event)"""

    def keyPressEvent(self, event):
        self.logger.info('{0}, {1}'.format(self.currentTextLength, len(self.toPlainText())))

        if self.currentTextLength >= len(self.toPlainText()):
            deltaForCurrentPoint = -1
        else:
            deltaForCurrentPoint = 1
        newKeys = {}

        self.logger.info(self.fixedPoints)

        if self.se.getCursorPoints() is not None and len(self.se.getCursorPoints()) > 0:
            for index, value in enumerate(self.se.getCursorPoints()):
                key = value.split(';')
                coordinates = key[1].strip('()')
                coordinates = coordinates.split(',')
                coordinate1 = int(coordinates[0]) + deltaForCurrentPoint
                coordinate2 = int(coordinates[1]) + deltaForCurrentPoint

                boundary = (coordinate1, coordinate2)
                newValue = "{0};{1}".format(key[0], str(boundary))
                newKeys[value] = newValue

        regex = ''
        comment = ''

        for key in newKeys:
            regex = self.se.getRegexes()[key]
            comment = self.se.getComments()[key]

            del self.se.getRegexes()[key]
            del self.se.getComments()[key]

            self.se.getRegexes()[newKeys[key]] = regex
            self.se.getComments()[newKeys[key]] = comment

        self.se.getCursorPoints().clear()
        for key in newKeys:
            self.se.getCursorPoints().append(newKeys[key])

        self.logger.info(self.se.getCursorPoints())

        QTextEdit.keyPressEvent(self, event)

    def setSE(self, se):
        self.se = se

    def setCategoryGrid(self, grid):
        self.categoryGrid = grid

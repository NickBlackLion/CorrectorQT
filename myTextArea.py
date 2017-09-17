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

        self.setStyleSheet('QTextEdit {font-family: Segoe UI; font-size: 14pt;}')
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def mousePressEvent(self, event):
        """Overrides native method and adds possibility
        to show comments for selected word when click"""
        point = QPoint(event.x(), event.y())
        cursor = self.cursorForPosition(point)
        position = copy.copy(cursor.position())
        pointsToDelete = []

        if len(self.textEditContainer) > 0:
            for value in self.textEditContainer:
                value.deleteLater()

            self.textEditContainer.clear()

        if self.se.getCursorPoints() is not None:
            for val in self.se.getCursorPoints():
                self.logger.info(val)

        self.logger.info('\n')

        if self.se.getCursorPoints() is not None and len(self.se.getCursorPoints()) > 0:
            self.logger.info('len before {0}'.format(len(self.se.getCursorPoints())))
            for step, val in enumerate(self.se.getCursorPoints()):
                # self.logger.info('len = {0}'.format(len(self.se.getCursorPoints())))
                keys = val.split(';')
                # self.logger.info(keys)
                coordinates = keys[1].strip('()')
                # self.logger.info(coordinates)
                coordinates = coordinates.split(',')
                # self.logger.info(coordinates)
                coordinate1 = int(coordinates[0])
                coordinate2 = int(coordinates[1])
                # self.logger.info(position)
                if coordinate1 < position < coordinate2:
                    textEdit = QTextEdit()
                    textEdit.insertPlainText(self.se.getComments()[val])
                    textEdit.setMaximumWidth(300)
                    self.categoryGrid.addWidget(textEdit)

                    pointsToDelete.append(val)

                    self.se.selectedTextDemark(val, coordinate1)

                    self.textEditContainer.append(textEdit)

                self.logger.info('step = {0}, value = {1}'.format(step, val))

            for val in pointsToDelete:
                self.se.deletePoints(val)

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

    def setSE(self, se):
        self.se = se

    def setCategoryGrid(self, grid):
        self.categoryGrid = grid

from PyQt5.Qt import QTextOption


class ChangeTextCharacteristics:
    def __init__(self):
        self.flags = None
        self.isPressed = False

    def __addUnprintableCharacters(self, textArea):

        doc = textArea.document()
        options = doc.defaultTextOption()
        self.flags = options.flags()
        options.setFlags(QTextOption.ShowTabsAndSpaces | QTextOption.ShowLineAndParagraphSeparators)
        doc.setDefaultTextOption(options)

    def __deleteUnprintableCharacters(self, textArea):
        doc = textArea.document()
        options = doc.defaultTextOption()
        options.setFlags(self.flags)
        doc.setDefaultTextOption(options)

    def increaseTextSize(self, textArea):
        font = textArea.textCursor().blockCharFormat().font()
        textArea.setStyleSheet('QTextEdit {font-family: ' + font.family() + '; font-size: ' + str(font.pointSize() + 1)
                          + 'pt}')

    def decreaseTextSize(self, textArea):
        font = textArea.textCursor().blockCharFormat().font()
        textArea.setStyleSheet('QTextEdit {font-family: ' + font.family() + '; font-size: ' + str(font.pointSize() - 1)
                                + 'pt}')

    def unprintableCharacters(self, textArea):
        if not self.isPressed:
            self.isPressed = True
            self.__addUnprintableCharacters(textArea)
        else:
            self.isPressed = False
            self.__deleteUnprintableCharacters(textArea)

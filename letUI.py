from btpPySide import *

class FloatMenu(QMenu):
    def __init__(self, menuContent):
        QMenu.__init__(self)
        for curItem in menuContent:
            action=QAction(self)
            action.setText(curItem[0])
            action.triggered.connect(curItem[1])
            self.addAction(action)

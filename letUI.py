from btpPySide import *

class FloatMenu(QMenu):
    def __init__(self, menuContent):
        QMenu.__init__(self)
        for curItem in menuContent:
            action=QAction(self)
            action.setText(curItem[0])
            action.triggered.connect(curItem[1])
            self.addAction(action)

import SelDialogUI
class SelDailog(QDialog):
	def __init__(self,parent=None):
		QDialog.__init__(self,parent)
		self.ui=SelDialogUI.Ui_Dialog()
		self.ui.setupUi(self)

	def AddList(self,items):
		self.ui.listWidget.addItems(items)

	def SelectedItem(self):
		return self.ui.listWidget.currentItem()
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Plotterui.ui'
#
# Created: Thu Oct 11 21:22:46 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Plotterui(object):
    def setupUi(self, Plotterui):
        Plotterui.setObjectName(_fromUtf8("Plotterui"))
        Plotterui.resize(803, 586)
        self.MPLArea = MplWidget(Plotterui)
        self.MPLArea.setGeometry(QtCore.QRect(150, 10, 641, 561))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MPLArea.sizePolicy().hasHeightForWidth())
        self.MPLArea.setSizePolicy(sizePolicy)
        self.MPLArea.setFocusPolicy(QtCore.Qt.NoFocus)
        self.MPLArea.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.MPLArea.setObjectName(_fromUtf8("MPLArea"))
        self.PLOT_Button = QtGui.QPushButton(Plotterui)
        self.PLOT_Button.setGeometry(QtCore.QRect(20, 190, 75, 23))
        self.PLOT_Button.setObjectName(_fromUtf8("PLOT_Button"))
        self.checkTotalInt = QtGui.QCheckBox(Plotterui)
        self.checkTotalInt.setGeometry(QtCore.QRect(11, 101, 62, 17))
        self.checkTotalInt.setChecked(True)
        self.checkTotalInt.setObjectName(_fromUtf8("checkTotalInt"))
        self.checkFlammenhoehe = QtGui.QCheckBox(Plotterui)
        self.checkFlammenhoehe.setGeometry(QtCore.QRect(11, 124, 95, 17))
        self.checkFlammenhoehe.setChecked(True)
        self.checkFlammenhoehe.setObjectName(_fromUtf8("checkFlammenhoehe"))
        self.checkFlammenhoeheGauss = QtGui.QCheckBox(Plotterui)
        self.checkFlammenhoeheGauss.setGeometry(QtCore.QRect(10, 150, 131, 17))
        self.checkFlammenhoeheGauss.setChecked(True)
        self.checkFlammenhoeheGauss.setObjectName(_fromUtf8("checkFlammenhoeheGauss"))

        self.retranslateUi(Plotterui)
        QtCore.QObject.connect(self.PLOT_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), Plotterui.myPlot)
        QtCore.QMetaObject.connectSlotsByName(Plotterui)

    def retranslateUi(self, Plotterui):
        Plotterui.setWindowTitle(QtGui.QApplication.translate("Plotterui", "Plotter", None, QtGui.QApplication.UnicodeUTF8))
        self.PLOT_Button.setText(QtGui.QApplication.translate("Plotterui", "PLOT!", None, QtGui.QApplication.UnicodeUTF8))
        self.checkTotalInt.setText(QtGui.QApplication.translate("Plotterui", "total Int", None, QtGui.QApplication.UnicodeUTF8))
        self.checkFlammenhoehe.setText(QtGui.QApplication.translate("Plotterui", "Flammenhoehe", None, QtGui.QApplication.UnicodeUTF8))
        self.checkFlammenhoeheGauss.setText(QtGui.QApplication.translate("Plotterui", "Flammenhoehe Gauss", None, QtGui.QApplication.UnicodeUTF8))

from mplwidget import MplWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Plotterui = QtGui.QWidget()
    ui = Ui_Plotterui()
    ui.setupUi(Plotterui)
    Plotterui.show()
    sys.exit(app.exec_())


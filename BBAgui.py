# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BBAgui.ui'
#
# Created: Thu Oct 11 21:22:44 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BBA(object):
    def setupUi(self, BBA):
        BBA.setObjectName(_fromUtf8("BBA"))
        BBA.resize(545, 457)
        self.centralwidget = QtGui.QWidget(BBA)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 524, 411))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ImageList = QtGui.QListWidget(self.layoutWidget)
        self.ImageList.setObjectName(_fromUtf8("ImageList"))
        self.verticalLayout.addWidget(self.ImageList)
        self.OpenImages = QtGui.QPushButton(self.layoutWidget)
        self.OpenImages.setObjectName(_fromUtf8("OpenImages"))
        self.verticalLayout.addWidget(self.OpenImages)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.currentImage = QtGui.QLineEdit(self.layoutWidget)
        self.currentImage.setObjectName(_fromUtf8("currentImage"))
        self.verticalLayout_2.addWidget(self.currentImage)
        self.BildViewer = QtGui.QGraphicsView(self.layoutWidget)
        self.BildViewer.setObjectName(_fromUtf8("BildViewer"))
        self.verticalLayout_2.addWidget(self.BildViewer)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        BBA.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(BBA)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 545, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMein_test = QtGui.QMenu(self.menubar)
        self.menuMein_test.setObjectName(_fromUtf8("menuMein_test"))
        BBA.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(BBA)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        BBA.setStatusBar(self.statusbar)
        self.actionOpen_Images = QtGui.QAction(BBA)
        self.actionOpen_Images.setObjectName(_fromUtf8("actionOpen_Images"))
        self.actionOpen_Image_directory = QtGui.QAction(BBA)
        self.actionOpen_Image_directory.setObjectName(_fromUtf8("actionOpen_Image_directory"))
        self.actionClose = QtGui.QAction(BBA)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionOpen_Settings = QtGui.QAction(BBA)
        self.actionOpen_Settings.setObjectName(_fromUtf8("actionOpen_Settings"))
        self.actionOpen_Plotter = QtGui.QAction(BBA)
        self.actionOpen_Plotter.setObjectName(_fromUtf8("actionOpen_Plotter"))
        self.menuMein_test.addAction(self.actionOpen_Images)
        self.menuMein_test.addAction(self.actionOpen_Image_directory)
        self.menuMein_test.addAction(self.actionClose)
        self.menuMein_test.addAction(self.actionOpen_Settings)
        self.menuMein_test.addAction(self.actionOpen_Plotter)
        self.menubar.addAction(self.menuMein_test.menuAction())

        self.retranslateUi(BBA)
        QtCore.QObject.connect(self.actionClose, QtCore.SIGNAL(_fromUtf8("triggered()")), BBA.close)
        QtCore.QObject.connect(self.OpenImages, QtCore.SIGNAL(_fromUtf8("clicked()")), BBA.openImages)
        QtCore.QObject.connect(self.ImageList, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), BBA.filepathClicked)
        QtCore.QObject.connect(self.actionOpen_Settings, QtCore.SIGNAL(_fromUtf8("triggered()")), BBA.openSettings)
        QtCore.QObject.connect(self.actionOpen_Plotter, QtCore.SIGNAL(_fromUtf8("triggered()")), BBA.openPlotter)
        QtCore.QMetaObject.connectSlotsByName(BBA)

    def retranslateUi(self, BBA):
        BBA.setWindowTitle(QtGui.QApplication.translate("BBA", "BBA", None, QtGui.QApplication.UnicodeUTF8))
        self.OpenImages.setText(QtGui.QApplication.translate("BBA", "Open Images", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMein_test.setTitle(QtGui.QApplication.translate("BBA", "Menu", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Images.setText(QtGui.QApplication.translate("BBA", "Open Images", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Image_directory.setText(QtGui.QApplication.translate("BBA", "Open Image directory", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("BBA", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Settings.setText(QtGui.QApplication.translate("BBA", "Open Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Plotter.setText(QtGui.QApplication.translate("BBA", "Open Plotter", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BBA = QtGui.QMainWindow()
    ui = Ui_BBA()
    ui.setupUi(BBA)
    BBA.show()
    sys.exit(app.exec_())


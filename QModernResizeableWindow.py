import sys
from os import path
from pathlib import Path
appMainDir = Path(getattr(sys, "_MEIPASS", path.dirname(path.abspath(__file__))))
try:
    import imp
except:
    imp = None
    pass
try:
    from ResizeableWindow import ResizeableWindow
except:
    try:
        ResizeableWindow = imp.load_source("ResizeableWindow",rf"{appMainDir}\ResizeableWindow.py")
        ResizeableWindow = ResizeableWindow.ResizeableWindow
    except:
        from QModernFramlessWindow.ResizeableWindow import ResizeableWindow
from qtpy.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QDesktopWidget,
    QSizePolicy,
    QFrame,
)
from qtpy.QtCore import Qt, QSize
from qtpy.QtGui import QIcon, QFont
try:
    from QModernTitleBar import QModernTitleBar, QModernDarkWindowsTitleBar
except:
    try:
        QModernTitleBar = imp.load_source("QModernTitleBar",rf"{appMainDir}\QModernTitleBar.py")
        QModernDarkWindowsTitleBar = QModernTitleBar.QModernDarkWindowsTitleBar
        QModernTitleBar = QModernTitleBar.QModernTitleBar
    except:
        from QModernFramlessWindow.QModernTitleBar import QModernTitleBar,QModernDarkWindowsTitleBar
from platform import system
try:
    from Helpers import modifyQFrameDragBehave, modifyQFrameDoubleClickBehave
except:
    try:
        imp.load_source("Helpers",rf"{appMainDir}\Helpers.py")
    except:
        from QModernFramlessWindow.Helpers import modifyQFrameDoubleClickBehave,modifyQFrameDragBehave


class QModernFramelessWindow(ResizeableWindow):
    def __init__(
        self,
        useWidnowsDarkTitleBar: bool = False,
        titleBarBgColor="default",
        windowName: str = "default",
        windowIconPath: QIcon = "default",
        windowTitleFont: QFont = "default",
        windowBorderRadius:int = 0
    ):
        super().__init__()
        self.oldGeomtry = self.geometry()
        self.isMaximizedNative = False
        self.isMaximizedNativeBefore = False
        self.isWaitingForMouseSlip = False
        self.MainAppLayout = QVBoxLayout()
        self.windowCenteralWidget = QWidget()
        self.windowGridLayout = QVBoxLayout(self.windowCenteralWidget)
        self.windowCenteralWidget.setContentsMargins(0, 0, 0, 0)
        self.windowGridLayout.setContentsMargins(0, 0, 0, 0)
        # self.windowCenteralWidget.setStyleSheet("background:black;")
        
        if not useWidnowsDarkTitleBar:
            self.titleBar = QModernTitleBar()
            self.titleBar.gridLayout.setContentsMargins(0, 0, 0, 0)
            self.titleBar.setContentsMargins(0, 0, 0, 0)
            if windowName == "default":
                self.titleBar.title.setText("Modern FramlessWindow")
            else:
                self.titleBar.title.setText(f"{windowName}")
            if windowIconPath != "default":
                self.titleBar.setWindowIcon(windowIconPath)
            if windowTitleFont != "default":
                self.titleBar.title.setFont(windowTitleFont)
            if titleBarBgColor != "default":
                self.titleBar.setStyleSheet("""background:"""+str(titleBarBgColor)+""";border:none;""")
            if windowBorderRadius != 0 :
                self.titleBarContainer.setObjectName("titleBarContainer")
                self.titleBarContainer.setStyleSheet(
                    f"border-top-left-radius:{windowBorderRadius};border-top-right-radius:{windowBorderRadius};"
                )
                self.titleBar.setObjectName("titleBar")
                self.setObjectName("MainWindow")
                self.titleBar.setStyleSheet(
                    """
                    QFrame > QPushButton,QFrame > QFrame {
                        border-bottom-left-radius:0px;
                        border-bottom-right-radius:0px;
                        border-top-left-radius:"""+str(windowBorderRadius)+"px"+""";
                        background-color:black;
                    }
                    QFrame > QPushButton {
                        border-top-right-radius:0px;
                        border-top-left-radius:0px;
                    }
                    QFrame > QPushButton#closeButton {
                        border-top-right-radius:"""+str(windowBorderRadius)+"px"+""";
                    }
                    QFrame {
                        border:none;
                        border-top-left-radius:"""+str(windowBorderRadius)+"px"+""";
                        border-top-right-radius:"""+str(windowBorderRadius)+"px"+""";
                        border-bottom-right-radius:0px;
                        border-bottom-right-radius:0px;
                        background:"""+str(titleBarBgColor)+""";
                    } 
        """
                )
                if windowBorderRadius != 0:
                    self.setAttribute(Qt.WA_TranslucentBackground)
        else:
            if windowBorderRadius != 0:
                self.setAttribute(Qt.WA_TranslucentBackground)
            self.titleBarContainer = QModernDarkWindowsTitleBar()
            self.titleBar = self.titleBarContainer.frame
            self.titleBar.setContentsMargins(0, 0, 0, 0)
            self.titleBar.setMinimumHeight(35)
            if windowName == "default":
                self.titleBar.title.setText("Modern FramlessWindow")
            else:
                self.titleBar.title.setText(f"{windowName}")
            if windowIconPath != "default":
                self.titleBar.setWindowIcon(windowIconPath)
            if windowTitleFont != "default":
                self.titleBar.title.setFont(windowTitleFont)
            if titleBarBgColor != "default":
                self.titleBar.setStyleSheet("""background:"""+str(titleBarBgColor)+""";border:none;""")
            if windowBorderRadius != 0 :
                self.titleBarContainer.setObjectName("titleBarContainer")
                self.titleBarContainer.setStyleSheet(
                    f"border-top-left-radius:{windowBorderRadius};border-top-right-radius:{windowBorderRadius};"
                )
                self.titleBar.setObjectName("titleBar")
                self.setObjectName("MainWindow")
                self.titleBar.setStyleSheet(
                    """
                    QFrame > QPushButton,QFrame > QFrame {
                        border-bottom-left-radius:0px;
                        border-bottom-right-radius:0px;
                        border-top-left-radius:"""+str(windowBorderRadius)+"px"+""";
                        background-color:black;
                    }
                    QFrame > QPushButton {
                        border-top-right-radius:0px;
                        border-top-left-radius:0px;
                    }
                    QFrame > QPushButton#closeButton {
                        border-top-right-radius:"""+str(windowBorderRadius)+"px"+""";
                    }
                    QFrame {
                        border:none;
                        border-top-left-radius:"""+str(windowBorderRadius)+"px"+""";
                        border-top-right-radius:"""+str(windowBorderRadius)+"px"+""";
                        border-bottom-right-radius:0px;
                        border-bottom-right-radius:0px;
                        background:"""+str(titleBarBgColor)+""";
                    } 
        """
                )
                if windowBorderRadius != 0:
                    self.setAttribute(Qt.WA_TranslucentBackground)
        self.windowGridLayout.setSpacing(0)
        # myButton.setStyleSheet("background:white;")
        # self.windowCenteralWidget.layout().addChildWidget(myButton)
        if system() != "Windows":
            modifyQFrameDragBehave(self, self.titleBar)
            modifyQFrameDoubleClickBehave(self, self.titleBar)
        else:
            [
                i.__setattr__("isDraggable", False)
                for i in self.findChildren(QPushButton)
                if i.objectName() != "pushButton_4"
            ]
        self.windowGridLayout.addWidget(
            self.titleBar, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.windowGridLayout.parent().setContentsMargins(0, 0, 0, 0)
        self.windowContainer = QFrame()
        self.windowContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.titleBar.parent().layout().setContentsMargins(0, 0, 0, 0)
        self.windowCenteralWidget.layout().setContentsMargins(0, 0, 0, 0)
        self.windowCenteralWidget.layout().addWidget(self.windowContainer, 0)
        self.setCentralWidget(self.windowCenteralWidget)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.titleBar.closeButton.clicked.connect(lambda: (self.close()))
        # self.titleBar.pushButton.clicked.connect(lambda: (self.setWindowState(Qt.WindowState.WindowFullScreen),self.showMaximized()) if not self.windowState() & Qt.WindowFullScreen else (self.setGeometry(self.oldGeomtry)))
        self.titleBar.maximizeButton.clicked.connect(
            lambda: (
                setattr(self, "isMaximizedNativeBefore", True),
                self.showMaximizedNative(),
                setattr(self, "isMaximizedNative", True),
            )
            if not self.isMaximizedNativeBefore
            else (
                setattr(self, "isMaximizedNative", False),
                self.setGeometry(self.oldGeomtry),
                setattr(self, "isMaximizedNativeBefore", False),
            )
        )
        self.titleBar.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.snapped = False
    def setTitlebar(
        self,
        titleBar: QFrame | QWidget,
        closeButton: QPushButton,
        maxButton: QPushButton,
        minButton: QPushButton,
        iconButtonOBjectName="titleIconButton",
    ):
        windowContainer = self.windowContainer
        self.windowContainer.destroy()
        self.titleBar.destroy()
        self.titleBar = titleBar
        self.windowGridLayout.addWidget(self.titleBar)
        self.titleBar.pushButton_3 = closeButton
        self.titleBar.pushButton = maxButton
        self.titleBar.pushButton_2 = minButton
        self.windowCenteralWidget.layout().addWidget(self.windowContainer, 0)
        [
            i.__setattr__("isDraggable", False)
            for i in self.findChildren(QPushButton)
            if i.objectName() != "titleIconButton"
        ]
        self.titleBar.pushButton_3.clicked.connect(lambda: (self.close(), exit(0)))
        # self.titleBar.pushButton.clicked.connect(lambda: (self.setWindowState(Qt.WindowState.WindowFullScreen),self.showMaximized()) if not self.windowState() & Qt.WindowFullScreen else (self.setGeometry(self.oldGeomtry)))
        self.titleBar.pushButton.clicked.connect(
            lambda: (
                setattr(self, "isMaximizedNativeBefore", True),
                self.showMaximizedNative(),
                setattr(self, "isMaximizedNative", True),
            )
            if not self.isMaximizedNativeBefore
            else (
                setattr(self, "isMaximizedNative", False),
                self.setGeometry(self.oldGeomtry),
                setattr(self, "isMaximizedNativeBefore", False),
            )
        )
        self.titleBar.pushButton_2.clicked.connect(lambda: self.showMinimized())

    def setWindowTitle(self, a0: str) -> None:
        self.titleBar.setWindowTitle(a0)

    def setTitleBarBackgroundColor(self, color):
        try:
            self.titleBar.setTitleBarBgColor(color)
        except:
            self.titleBar.setStyleSheet(self.titleBar.styleSheet()+color)

    def setWindowIcon(self, icon: QIcon) -> None:
        self.titleBar.setWindowIcon(icon)

    def setWindowIconSize(self, size: QSize):
        self.titleBar.pushButton_4.setIconSize(size)

    def setCloseIcon(self, icon: QIcon):
        self.titleBar.pushButton_3.setIcon(icon)

    def hideIcon(self):
        self.titleBarContainer.hideIcon()

    def setResizeBorderWidth(self, size: int):
        self.BorderWidth = size

    def resizeEvent(self, event):
        if not self.isMaximizedNativeBefore:
            self.oldGeomtry = self.geometry()
        return super().resizeEvent(event)

    def moveEvent(self, a0) -> None:
        try:
            if not self.isMaximizedNativeBefore:
                self.oldGeomtry = self.geometry()
        except:
            self.isMaximizedNativeBefore = False
        return super().moveEvent(a0)

    def showMaximizedNative(self):
        geo = QDesktopWidget().availableGeometry(QDesktopWidget().screenNumber(self))
        self.setGeometry(geo)


if __name__ == "__main__":
    app = QApplication([])
    m = QModernFramelessWindow(True,windowBorderRadius=4)
    m.show()
    app.exec_()

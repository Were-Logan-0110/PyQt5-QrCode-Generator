from QtDragAndDropDialog import QFileDrop, path
from uploadFile import uploadFile as UploadFile
from GUI import Ui_MainWindow as GUI
from tempfile import gettempdir
from QModernResizeableWindow import QModernFramelessWindow
from qtutils import inmain as m
from QrCodeGenerator import *
from PyQt5.QtWidgets import *
from threading import Thread
from fileHandlers import *
from PyQt5.QtCore import *
from loader import Loader
from PyQt5.QtGui import *
from STYLE import STYLE
from time import sleep
from os import remove


class MainWindow(QMainWindow):
    """_summary_

    Args:
        QMainWindow (_type_): _description_
    """

    def __init__(self):
        """_summary_"""
        super(MainWindow, self).__init__()
        self.ui = GUI()
        self.ui.setupUi(self)
        self.ui.drawerStyle.addItems(ParseConstants(GetAvailableDrawerStyles()))
        self.ui.maskStyle.addItems(ParseConstants(GetAvailableMaskStyles()))
        self.ui.bgColor.setStyleSheet(
            """
                    border:1px solid white;
                    border-radius:6px;
                    background-color: white;"""
        )
        self.ui.bgColor.clicked.connect(self.showColorDialog)
        self.ui.qrType.currentIndexChanged.connect(self.setQrType)
        self.cUrl = ""
        self.qrType = "Text"
        self.isUploaded = False
        self.changed = True
        self.bgColor = "white"
        self.bgColorTuple = (255, 255, 255, 255)
        self.ui.qrContent.setPlainText("https://github.com/Were-Logan-0110/")
        self.CreateQrCode()
        u = self.ui
        u.exportQrCode.clicked.connect(lambda: self.ExportQrCode())
        valueChangeLi = self.findChildren(QComboBox)
        valueChangeLi.extend(self.findChildren(QCheckBox))
        valueChangeLi.extend(self.findChildren(QSpinBox))
        Thread(target=self.Timer).start()
        for widg in valueChangeLi:
            if isinstance(widg, QComboBox):
                widg.currentTextChanged.connect(
                    lambda: self.__setattr__("changed", True)
                )
            if isinstance(widg, QCheckBox):
                widg.stateChanged.connect(lambda: self.__setattr__("changed", True))
            if isinstance(widg, QSpinBox):
                widg.valueChanged.connect(lambda: self.__setattr__("changed", True))
            if isinstance(widg, QPlainTextEdit):
                widg.valueChanged.connect(lambda: self.__setattr__("changed", True))
    def ExportQrCode(self):
        filePath = Loader.ExportToFile(self)
        if filePath:
            self.ui.QrCodeImage.pixmap().save(filePath)
    def Timer(self):
        def GetVal():
            return m(self.ui.delay.value)

        while True:
            sleep(GetVal())
            if self.changed:
                self.CreateQrCode()
                self.changed = False

    def setQrType(self):
        if self.ui.qrType.currentText() != "Text":
            filePath = QFileDrop.GetFile()
            if filePath:
                if path.exists(filePath) and (not path.isdir(filePath)):
                    self.filePath = str(filePath)
                    self.qrType = "File"
                    self.isUploaded = True
                    self.SetFile()
        else:
            self.qrType = "Text"

    def GetDrawerStyle(self):
        return GetDrawerStyle(
            GetAvailableDrawerStyles()[
                GetAvailableDrawerStyles().index(
                    ReverseParseConstants([self.ui.drawerStyle.currentText()])[0]
                )
            ]
        )

    def GetMaskStyle(self):
        return GetMaskStyle(
            GetAvailableMaskStyles()[
                GetAvailableMaskStyles().index(
                    ReverseParseConstants([self.ui.maskStyle.currentText()])[0]
                )
            ]
        )

    def CreateQrCode(self):
        content = m(self.ui.qrContent.toPlainText)
        if self.qrType == "File" and self.isUploaded:
            content = self.cUrl
        image = generateQrCode(
            content, m(self.GetDrawerStyle), m(self.GetMaskStyle), self.bgColorTuple
        )
        imagePath = str(Path(gettempdir()) / "temp.png")
        image.save(imagePath)

        def main():
            pixmap = QPixmap(imagePath)
            if self.ui.defaultSize.isChecked():
                pixmap = pixmap.scaled(self.ui.width.value(), self.ui.height.value())
            self.ui.QrCodeImage.setPixmap(pixmap)

        m(main)
        remove(imagePath)

    @staticmethod
    def updateProgressbar(progressbar: QProgressBar):
        def u():
            progressbar.setValue(progressbar.value() + 1)

        m(u)

    @staticmethod
    def finishProgressBar(progressbar: QProgressBar):
        def u():
            progressbar.setValue(100)

        m(u)

    def SetFile(self):
        uploadFile = self.ui.uploadFile.isChecked()
        if uploadFile:
            self.ui.qrType.setDisabled(True)
            self.ui.progressBar.setValue(0)
            pageURL = self.ui.pageURL.isChecked()
            Thread(
                target=lambda: UploadFile(
                    self.filePath,
                    pageURL,
                    lambda x=1: self.updateProgressbar(self.ui.progressBar),
                    lambda: (
                        self.finishProgressBar(self.ui.progressBar),
                        m(lambda: self.ui.qrType.setDisabled(False)),
                    ),
                    lambda url: m(
                        lambda: (
                            self.ui.uploadedUrl.setText(url),
                            self.__setattr__("cUrl", str(url)),
                            self.__setattr__("isUploaded", True),
                        )
                    ),
                )
            ).start()
        else:
            with open(self.filePath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self.ui.qrContent.setPlainText(content)
            self.isUploaded = False

    @staticmethod
    def QColorToRgba(qcolor: QColor):
        red = qcolor.red()
        green = qcolor.green()
        blue = qcolor.blue()
        alpha = qcolor.alpha()
        return red, green, blue, alpha

    def showColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bgColor = color.name()
            self.bgColorTuple = self.QColorToRgba(color)
            self.ui.bgColor.setStyleSheet(
                f"""
                        border:1px solid white;
                        border-radius:6px;
                        background-color: {color.name()};"""
            )
            self.changed = True


def setModernTitleBar(
    window: QMainWindow,
    useWidnowsDarkTitleBar: bool = False,
    titleBarBgColor="default",
    windowName: str = "default",
    windowIconPath: QIcon = "default",
    windowTitleFont: QFont = "default",
    windowBorderRadius: int = 0,
) -> QModernFramelessWindow:
    centralWidget = window.centralWidget()
    centralWidget.setStyleSheet(STYLE)
    framlessWindow = QModernFramelessWindow(
        useWidnowsDarkTitleBar=useWidnowsDarkTitleBar,
        titleBarBgColor=titleBarBgColor,
        windowName=windowName,
        windowIconPath=windowIconPath,
        windowTitleFont=windowTitleFont,
        windowBorderRadius=windowBorderRadius,
    )
    Layout = QGridLayout()
    Layout.setContentsMargins(0, 0, 0, 0)
    Layout.addWidget(centralWidget)
    framlessWindow.windowContainer.setLayout(Layout)
    return framlessWindow


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    # window.show()
    Window: QMainWindow = setModernTitleBar(window, True)
    window.setStyleSheet(window.styleSheet())
    Window.show()
    Window.titleBar.title.setText("Qr Code Generator By Logan Umzingeli")
    Window.closeEvent = window.closeEvent
    app.exec_()

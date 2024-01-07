import os
import sys
from PyQt5.QtWidgets import *
try:
    from QModernResizeableWindow import QModernFramelessWindow
except:
    from QModernFramlessWindow.QModernResizeableWindow import QModernFramelessWindow
from pathlib import Path


class FileOpenerDialog(QDialog):
    def __init__(self, folder_path="", file_name=""):
        super().__init__()

        self.folder_path = folder_path
        self.file_name = file_name
        self.fullPath = str(Path(folder_path) / f"{file_name}")
        self.setStyleSheet(
            """
        QDialog {
            background-color: #2e2e2e;
        }
        QLabel {
            color: white;
        }
        QPushButton {
            background-color: #007ACC;
            color: white;
            border: 1px solid #007ACC;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #005F92;
        }
    """
        )

        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Opener")
        self.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()

        self.result_label = QLabel(f"Saved To {self.fullPath}")

        self.open_folder_button = QPushButton("Open Folder")
        self.open_file_button = QPushButton("Open File")

        self.open_folder_button.clicked.connect(self.openFolder)
        self.open_file_button.clicked.connect(self.openFile)

        layout.addWidget(self.result_label)
        layout.addWidget(self.open_folder_button)
        layout.addWidget(self.open_file_button)

        self.setLayout(layout)

    def openFolder(self):
        if os.path.exists(self.folder_path):
            if sys.platform == "win32":
                os.system(f'explorer "{self.folder_path}"')
            elif sys.platform == "darwin":
                os.system(f'open "{self.folder_path}"')
            elif sys.platform == "linux":
                os.system(f'xdg-open "{self.folder_path}"')
            else:
                self.result_label.setText("Unsupported platform")
                return
            self.result_label.setText(f"Opened folder: {self.folder_path}")
        else:
            self.result_label.setText("Folder not found.")

    def openFile(self):
        fullPath = self.fullPath
        if os.path.exists(fullPath):
            if sys.platform == "win32":
                os.system(f'start "" "{fullPath}"')
            elif sys.platform == "darwin":
                os.system(f'open "{fullPath}"')
            elif sys.platform == "linux":
                os.system(f'xdg-open "{fullPath}"')
            else:
                self.result_label.setText("Unsupported platform")
                return
            self.result_label.setText(f"Opened file: {self.file_name}")
        else:
            self.result_label.setText("File not found.")


def setModernTitleBar(
    window: QDialog,
    useWidnowsDarkTitleBar: bool = False,
    titleBarBgColor="default",
    windowName: str = "default",
    windowIconPath="default",
    windowTitleFont="default",
    windowBorderRadius: int = 0,
) -> QModernFramelessWindow:
    centralWidget = window
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


def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)


def showFileOpenerDialog(dirPath: (str | Path), fileName: (str | Path)):
    dirPath = str(dirPath)
    fileName = str(fileName)
    dialog = FileOpenerDialog(dirPath, fileName)
    window = setModernTitleBar(dialog, True)
    window.resize(200, 200)
    center(window)
    window.titleBar.title.setText("File Opener")

    def deleteWin(window):
        window.hide()

    window.titleBar.closeButton.clicked.connect(lambda: deleteWin(window))
    window.show()

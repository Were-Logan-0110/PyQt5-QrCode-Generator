import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pathlib import Path
from os import path


def getSize(filePath: str):
    sizeUnits = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    size = path.getsize(filePath)
    unitIndex = 0

    while size >= 1024 and unitIndex < len(sizeUnits) - 1:
        size /= 1024.0
        unitIndex += 1

    return f"{size:.2f} {sizeUnits[unitIndex]}"


class QFileDrop(QDialog):
    def __init__(self):
        super().__init__()
        self.filePath = None
        self.setWindowTitle("File Drop Dialog")
        layout = QVBoxLayout()
        self.resize(300, 200)
        # Create label for displaying file information
        self.infoLabel = QLabel(self)
        self.infoLabel.setText("Drop File Here")
        self.infoLabel.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.infoLabel)
        self.displayLabel = QLabel(self)
        self.displayLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.displayLabel)
        self.setAcceptDrops(True)

        # Create submit button
        submitButton = QPushButton("Submit", self)
        submitButton.clicked.connect(self.onSubmit)
        layout.addWidget(submitButton)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        mimeType = event.mimeData()
        try:
            if mimeType.hasUrls() and mimeType.urls()[0].isLocalFile():
                event.acceptProposedAction()
        except IndexError:
            if path.exists(mimeType.text()):
                event.acceptProposedAction()

    def dropEvent(self, event):
        mimeType = event.mimeData()
        try:
            if mimeType.hasUrls() and mimeType.urls()[0].isLocalFile():
                filePath = Path(mimeType.urls()[0].toLocalFile())
                self.filePath = filePath
                self.showFileInfo(filePath)
        except:
            filePath = Path(mimeType.text())
            self.filePath = filePath
            self.showFileInfo(filePath)

    def showFileInfo(self, filePath):
        # Display file information
        fileInfo = f"File Path: {filePath}\nFile Size: {getSize(filePath)}\n"
        fileInfo += f"File Type: {'Image' if filePath.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif'} else 'Not an Image'}"
        self.infoLabel.setText(fileInfo)
        if path.exists(str(filePath)):
            pixmap = QPixmap(str(filePath))
            self.displayLabel.setPixmap(pixmap)

    def onSubmit(self):
        self.close()
        return self.filePath

    @property
    def filePathInfo(self):
        return self.infoLabel.text()

    @staticmethod
    def GetFile():
        dialog = QFileDrop()

        # Apply some styling
        dialog.setStyleSheet(
            """
            QDialog {
                background-color: #f0f0f0;
                border: 2px solid #3498db;
                border-radius: 10px;
            }
            
            QLabel {
                margin: 10px;
                background:transparent;
                color:black;
                font-weight: 700;
                font-size: 15px;
            }

            QPushButton {
                margin: 10px;
                padding: 10px;
                background-color: #3498db;
                color: #fff;
                border: none;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #217dbb;
            }
        """
        )

        dialog.show()
        dialog.exec_()
        return dialog.filePath


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(QFileDrop.GetFile())
    sys.exit(app.exec_())

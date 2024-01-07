from PyQt5.QtWidgets import QFileDialog
from fileOpener import showFileOpenerDialog
from os import path
class Loader:
    
    def __init__(self) -> None:
        pass
    @staticmethod
    def loadFile(Window, ListWidget=None, Label=None) -> None:
        fileDailog = QFileDialog()
        filePath, _ = fileDailog.getOpenFileName(Window, "Open File")
        if filePath:
            if ListWidget is not None:
                with open(filePath, "r",encoding="utf-8",errors="ignore") as File:
                    ListWidget.addItems([line.strip() for line in File.readlines()])
                if Label:
                    Label.setText(str(ListWidget.count()))
            else:
                return filePath
    @staticmethod
    def ExportToFile(Window, ListWidget=None):
        fileDialog = QFileDialog()
        filePath, _ = fileDialog.getSaveFileName(Window, "Save File")
        if filePath and ListWidget:
            with open(filePath, "w") as File:
                File.writelines([
                    str(ListWidget.item(i).text()+"\n")
                    for i in range(ListWidget.count())
                ])
            showFileOpenerDialog(path.dirname(filePath),filePath.split("/")[-1])
            return filePath
        return filePath
    @staticmethod
    def loadDirectory(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if dialog.exec_():
            selected_directory = dialog.selectedFiles()[0]
            return selected_directory
        else:
            return None
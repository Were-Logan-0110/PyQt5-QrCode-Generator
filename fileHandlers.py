from pathlib import Path
from os import makedirs, path
import sys

appMainDir = Path(getattr(sys, "_MEIPASS", path.dirname(path.abspath(__file__))))


def readFile(filePath: (Path | str), strip: bool = False) -> str:
    with open(filePath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read() if not strip else f.read().strip()


def GetMainDir() -> str:
    cPath = appMainDir
    if "_internal" in str(cPath):
        cPath = Path(str(cPath).replace("//_internal", ""))
        cPath = Path(str(cPath).replace("\\_internal", ""))
    return cPath
def tryGetPathInDir(file: (Path | str)) -> Path:
    if not path.exists(file):
        cPath = appMainDir
        if "_internal" in str(cPath):
            cPath = Path(str(cPath).replace("//_internal", ""))
            cPath = Path(str(cPath).replace("\\_internal", ""))
        nFile = cPath
        if str(file) not in str(cPath):
            nFile = cPath / file
        return nFile
    return file


def createFile(filePath: (Path | str)) -> bool:
    try:
        makedirs(path.dirname(filePath))
    except:
        pass
    try:
        with open(filePath, "a", encoding="utf-8", errors="ignore") as f:
            pass
        return True
    except:
        return False


def appendToFile(filePath: (Path | str), text: str) -> bool:
    if not path.exists(filePath):
        createFile(filePath)
    with open(filePath, "a", encoding="utf-8", errors="ignore") as f:
        f.write(text)


def appendToFileInMainDir(fileName: str, text: str, endl: bool = True) -> bool:
    aFile = tryGetPathInDir(fileName)
    appendToFile(aFile, text + "\n" if endl else text)


def createFileInMainDir(fileName: str) -> bool:
    nFile = tryGetPathInDir(fileName)
    return createFile(nFile)

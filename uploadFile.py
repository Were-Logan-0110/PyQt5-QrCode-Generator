from bs4 import BeautifulSoup
from fileHandlers import *
from pathlib import Path
import requests


class UploadInChunks:
    def __init__(
        self, filename, callback=None, finishedCallback=None, callbackFrequency=100
    ):
        self.filename = filename
        self.callbackFrequency = callbackFrequency
        self.totalSize = path.getsize(filename)
        self.readSoFar = 0
        self.callback = callback
        self.iterCount = 0
        self.chunkSize = self.calculateChunkSize()
        self.finishedCallback = finishedCallback

    def calculateChunkSize(self):
        return max(1, self.totalSize // self.callbackFrequency)

    def __iter__(self):
        with open(self.filename, "rb") as file:
            while True:
                data = file.read(self.chunkSize)
                if not data:
                    break
                self.readSoFar += len(data)
                yield data
                if self.callback:
                    self.callback(self.iterCount + 1)
                self.iterCount += 1
                if self.readSoFar >= self.totalSize:
                    if self.finishedCallback:
                        self.finishedCallback()

    def __len__(self):
        return self.totalSize


def uploadFile(
    filePath: (str | Path), pageUrl: bool = True, callback=None, finishedCallback=None,urlFinishedCallback=None):
    filePath = tryGetPathInDir(filePath)
    headers = {
        "authority": "filebin.net",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.5",
        "cache-control": "no-cache",
        # 'cookie': 'sb=4sQlZXNa64l0inJ728BQijrE; datr=4sQlZbQOGvWvlaHM8n0vcJlW; c_user=100050005532993; m_page_voice=100050005532993; dpr=0.8999999761581421; xs=30%3AEpSScVWke8B3Bg%3A2%3A1696974406%3A-1%3A6421%3A%3AAcVRk7rXaGFsp8-EU27UChpK7VRpuzOb56ED9DvSiPw; fr=1ipBDCRZVBIV0Tf5r.AWUDb2L34CCr4Vo3X0k6CAkSNKQ.BlOadM.CN.AAA.0.0.BlOaxq.AWX6V15Evjo; wd=841x723; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1698278698585%2C%22v%22%3A1%7D',
        "dpr": "0.9",
        "pragma": "no-cache",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-full-version-list": '"Chromium";v="118.0.5993.89", "Google Chrome";v="118.0.5993.89", "Not=A?Brand";v="99.0.0.0"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"10.0.0"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "viewport-width": "841",
    }
    filePath = str(filePath)
    if "/" in filePath:
        fileName = filePath.split("/")[-1]
    else:
        fileName = filePath.split("\\")[-1]
    session = requests.session()
    session.headers.update(headers)
    response = session.get("https://filebin.net")
    soup = BeautifulSoup(response.text, "lxml")
    url = [
        url.get("href")
        for url in soup.find_all("a")
        if url.get("href").startswith("https://filebin.net/")
    ][0]
    headers["Filename"] = fileName
    headers["Bin"] = url.split("/")[-1]
    response = session.post(
        url + f"/{fileName}",
        data=UploadInChunks(
            filePath, callback, finishedCallback
        ),
    )
    if urlFinishedCallback:
        urlFinishedCallback(url)
    if pageUrl:
        return url
    else:
        return url + f"/{fileName}"
# print(uploadFile(r"C:\Users\ahmed\Downloads\VID_20240104_113840.mp4", False))
pip install -r .\requirements.txt
./Scripts/Activate.ps1
./Scripts/nuitka --disable-console --standalone --lto=no --enable-plugin=pyqt5 main.py
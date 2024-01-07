python -m venv .
./Scripts/Activate.ps1
pip install -r .\requirements.txt
./Scripts/nuitka --disable-console --standalone --lto=no --enable-plugin=pyqt5 main.py

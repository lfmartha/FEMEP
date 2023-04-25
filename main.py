import sys
from PyQt5.QtWidgets import QApplication
from appcontroller import AppController


# ----------------------- UTILIDADES ----------------------------
# Codigo utilizado para converter .ui->.py: pyuic5 GM2DTool.ui -o GM2DTool.py
# Ambiente virtual : .env/Scripts/Activate.ps1 ---> deactivate
# criando um exe: pyinstaller --noconsole main.py
# ----------------------------------------------------------------


# Finite Element Method Educational Computer Program - FEMEP
if __name__ == '__main__':
    qt = QApplication(sys.argv)
    App = AppController()
    App.show()
    qt.exec_()

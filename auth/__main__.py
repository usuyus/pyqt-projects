from PyQt5.QtWidgets import QApplication
from login import LoginWindow
import os

RELOAD = False

if RELOAD:
	path = f"{os.getcwd()}/{__file__}/.."
	print(path)
	os.system(f"pyuic5 {path}/design.ui -o {path}/design.py")
	print("design.ui reloaded.")

app = QApplication([])
widget = LoginWindow()
widget.show()
app.exec_()
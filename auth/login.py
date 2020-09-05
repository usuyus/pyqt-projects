from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from design import Ui_LoginWindow
from hashlib import sha256
import pickle

class LoginWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.ui = Ui_LoginWindow()
		self.ui.setupUi(self)
		self.loadHashes()
		self.newUsers = False

	def loadHashes(self):
		try:
			with open("hashes.pickle", "rb") as f:
				try: self.hashes = pickle.load(f)
				except EOFError: self.hashes = {}
		except FileNotFoundError: self.hashes = {}

	def saveHashes(self):
		if self.newUsers:
			with open("hashes.pickle", "wb") as f:
				pickle.dump(self.hashes, f)
				print("saved")

	def setStatus(self, msg):
		self.ui.statusLabel.setText(msg)

	def login(self):
		pw = self.ui.pwEdit.text()
		user = self.ui.userEdit.text()
		h = sha256(bytes(pw, "utf-8")).hexdigest()

		try: self.hashes[user]
		except KeyError: self.setStatus("User does not exist")
		else:
			if self.hashes[user] != h: self.setStatus("Wrong password")
			else: self.setStatus("Access granted")

	def signup(self):
		pw = self.ui.pwEdit.text()
		user = self.ui.userEdit.text()
		h = sha256(bytes(pw, "utf-8")).hexdigest()

		try: self.hashes[user]
		except KeyError: 
			self.hashes[user] = h
			self.setStatus("User created")
			self.newUsers = True
		else: self.setStatus(f"User already exists")

	def closeEvent(self, event):
		self.saveHashes()
		event.accept()

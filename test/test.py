from PyQt5 import QtCore, QtGui, QtWidgets

class UiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setStyleSheet("background-color: #eeeeee;")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 341, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setStyleSheet("color: #000000;\n"
"font-size: 40pt;\n"
"font-weight: bold;")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setStyleSheet("padding: 20px;\n"
"font-size: 16pt;\n"
"font-weight: bold;\n"
"background-color: #aaaaaa;")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.toggleButton)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Text"))
        self.pushButton.setText(_translate("Form", "Trigger"))

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = UiForm()
        self.ui.setupUi(self)
        self.textVisible = True

    def toggleButton(self):
        if self.textVisible: self.ui.label.clear()
        else: self.ui.label.setText("Text")
        self.textVisible = not self.textVisible

app = QtWidgets.QApplication([])
widget = MainWidget()
widget.show()
app.exec_()

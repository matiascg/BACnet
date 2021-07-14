import sys

from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QScrollArea,
    QPushButton,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QTabWidget
)
from PyQt5.QtCore import Qt, QFile, QIODevice, QTextStream
from FrontEnd.Tabs import ContactTab, ShareTab, RecoveryTab, PendingTab, act
from FrontEnd.CustomTab import TabBar, TabWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Widget holding all the window contents
        self.widget = QWidget()
        # Layout for self.widget
        self.vbox = QVBoxLayout()
        self.widget.setLayout(self.vbox)
        # Setup different Tabs
        self.tabs = TabWidget(self)
        self.tabs.setTabBar(TabBar())
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.addTab(ContactTab(self), "Contacts")
        self.tabs.addTab(ShareTab(self), "Share")
        self.recoveryTab = RecoveryTab(self)
        self.tabs.addTab(self.recoveryTab, "Recovery")
        self.tabs.currentChanged.connect(self.recoveryTab.autoRecovery.updateComboBox)
        # Add the tabs to the Layout of self.widget
        self.vbox.addWidget(self.tabs)
        # Create Update Button, should pull all the information from ?? and update the contents
        self.updateButton = QPushButton("Update")
        # TODO create update function and connect to button
        self.updateButton.clicked.connect(self.updateContents)
        self.vbox.addWidget(self.updateButton)

        # add a scroll area to deal with resizing of the window
        self.scroll = QScrollArea()
        # we can turn off the vertical scrollbar because there is a minimum size
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        # set self.widget in the scroll area
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        # definition of window size and Title
        self.resize(500, 600)
        self.setMinimumHeight(600)
        self.setWindowTitle("Secret Sharing BACnet")
        self.show()
        return

    def updateContents(self):
        #TODO actually update content
        print("updated")


class LoginPage(QDialog):
    def __init__(self, parent=None):
        super(LoginPage, self).__init__(parent)
        loginLayout = QFormLayout()
        self.usernameInput = QLineEdit()
        loginLayout.addRow("Username", self.usernameInput)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.check)
        self.buttons.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addLayout(loginLayout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def check(self):
        act.create_user(self.usernameInput.text())
        self.accept()
        pass

    def createUser(self):
        #TODO How do we create users and store information about them, we probably want to create the key pairs here
        act.create_user(self.usernameInput.text())
        print(f"created user {self.usernameInput.text()}")
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Style from: https://github.com/sommerc/pyqt-stylesheets/blob/master/pyqtcss/src/dark_orange/style.qss
    if not act.rq_handler.logged_in:
        login = LoginPage()
        if not login.exec_():
            sys.exit(-1)
    qss = "FrontEnd/styles/style3.qss"
    stream = QFile(qss)
    stream.open(QIODevice.ReadOnly)
    app.setStyleSheet(QTextStream(stream).readAll())
    stream.close()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

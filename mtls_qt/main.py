import os
import sys
from configparser import ConfigParser
from functools import partial
from pathlib import Path

from mtls import MutualTLS
from PyQt5 import QtWidgets, QtCore, QtGui

NAME = "mtls"
CONFIG_HOME = os.environ.get(
    "XDG_CONFIG_HOME",
    os.path.join(os.environ.get("HOME"), "config")
)
CONFIG_PATH = f"{CONFIG_HOME}/.config/mtls/config.ini"


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        create_if_missing(CONFIG_PATH)
        self.config = ConfigParser()
        self.config.read(CONFIG_PATH)
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        self.parent = parent

        # Connect
        connectMenu = QtWidgets.QMenu("Server", menu)
        for section in self.config.sections():
            action = connectMenu.addAction(section)
            action.triggered.connect(partial(self.execute, section))
        menu.addMenu(connectMenu)

        menu.addSeparator()

        # Settings
        # TODO(drGrove): Create UI for editing settings
        # settingsAction = menu.addAction("Settings")
        # settingsAction.triggered.connect(self.preferences)

        # Exit
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)
        self.setContextMenu(menu)

    def showMsg(self, msg, timeout=2000):
        self.showMessage(
            NAME,
            msg,
            QtWidgets.QSystemTrayIcon.Information,
            timeout
        )

    def exit(self):
        QtCore.QCoreApplication.exit()

    def preferences(self):
        self.parent.show()

    def execute(self, var):
        options = {
            'config': None,
            'gpg_password': None
        }
        mtls = MutualTLS(var, options)
        try:
            mtls.get_crl(False)
            mtls.create_cert(None)
        except ValueError as e:
            self.showMsg(str(e), 5000)


class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, image, parent=None):
        super().__init__()
        self.hide()
        path = os.path.dirname(os.path.realpath(__file__))
        icon_path = f"{path}/assets/{image}"
        print(icon_path)
        self.tray_icon = SystemTrayIcon(QtGui.QIcon(icon_path), self)
        self.tray_icon.show()
        self.settings = QtCore.QSettings(
            CONFIG_PATH,
            QtCore.QSettings.IniFormat
        )
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.tab_widget.setObjectName("tabWidget")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMsg("Application minimize to Tray")


def create_if_missing(config_file):
    directory = os.path.dirname(config_file)
    Path(directory).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(config_file):
        with open(config_file, 'w'):
            pass


def main():
    image = "icon.png"
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    SettingsWindow(image, w)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

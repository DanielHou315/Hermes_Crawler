from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 

from . import crawler, files, htime

# create system tray
def create_system_tray(menu, icon):
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.setContextMenu(menu)

# create menu
def create_menu(app, iem, ist, ich, och, occ, oqu):
    menu = QMenu()
    menu.addAction(iem)
    menu.addAction(ist)
    menu.addAction(ich)
    menu.addAction(och)
    menu.addAction(occ)
    menu.addAction(oqu)
    return menu

# Info - Client email
def create_info_email(app, client_email):
    info_email = QLabel(client_email)
    info_email_action = QWidgetAction(app)
    info_email_action.setDefaultWidget(info_email)
    return info_email_action
    
def create_info_status(app):
    info_status = QLabel(" Last Checked ")
    info_status_action = QWidgetAction(app)
    info_status_action.setDefaultWidget(info_status)
    return info_status_action

def create_info_checktime(app, last_check_time):
    info_time = QLabel(htime.get_time_str_short(last_check_time))
    info_time_action = QWidgetAction(app)
    info_time_action.setDefaultWidget(info_time)
    return info_time_action

def create_option_checknow(check_func):
    option_check_now = QAction("Check Now")
    option_check_now.triggered.connect(check_func)       # Connect Check Function
    return option_check_now

def create_option_clearcache(clear_cache_func):
    option_clear_cache = QAction("Clear Cache")
    option_clear_cache.triggered.connect(clear_cache_func)       # Connect Check Function
    return option_clear_cache

def create_option_quit(app):
    option_quit = QAction("Quit")
    option_quit.triggered.connect(app.quit)
    return option_quit



if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    
    # Adding an icon
    icon = QIcon("hermes.icns")
    
    # Adding item on the menu bar
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    
    # Creating the options
    menu = QMenu()
    option1 = QAction("Geeks for Geeks")
    option2 = QAction("GFG")
    menu.addAction(option1)
    menu.addAction(option2)
    
    # To quit the app
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)
    
    # Adding options to the System Tray
    tray.setContextMenu(menu)
    
    app.exec_()
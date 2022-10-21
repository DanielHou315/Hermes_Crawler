import os, sys
from datetime import datetime

from hclib import ui, files, htime, msg, crawler



class HC():
    def __init__(self):
        '''
        QT App Initialization
        '''
        # Start an app instance
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        print("[Main] Initialized app")

        '''
        Settings Initialization
        '''
        self.checking = False
        self.client_email = files.load_email()
        self.last_check_time = files.load_history()
        # print(self.last_check_time)
        self.last_check_file = files.find_last_record()
        self.icon = QIcon("./hermes.icns")
        print("[Main] Initialized settings")

        '''
        UI Initialization
        '''
        # information
        # self.info_email = ui.create_info_email(self.app, self.client_email)
        self.info_email = QLabel(self.client_email)
        self.info_email_action = QWidgetAction(self.app)
        self.info_email_action.setDefaultWidget(self.info_email)
        # self.info_status = ui.create_info_status(self.app)
        self.info_status = QLabel("Last Checked")
        self.info_status_action = QWidgetAction(self.app)
        self.info_status_action.setDefaultWidget(self.info_status)
        # self.info_time = ui.create_info_checktime(self.app, self.last_check_time)
        self.info_time = QLabel("{0} {1}".format(htime.get_relative_day_str(datetime.now(), self.last_check_time), \
            htime.get_time_str_short(self.last_check_time)))
        self.info_time_action = QWidgetAction(self.app)
        self.info_time_action.setDefaultWidget(self.info_time)
        print("[Main] Initialized info")

        # Options
        # self.option_checknow = ui.create_option_checknow(self.check)
        self.option_check_now = QAction("Check Now")
        self.option_check_now.triggered.connect(self.check)
        # self.option_clearcache = ui.create_option_clearcache(files.clear_cache)
        self.option_clear_cache = QAction("Clear Cache")
        self.option_clear_cache.triggered.connect(files.clear_cache)
        # self.option_quit = ui.create_option_quit(self.app)
        self.option_quit = QAction("Quit")
        self.option_quit.triggered.connect(self.app.quit)
        print("[Main] Initialized options")

        # Menu
        self.menu = QMenu()
        self.menu.addAction(self.info_email_action)
        self.menu.addAction(self.info_status_action)
        self.menu.addAction(self.info_time_action)
        self.menu.addAction(self.option_check_now)
        self.menu.addAction(self.option_clear_cache)
        self.menu.addAction(self.option_quit)

        # System Tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        self.tray.setContextMenu(self.menu)

        print("[Main] Initialized menu and tray")

        '''
        File Directory Initialization
        '''
        # Enter Documents Directory
        files.enter_directory()

        print("[Main] Entered directory")

        '''
        Daemon Initialization
        '''
        # Create Daemon
        self.schedule_daemon_thread = QTimer()
        self.schedule_daemon_thread.setInterval(10000)
        self.schedule_daemon_thread.timeout.connect(self.crawler_daemon)
        self.schedule_daemon_thread.start()
        
        print("[Main] Initialized daemon")

    '''
    Run App
    '''
    def run(self):
        self.app.exec_()


    '''
    Daemon Functions
    '''
    def crawler_daemon(self):
        # If checking in progress, wait till another cycle
        if self.checking == True: 
            return

        # Update Time Display
        rel_day = htime.get_relative_day_str(datetime.now(), self.last_check_time)
        time_str = htime.get_time_str_short(self.last_check_time)
        self.info_time.setText("{0} {1}".format(rel_day, time_str))
        del rel_day
        del time_str

        # Check update at the beginning of every hour
        if htime.new_hour(datetime.now(), self.last_check_time):
            self.check()


    '''
    Check Functions
    '''
    # Crawl for updates
    def check(self):
        print("[Main] Checking")
        # Disable Check Now Button while checker is running
        self.checking = True
        self.option_check_now.setDisabled(True)
        self.info_time.setText(" Checking... ")
        now = datetime.now()

        # Get New Record
        new_file_name = crawler.get_new_record()
        print("[Main] Gotten New Record")

        # Process history
        old_record = []
        old_links = []
        old_images = []
        if not self.last_check_file == "":
            old_record, old_links, old_images = crawler.extract(self.last_check_file)
        new_record, new_links, new_images  = crawler.extract(new_file_name)
        print("[Main] Processed Records")

        # Compare Records
        diff_list, diff_links, diff_images = crawler.compare(old_record, old_links, old_images, new_record, new_links, new_images)
        print("[Main] Compared Lists")

        # Send Email
        if len(diff_list) > 0:
            msg.send_email(self.client_email, diff_list, diff_links, diff_images)
            print("[Main] Found New Items")
        del diff_list, diff_links, diff_images
        print("[Main] Sent Email")
        
        # Clean up
        # Update Time
        with open("setting_history.txt", "w") as file:
            file.write(htime.get_time_str_now())
            file.close()
        self.info_time.setText("Just Now")
        print("[Main] Updated setting history")

        # Update Settings
        self.last_check_file = new_file_name
        self.last_check_time = now
        del now
        self.checking = False
        # Update UI
        self.option_check_now.setDisabled(False)
        print("[Main] Finished Checking")
        return



'''
Main
'''

if __name__ == "__main__":
    crawler_app = HC()
    crawler_app.run()

    '''
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
    '''
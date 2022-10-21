# #!/opt/homebrew/Cellar/python@3.10/3.10.6_2/Frameworks/Python.framework/Versions/3.10/lib/python3.10

import os, sys, json
from datetime import datetime
from lib import utils, msg, crawler

ROOT_PATH = "/Users/danielhou/"

class HC():
    def __init__(self):
        ''' Configure Directory '''
        self.root = self.configure_filepath(ROOT_PATH)
        print(self.root)
        ''' Configure Logger '''
        self.logger = self.configure_logger(self.root)

        ''' Load Settings '''
        self.user_name = "dear customer"
        self.user_email = ""
        self.tracking_list = []
        self.load_config(logger=self.logger, config_file=self.root+"configuration.json")
        self.last_check_file = utils.find_last_record(self.root)
        self.logger.log("Main", "Initialized settings")

        ''' Clear Cache '''
        clear_cache_status = utils.clear_cache(self.root)
        self.logger.log("Main", "Cleared Cache Status: " + str(clear_cache_status))


    def load_config(self, logger, config_file="./configuration.json"):
        # Open Json
        if not os.path.isfile(config_file):
            self.logger.log("Main", "No Configuration.json file found in target path")
            raise Exception("No Configuration.json file found in target path")
        with open(config_file, "r") as conf:
            try:
                data = conf.read()
                content = json.loads(data)
                self.logger.log("Main", "[Config Loader] Config JSON opened, loading...")
            except:
                raise Exception("Configurator cannot open configuration.json")
            try: 
                self.user_email=content["user_email"]
                if not utils.is_valid_email(self.user_email):
                    raise Exception("Email format not valid!")
                self.logger.log("Config Loader", "User Email {0} Noted".format(self.user_email))
            except:
                raise Exception("Failed to get user email from JSON")
            try:
                self.tracking_list = content["tracked_bag_names"]
                for item in self.tracking_list:
                    if item == "": self.tracking_list.remove(item)
            except:
                raise Exception("Failed to get tracking list from JSON")

            try: self.user_name = content["user_name"]
            except: pass
        return




    def configure_filepath(self, root_path):
        try:
            if not os.path.isdir(root_path + ".hermes_crawler/"):
                os.mkdir(root_path + ".hermes_crawler/")
            for sub_dir in ['log', 'record_cache', 'image_cache']:
                if not os.path.isdir(root_path + ".hermes_crawler/" + sub_dir):
                    os.mkdir(root_path + ".hermes_crawler/" + sub_dir)
            return root_path + ".hermes_crawler/"
        except:
            raise PermissionError("Hermes Server does not have permission to edit in your home path")



    def configure_logger(self, root):
        try: 
            logger = utils.LogRep(root + "log/hermes_server_log", print_log=True, write_log=True)
            return logger
        except: raise PermissionError("Hermes Server does not have permission to write Log")
        


    '''Check Functions'''
    # Crawl for updates
    def check(self):
        self.logger.log("Main", "Checking")
        # now = datetime.now()

        # Get New Record
        new_file = crawler.get_new_record(logger=self.logger, root=self.root)
        self.logger.log("Main", "Gotten New Record: " + new_file)



        # Process history
        old_record = []; old_links = []; old_images = []
        if not self.last_check_file == "":
            old_record, old_links, old_images = crawler.extract(logger=self.logger, file=self.last_check_file)
        new_record, new_links, new_images  = crawler.extract(logger=self.logger, file=new_file)
        self.logger.log("Main", "Processed Records")



        # Compare Records
        diff_list, diff_links, diff_images = crawler.compare(self.logger, self.tracking_list, \
            old_record, old_links, old_images, new_record, new_links, new_images)
        self.logger.log("Main", "Compared Lists")




        # Send Email
        if len(diff_list) > 0:
            msg.send_email(self.logger, self.root, self.user_email, diff_list, diff_links, diff_images)
            self.logger.log("Main", "Sent Email")
            del diff_list, diff_links, diff_images
        else:
            self.logger.log("Main", "No Different Items, so no email sent")
        # Clear Cache
        utils.clear_cache(root=self.root)
        # Finish
        self.logger.log("Main", "Finished Checking")
        return


if __name__ == "__main__":
    instance = HC()
    instance.check()
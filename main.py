#!/usr/bin/env python3
from modules.Config import Config
from modules.Logger import Logger
import importlib, os, time

current_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

config = Config(current_dir + "main.cfg")
if not config.has("current_dir"):
    config.write("current_dir", current_dir)
else:
    config.update("current_dir", current_dir)

logger = Logger(config)

logger.info("Checking `"+current_dir+"tmp/` folder")
if not os.path.isdir(current_dir + "tmp/"):
    logger.warning("Cannot find `"+current_dir+"tmp/` directory. Creating one.")
    try:
        os.mkdir(current_dir+"tmp/")
    except Exception as e:
        msg = "Cannot create Directory `"+current_dir+"tmp/`. Error msg: " + str(e)
        logger.fatal(msg)
        print(msg)
        exit()
logger.success("Done!")

logger.info("Loading CalDavManager")
try:
    from modules.CalDavManager import CalDavManager
    cdav = CalDavManager(config)
    logger.success("Loaded!")
except Exception as e:
    logger.fatal("Error! " + str(e))

logger.info("Loading identifyUrl")
try:
    from modules.url import identifyUrl
    logger.success("Loaded!")
except Exception as e:
    logger.fatal("Error! " + str(e))

url_list = config.get("url_file")
logger.info("Loading urls from `"+ url_list +"`")
urls = list()
try:
    with open(url_list, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line:
                urls.append(line)
    if len(urls) == 0:
        raise Exception("Url list is empty!")
    logger.success("Loaded!")
except Exception as e:
    msg = "Cannot load urls! Error msg: " + str(e)
    logger.fatal(msg)
    print(msg)
    exit()

logger.info("Loading all modules!")
mods = {}
modules = {}
for url in urls:
    module = identifyUrl(url)
    if module:
        if not module in mods:
            mods[module] = 1

for key in mods:
    logger.info("Loading: " + key + " module")
    modules[key] = importlib.import_module("modules." + key)

logger.success("Done!")

while True:
    logger.info("Checking for changes!")
    last_module = None
    for url in urls:
        module = identifyUrl(url)
        if module:
            if not last_module == module:
                try:
                    # site = eval("modules." + module + ".Site(config, logger)")
                    site = modules[module].Site(config, logger)
                except Exception as e:
                    msg = "Cannot load Site class from " + module + " module! Error msg: " + str(e)
                    logger.fatal(msg)
                    print(msg)
                    exit()

            if site.checkForChanges(url):
                msg = "New Ep from module `" + module + "`. Url: " + url
                logger.info(msg)
                print(msg)

                logger.info("Creating new WebDav event!")
                event = cdav.createEvent(msg, msg + "\nCheck if this is not an error or something :)")
                logger.info("Sending event!")
                cdav.sendEvent(event)
        else:
            module = None
        
        last_module = module
    
    logger.info("Sleep for 120s")
    print("Sleep for 120s")
    time.sleep(120)
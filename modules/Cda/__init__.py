from modules.Site import Site as _Site
from modules.Config import Config
import json
from modules.Logger import Logger

class Site(_Site):
    def checkForChanges(self, url: str) -> bool:
        bs4 = self.getSite(url)
        episodes = bs4.findAll("div", {"class": "list-when-small tip"})
        if len(episodes) < 1:
            return False
        last_ep_config = self.getLastEp(url)
        if last_ep_config == "":
            self.setLastEp(url, str(len(episodes)))
            return False
        elif last_ep_config != str(len(episodes)):
            self.setLastEp(url, str(len(episodes)))
            return True
        else:
            return False
from modules.Site import Site as _Site
from modules.Config import Config
import json
from modules.Logger import Logger

class Site(_Site):
    def checkForChanges(self, url: str) -> bool:
        bs4 = self.getSite(url)
        episodes = bs4.findAll("ul", {"class": "episodios"})
        if len(episodes) < 1:
            return False
        else:
            episodes = episodes[0]
        last_ep = episodes.findAll("a")
        last_ep = last_ep[len(last_ep)-1].text
        last_ep_config = self.getLastEp(url)
        if last_ep_config == "":
            self.setLastEp(url, last_ep)
            return False
        elif last_ep_config != last_ep:
            self.setLastEp(url, last_ep)
            return True
        else:
            return False
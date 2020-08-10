from modules.Site import Site as _Site
from modules.Config import Config
import json
from modules.Logger import Logger
from urllib.parse import urlparse

class Site(_Site):
    def checkForChanges(self, url: str) -> bool:
        bs4 = self.getSite(url)
        episodes = bs4.find("table", {"class": "lista"})
        if len(episodes) < 1:
            return False
        
        hostname = urlparse(url).netloc
        last_ep = episodes.findAll("a")
        last_ep = last_ep[len(last_ep)-1]
        last_ep = "https://" + hostname + "/" + last_ep['href']
        last_ep_config = self.getLastEp(url)
        if last_ep_config == "":
            self.setLastEp(url, last_ep)
            return False
        elif last_ep_config != last_ep:
            self.setLastEp(url, last_ep)
            return True
        else:
            last_date_config = self.getLastEp(last_ep)
            last_date = episodes.findAll("td", {"class": "center"})
            last_date = last_date[len(last_date)-1].text
            if last_date_config == "":
                self.setLastEp(last_ep, last_date)
                return False
            elif last_date_config != last_date:
                self.setLastEp(last_ep, last_date)
                return True
            else:
                return False
from modules.Site import Site as _Site
from modules.Config import Config

class Site(_Site):
    def checkForChanges(self, url: str) -> bool:
        bs4 = self.getSite(url)
        episodes = bs4.find("ul", {"class": "episodes"})
        if not episodes:
            return False
        last_ep = episodes.findAll("a")
        last_ep = last_ep[len(last_ep)-1]['href']
        last_ep_config = self.getLastEp(url)
        if last_ep_config == "":
            self.setLastEp(url, last_ep)
            return False
        elif last_ep_config != last_ep:
            self.setLastEp(url, last_ep)
            return True
        else:
            return False
from bs4 import BeautifulSoup
import requests
import os
from modules.Config import Config
from modules.Logger import Logger

class Site:
    def __init__(self, config: Config, logger: Logger):
        self._author_ = "Majroch"
        self.config = config
        self.logger = logger
    
    def getSite(self, url: str) -> BeautifulSoup:
        html = requests.get(url).text
        beauty = BeautifulSoup(html, 'html.parser')
        return beauty

    def getProjectDir(self):
        return self.config.get("current_dir")
    
    def getLastEp(self, url: str) -> str:
        if not os.path.isfile(self.config.get("anime_state_cfg")):
            anime_state = Config(self.config.get("anime_state_cfg"), True)
            self.logger.warning("Cannot find file of last state! Creating.")
        else:
            anime_state = Config(self.config.get("anime_state_cfg"), True)
        
        if anime_state.has(url):
            return anime_state.get(url)
        else:
            return ""
    
    def setLastEp(self, url: str, ep: str):
        if not os.path.isfile(self.config.get("anime_state_cfg")):
            anime_state = Config(self.config.get("anime_state_cfg"), True)
            self.logger.warning("Cannot find file of last state! Creating.")
        else:
            anime_state = Config(self.config.get("anime_state_cfg"), True)
        
        if anime_state.has(url):
            anime_state.update(url, ep)
        else:
            anime_state.write(url, ep)
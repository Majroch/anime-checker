from modules.Config import Config
import datetime
from urllib.parse import urlparse
import os

try:
    import vobject #pylint: disable=import-error
except ImportError:
    print("No module found: vobject. Trying to Install")
    try:
        os.system("pip install vobject")
        import vobject #pylint: disable=import-error
    except:
        print("Cannot install and enable: vobject!")

try:
    import caldav #pylint: disable=import-error
except ImportError:
    print("No module found: vobject. Trying to Install")
    try:
        os.system("pip install caldav")
        import caldav #pylint: disable=import-error
    except:
        print("Cannot install and enable: vobject!")

class CalDavManager:
    def __init__(self, config: Config):
        self.config = config
    
    def createEvent(self, title: str="New Chapter - Anime", body: str="Change occured! Maybe new chapter! Or just a bug :/\nIf so, then check log for (maybe) some bug fixes :P"):
        now = datetime.datetime.now()
        calendar = vobject.iCalendar()
        calendar.add('vevent').add('summary').value = title
        calendar.vevent.add('description').value = body

        valarm = calendar.vevent.add('valarm')
        valarm.add('action').value = "AUDIO"
        if now.hour >= 16 and now.hour < 20:
            calendar.vevent.add('dtstart').value = datetime.datetime(now.year, now.month, now.day, 20, 0, 0, 0)
            calendar.vevent.add('dtend').value = datetime.datetime(now.year, now.month, now.day, 21, 0, 0, 0)
            valarm.add('trigger').value = datetime.datetime(now.year, now.month, now.day, 20, 0, 0, 0)
        elif now.hour > 20:
            calendar.vevent.add('dtstart').value = datetime.datetime(now.year, now.month, now.day+1, 16, 0, 0, 0)
            calendar.vevent.add('dtend').value = datetime.datetime(now.year, now.month, now.day+1, 17, 0, 0, 0)
            valarm.add('trigger').value = datetime.datetime(now.year, now.month, now.day+1, 16, 0, 0, 0)
        else:
            calendar.vevent.add('dtstart').value = datetime.datetime(now.year, now.month, now.day, 16, 0, 0, 0)
            calendar.vevent.add('dtend').value = datetime.datetime(now.year, now.month, now.day, 17, 0, 0, 0)
            valarm.add('trigger').value = datetime.datetime(now.year, now.month, now.day, 16, 0, 0, 0)
        
        return calendar
    
    def sendEvent(self, event: vobject.icalendar.VCalendar2_0):
        url_caldav2 = self.config.get("webdav_calendar")
        url_caldav = urlparse(url_caldav2)
        url_caldav2 = urlparse(url_caldav2)
        url_caldav = url_caldav._replace(netloc="{}:{}@{}".format(self.config.get("webdav_login"), self.config.get("webdav_password"), url_caldav.hostname))

        dav = caldav.DAVClient(url_caldav)
        principal = dav.principal()
        calendars = principal.calendars()

        cal = None

        if len(calendars) > 0:
            for calendar in calendars:
                calendar_parsed = urlparse(str(calendar.url))
                if calendar_parsed.hostname == url_caldav2.hostname and calendar_parsed.path == url_caldav2.path:
                        cal = calendar
        
        return cal.add_event(event.serialize())
from datetime import datetime
from json import dump, load
from os import getenv, system
import shlex
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests import get, post
from tracker import LOGGER

load_dotenv("vars.env")
BOT_TOKEN = str(getenv("BOT_TOKEN"))


class Linux:
    @staticmethod
    def get_versions():
        """
        Scrape the latest kernel versions from kernel.org and save it in a list 
        """
        url = "https://www.kernel.org"
        page = get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        releases_table = soup.find(id='releases')
        vert = releases_table.findAll('tr')
        vtable = {'mainline': '', 'stable': [], 'longterm': [], 'next': ''}
        for i in vert:
            td = i.find('td').text
            if td == 'mainline:':
                vtable['mainline'] = i.find('strong').text
            elif td == 'stable:':
                vtable['stable'].append(i.find('strong').text)
            elif td == 'longterm:':
                vtable['longterm'].append(i.find('strong').text)
            elif td == 'linux-next:':
                vtable['next'] = i.find('strong').text
        return vtable

    @staticmethod
    def write_file():
        """
        Write the latest available kernel versions as a json file with
        'mainline' being the latest available mainline kernel and stable
        and longterm kernels as 'stable' and the 'longterm' respectively
        """
        data = Linux.get_versions()
        with open('data.json', 'w') as f:
            dump(data, f, indent=4)

    @staticmethod
    def get_file_content():
        """
        Get contents from data.json file and save it as a data dictionary
        """
        with open('data.json', 'r') as f:
            data = load(f)
        return data

    @staticmethod
    def is_updated():
        """
        Get the contents from data.json and compare it with the scraped data from
        kernel.org and return mainline as Boolean as there will be only a single 
        mainline kernel and Stable and Longterm Kernels as list.
        """
        realdat = Linux.get_versions()
        fildat = Linux.get_file_content()
        mainline = realdat['mainline'] == fildat['mainline']
        stable = [i for i in realdat['stable'] if i not in fildat['stable']]
        longterm = [i for i in realdat['longterm']
                    if i not in fildat['longterm']]
        nex = realdat['next'] == fildat['next']
        return mainline, stable, longterm, nex

    @staticmethod
    def updatable_kernels():
        """
        Returns the list of updatable kernels
        """
        main, sta, lon, nex = Linux.is_updated()
        da = Linux.get_versions()
        dict_keys = [x for x in da.keys()]
        updates = []
        key = []
        if not main:
            updates.append(da['mainline'])
            key.append(dict_keys[0])

        if sta:
            updates.extend(sta)
            for _ in range(len(sta)):
                key.append(dict_keys[1])

        if lon:
            updates.extend(lon)
            for _ in range(len(lon)):
                key.append(dict_keys[2])

        if not nex:
            updates.append(da['next'])
            key.append(dict_keys[3])

        if updates:
            Linux.write_file()
            Linux.git_push()

        return updates, key

    @staticmethod
    def git_push():
        """
        Pushes the data.json regularly to git everytime any kernel gets updates
        """
        nw = datetime.today()
        today = nw.strftime("%d-%m-%Y %H%M%S")
        github_oauth = str(getenv("GITHUB_OAUTH"))
        system(
            "git config user.name 'dracarys18' && git config user.email karthihegde010@gmail.com && git add data.json && git commit -m \"[Kernel] sync: {0}\" && git push -q https://{1}@github.com/dracarys18/Kernel_Tracker.git HEAD:master".format(today, github_oauth))

    @staticmethod
    def post_to_channel(message):
        """
        Post the message into the channel using HTTP POST
        """
        pars = (
            ('chat_id', -1001195071888),
            ('text', str(message)),
            ('parse_mode', "HTML"),
            ('disable_web_page_preview', "yes")
        )
        url = "https://api.telegram.org/bot{0}/sendMessage".format(BOT_TOKEN)
        req = post(url, params=pars)
        status = req.status_code
        reason = req.reason
        if status == 200:
            LOGGER.info("Message sent")
        else:
            LOGGER.warning(
                "Cant sent the message\n Error Code:-\n{0}:{1}".format(str(status), reason))

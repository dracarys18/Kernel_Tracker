from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from os import system,path,getenv
from requests import get,post
from json import dump,load
import logging

load_dotenv("vars.env")
BOT_TOKEN = str(getenv("BOT_TOKEN"))
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)
class Linux:
    def __init__(self):
        if not path.exists("data.json"):
            self.write_file()
    
    def get_versions(self):
        """
        Scrape the latest kernel versions from kernel.org and save it in a list 
        """
        url = "https://www.kernel.org"
        page = get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        releases_table = soup.find(id='releases')
        vert = releases_table.findAll('tr')
        vtable = {'mainline':'','stable':[],'longterm':[],'next':''}
        for i in vert:
            td = i.find('td').text
            if td=='mainline:':
                vtable['mainline'] = i.find('strong').text
            elif td=='stable:':
                vtable['stable'].append(i.find('strong').text)
            elif td=='longterm:':
                vtable['longterm'].append(i.find('strong').text)
            elif td=='linux-next:':
                vtable['next']=i.find('strong').text
        return vtable
    

    def write_file(self):
        """
        Write the latest available kernel versions as a json file with
        'mainline' being the latest available mainline kernel and stable
        and longterm kernels as 'stable' and the 'longterm' respectively
        """
        data = self.get_versions()
        with open('data.json','w') as f:
            dump(data,f)

        
    def get_file_content(self):
        """
        Get contents from data.json file and save it as a data dictionary
        """
        with open('data.json','r') as f:
            data = load(f)
        return data

    def is_updated(self):
        """
        Get the contents from data.json and compare it with the scraped data from
        kernel.org and return mainline as Boolean as there will be only a single 
        mainline kernel and Stable and Longterm Kernels as list.
        """
        realdat = self.get_versions()
        fildat = self.get_file_content()
        mainline = realdat['mainline']==fildat['mainline']
        stable = [i for i in realdat['stable'] if i not in fildat['stable']]
        longterm = [i for i in realdat['longterm'] if i not in fildat['longterm']]
        nex = realdat['next']==fildat['next']
        return mainline,stable,longterm,nex

    def updatable_kernels(self):
        """
        Returns the list of updatable kernels
        """
        main,sta,lon,nex = self.is_updated()
        da = self.get_versions()
        dict_keys = [x for x in da.keys()]
        updates = []
        key = []
        if not main:
            updates.append(da['mainline'])
            key.append(dict_keys[0])

        if sta:
            updates.extend(sta)
            for i in range(len(sta)):
                key.append(dict_keys[1])

        if lon:
            updates.extend(lon)
            for i in range(len(lon)):
                key.append(dict_keys[2])

        if not nex:
            updates.append(da['next'])
            key.append(dict_keys[3])
    
        if updates:
            self.write_file()
            self.git_push()

        return updates,key
    
    def git_push(self):
        """
        Pushes the data.json regularly to git everytime any kernel gets updates
        """
        nw = datetime.today()
        today = nw.strftime("%d-%m-%Y")
        github_oauth=str(getenv("GITHUB_OAUTH"))
        system("git config user.name 'dracarys18' && git config user.email karthihegde010@gmail.com && git add data.json && git commit -m \"[Kernel] sync: {0}\" && git push -q https://{1}@github.com/dracarys18/Kernel_Tracker.git HEAD:master".format(today,github_oauth))
    
    def post_to_channel(self,message):
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
        req = post(url,params=pars)
        status = req.status_code
        if status==200:
            LOGGER.info("Message sent")
        else:
            LOGGER.warn("Cant sent the message\n Error Code:-"+str(status))


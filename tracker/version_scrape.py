from bs4 import BeautifulSoup
from datetime import datetime
from os import system,path,getenv
import requests
import json

class Linux:
    def __init__(self):
        if not path.exists("data.json"):
            self.write_file()
    
    def get_versions(self):
        """
        Scrape the latest kernel versions from kernel.org and save it in a list 
        """
        url = "https://www.kernel.org"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        releases_table = soup.find(id='releases')
        versions = releases_table.findAll('strong')
        vtable = {'mainline':versions[0].text,'stable':versions[1].text,'longterm':[]}
        for i in versions[2:]:
            vtable['longterm'].append(i.text)
        return vtable
    

    def write_file(self):
        """
        Write the latest available kernel versions as a json file with
        'mainline' being the latest available mainline kernel and stable
        and longterm kernels as 'stable' and the 'longterm' respectively
        """
        data = self.get_versions()
        with open('data.json','w') as f:
            json.dump(data,f)

        
    def get_file_content(self):
        """
        Get contents from data.json file and save it as a data dictionary
        """
        with open('data.json','r') as f:
            data = json.load(f)
        return data

    def is_updated(self):
        """
        Get the contents from data.json and compare it with the scraped data from
        kernel.org and return 3 booleans.
        """
        realdat = self.get_versions()
        fildat = self.get_file_content()
        mainline = realdat['mainline']==fildat['mainline']
        stable = realdat['stable']==fildat['stable']
        longterm =[]
        for i in range(len(realdat['longterm'])):
            longterm.append(fildat['longterm'][i]==realdat['longterm'][i])
        return mainline,stable,longterm
    
    def updatable_kernels(self):
        """
        Returns the list of updatable kernels
        """
        updatable=False
        main,sta,lon = self.is_updated()
        da = self.get_versions()
        updates = []
        if not main:
            updatable=True
            updates.append(da['mainline'])

        if not sta:
            updatable=True
            updates.append(da['stable'])

        for i in range(len(lon)):
            if not lon[i]:
                updatable=True
                updates.append(da['longterm'][i])
    
        if updatable:
            self.write_file()
            self.git_push()
        return updates
    
    def git_push(self):
        """
        Pushes the data.json regularly to git everytime any kernel gets updates
        """
        nw = datetime.today()
        today = nw.strftime("%d-%m-%Y")
        github_oauth=str(getenv("GITHUB_OAUTH"))
        system("git config user.name 'dracarys18' && git config user.email karthihegde010@gmail.com && git add data.json && git commit -m \"[Kernel] sync: {0}\" && git push -q https://{1}@github.com/dracarys18/Kernel_Tracker.git HEAD:master".format(today,github_oauth))
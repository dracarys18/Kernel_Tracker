<h1>Channel</h1>
<a href='https://t.me/kernel_tracker'>Kernel Tracker</a> is the channel where the bot will be sending the updates in.
<h1>Introduction</h1>
This is a Telegram Bot to Track Kernel Upstreams <a href='https://www.kernel.org/'>kernel.org</a> and send it to a telegram channel specified. I used BeautifulSoup to scrape the data from the kernel.org website and telethon to send the message to the channel.

<h1>Configuration</h1>
<ol>
<li>Get the API ID and API hash from <a href='https://my.telegram.org/'>my.telegram.org</a>. And Bot API Key from <a href='https:/t.me/botfather'>@BotFather</a></li>
<li>Fill the values in <code>vars_sample.env</code> and rename it into <code>vars.env</code>.</li>
<li>And run the bot by running:-
<pre><code>python3 -m tracker</pre></code>
</li>
</ol>
<h1>Other uses</h1>
The bot regularly updates the data.json whenever the new Kernel gets released. So you can fetch data.json and create your own module to get you a remainder about the Kernel Upstreams. An example is given below.

```python
import requests
'''
Write your own function post the message
in group/channel for this example purpose
I will take the function as post_to_telegram(text)
'''

def check_updates():
    r=''
    while True:
        resp = requests.get("https://raw.githubusercontent.com/dracarys18/Kernel_Tracker/master/data.json").json()
        for i in resp['longterm']:
            if i.startswith('4.14') and i!=r:
                r=i
                post_to_telegram(i+'arrived')
```

 
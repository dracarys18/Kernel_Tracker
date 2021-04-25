<h1>Channel</h1>
<a href='https://t.me/kernel_tracker'>Kernel Tracker</a> is the channel where the bot will be sending the updates in.
<h1>Introduction</h1>
This is a Telegram Bot to Track Kernel Upstreams <a href='https://www.kernel.org/'>kernel.org</a> and send it to a telegram channel specified. I used BeautifulSoup to scrape the data from the kernel.org website and telegram http api to send the message to the channel.

<h1>Configuration</h1>
<ol>
<li> Get Bot API Key from <a href='https:/t.me/botfather'>@BotFather</a></li>
<li>Fill the values in <code>vars_sample.env</code> and rename it into <code>vars.env</code>.</li>
<li>And run the bot by running:-
<pre><code>python3 -m tracker</pre></code>
</li>
</ol>
<h1>Other uses</h1>
The bot regularly updates the data.json whenever the new Kernel gets released. So you can fetch data.json and create your own module to get you a remainder about the Kernel Upstreams. An example repository is here. 
<p><a href="https://github.com/dracarys18/4.14-tracker.git">4.14 Tracker</a></p>


 
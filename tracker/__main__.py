import os
from tracker import client
from tracker import lin

def main():
    updatables = lin.updatable_kernels()
    client.parse_mode = 'html'
    if updatables:
        for i in updatables:
            client.send_message(-1001195071888,"<strong>New Kernel version available</strong>\n<a href='https://www.kernel.org/'>{0}</a>".format(i))

if __name__=="__main__":
    bot_token=str(os.getenv("BOT_TOKEN"))
    client.start(bot_token=bot_token)
    while True:
        main()
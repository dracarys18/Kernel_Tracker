import os
from tracker import client
from tracker import lin

def main():
    updatables = lin.updatable_kernels()
    client.parse_mode = 'html'
    href=''
    if updatables:
        for i in updatables:
            if str(i).startswith("next"):
                href='https://www.kernel.org/'
            else:
                href='https://git.kernel.org/torvalds/h/{0}'.format(str(i))

            client.send_message(-1001195071888,"<strong>New Kernel version available</strong>\n<a href='{0}'>{1}</a>".format(href,i))

if __name__=="__main__":
    bot_token=str(os.getenv("BOT_TOKEN"))
    client.start(bot_token=bot_token)
    while True:
        main()
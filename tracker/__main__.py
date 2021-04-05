import os
from tracker import client,lin,LOGGER
from time import sleep

def main():
    updatables = lin.updatable_kernels()
    client.parse_mode = 'html'
    href=''
    if updatables:
        for i in updatables:
            if str(i).startswith("next"):
                href='https://www.kernel.org/'
            else:
                href='https://git.kernel.org/torvalds/h/v{0}'.format(str(i))
            try:
                client.send_message(-1001195071888,"<strong>New Kernel version available</strong>\n<a href='{0}'>{1}</a>".format(href,i))
            except Exception as e:
                LOGGER.error(e)

if __name__=="__main__":
    bot_token=str(os.getenv("BOT_TOKEN"))
    client.start(bot_token=bot_token)
    LOGGER.info("Bot has started")
    while True:
        main()
        sleep(3)

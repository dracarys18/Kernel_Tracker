import os
from tracker import lin,LOGGER
from time import sleep

def main():
    updatables = lin.updatable_kernels()
    href=''
    if updatables:
        for i in updatables:
            if str(i).startswith("next"):
                href='https://www.kernel.org/'
            else:
                href='https://git.kernel.org/torvalds/h/v{0}'.format(str(i))
            message="<strong>New Kernel version available</strong>\n<a href='{0}'>{1}</a>".format(href,i)
            lin.post_to_channel(message)
    
if __name__=="__main__":
    LOGGER.info("Bot has started")
    while True:
        main()
        sleep(3)

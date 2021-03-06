from os import path

from tracker import LOGGER
from tracker.module.version_scrape import Linux


def main():
    if not path.exists("data.json"):
        Linux.write_file()
    updatables, keys = Linux.updatable_kernels()
    href = ''
    if updatables:
        for i, values in enumerate(updatables):
            if values.startswith("next"):
                href = 'https://www.kernel.org/'
            else:
                href = 'https://git.kernel.org/stable/h/v{0}'.format(values)
            message = "<strong>New {0} Kernel version available</strong>\n<a href='{1}'>{2}</a>".format(
                str(keys[i]).capitalize(), href, values)
            Linux.post_to_channel(message)


if __name__ == "__main__":
    LOGGER.info("Bot has started")
    main()

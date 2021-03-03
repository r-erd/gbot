# gbot

this is a telegram bot that regulary checks the website of "FSU Jena" for new grades regarding the exams you took.
it will notify you if there were any changes to your grades (or, more importantly new grades added). You can also trigger a manual check by sending the command "/check" to the bot.

!!!  you will have to get your own bot token from telegram and set this script up somewhere to run continously
> this is a work in progress and only a short draft

## Installation and Usage

requires 
- Python3
- pip
- chromedriver


```bash
pip3 install selenium
pip3 install python-telegram-bot
pip3 install bs4
pip3 install schedule
pip3 install html5lib

git clone https://github.com/r-erd/gbot.git
cd gbot

#add your chat_id, telegram-bot token and friedolin credentials to the code
#maybe adjust the chromedriver path

#start the script

sudo nohup python3 gbot.py &

```

## License
[MIT](https://choosealicense.com/licenses/mit/)


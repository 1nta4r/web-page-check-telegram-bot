import configparser
import requests
import hashlib
import logging
import dirlib
import time
import os


class WebCheckBot():

    def __init__(self) -> None:
        self.mode = 'default'
        self.bot_token = ''
        self.chat_id = ''
        self.timeout = 60
        self.urls_list = []


    # Check changes in url and send notification in telegram
    def report_changes(self, url: str):
        html_response = requests.get(url).text
        html_response_hash = str(hashlib.sha3_256(html_response.encode()).hexdigest())
        file_name = ''.join(x for x in url if x.isalpha()) + ".txt"
        dirpath = os.path.join('bd_dir',  file_name)
        if os.path.exists(dirpath):
            cache_file = open(dirpath, "r")
            html_cache = cache_file.read()
            if html_response_hash != html_cache:
                cache_file = open(dirpath, "w")
                cache_file.write(html_response_hash)
                self.send_to_bot("Changes detected at url: " + url)
        else:
            cache_file = open(dirpath, "w")
            cache_file.write(html_response_hash)


    # Check changes in gilab commits count
    def gitlab_report_changes(self, url: str):
        html_response = requests.get(url).text
        commits_count = html_response.split('</strong> Commits</a>')[0].split('>')[-1].strip()
        file_name = ''.join(x for x in url if x.isalpha()) + ".txt"
        dirpath = os.path.join('bd_dir',  file_name)
        if os.path.exists(dirpath):
            cache_file = open(dirpath, "r")
            html_cache = cache_file.read()
            if commits_count != html_cache:
                cache_file = open(dirpath, "w")
                cache_file.write(commits_count)
                self.send_to_bot("Changes detected at url: " + url)
        else:
            print("No cache file for " + url + " found, creating one...")
            with open (dirpath, "w") as cache_file:
                cache_file.write(commits_count)

    

    modes_list = {'default': report_changes, 'gitlab': gitlab_report_changes}


    # Init urls list from text file
    def set_urls_list_from_file(self, path_to_file: str):
        try:
            if os.path.isfile(path_to_file):
                with open(path_to_file) as urls_file:
                    urls_list = urls_file.readlines()
                self.urls_list = [url.strip() for url in urls_list]
        except:
            logging.warn('Cann\'t read urls file')
            pass
    

    # Change timeout between requests in code
    def set_timeout(self, new_timeout: int):
        if 86400 > new_timeout > 9:
            self.timeout = new_timeout 
        else:
            self.timeout = 60
            logging.info('Timeout is greater or less than the limit. The default value is set: {}'.format(60))


    # Set bot params from config file
    def set_params_from_config(self, path_to_config: str):
        config = configparser.ConfigParser()
        config.read(path_to_config)
        logging.info('Config file is loaded...')
        try:
            self.mode = config['MONITORING']['mode']
            self.bot_token = config['BOT']['token']
            self.chat_id = config['BOT']['chat_id']
            self.timeout = int(config['MONITORING']['timeout']) if 'timeout' in config['MONITORING'] else 60
            self.set_urls_list_from_file(os.path.join('configs',  config['MONITORING']['urls_list_filename']))
            logging.info('Params are set...')
            if self.bot_token == "''":
                logging.error('Bot token is empty!')
                raise ValueError('Bot token is empty!')
            elif self.chat_id == "''":
                logging.error('Chat id is empty!')
                raise ValueError('Chat id is empty!')      
        except:
            logging.warn('Some parameters are missing in the config file (token, chat_id, timeout)')
            exit(-1)


    def scan_urls(self):
        for url in self.urls_list:
            self.modes_list[self.mode](self, url)
            time.sleep(0.5)


    # Send notification to telegram
    def send_to_bot(self, bot_message):
        send_text = 'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatID}\
            &parse_mode=Markdown&text={bot_message}'.format(bot_token=self.bot_token, chatID=self.chat_id, bot_message=bot_message)
        response = requests.get(send_text)
        return response.json()


    def run(self):
        dirlib.reinit_dir('bd_dir')
        logging.info('Bot is running...')
        while True:
            self.scan_urls()
            time.sleep(self.timeout)
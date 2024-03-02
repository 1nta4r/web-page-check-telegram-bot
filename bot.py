import requests
import hashlib
import time
import os


BOT_TOKEN = ''
CHAT_ID = ''


def report_changes(url):
    html_response = requests.get(url).text
    html_response_hash = str(hashlib.sha3_256(html_response.encode()).hexdigest())
    file_name = ''.join(x for x in url if x.isalpha()) + ".txt"
    if os.path.exists(file_name):
        cache_file = open(file_name, "r")
        html_cache = cache_file.read()
        if html_response_hash != html_cache:
            cache_file = open(file_name, "w")
            cache_file.write(html_response_hash)
            send_to_bot("Changes detected at url: " + url)
    else:
        print("No cache file for " + url + " found, creating one...")
        cache_file = open(file_name, "w")
        cache_file.write(html_response_hash)


def scan_urls():
    with open("urls.txt") as urls_file:
        urls_list = urls_file.readlines()
    urls_list = [x.strip() for x in urls_list]
    for url in urls_list:
        report_changes(url)
        time.sleep(1)


def send_to_bot(bot_message):
    send_text = 'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatID}\
        &parse_mode=Markdown&text={bot_message}'.format(bot_token=BOT_TOKEN, chatID=CHAT_ID, bot_message=bot_message)
    response = requests.get(send_text)
    return response.json()


def run():
    while True:
        scan_urls()
        time.sleep(10)
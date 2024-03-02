import logging
import bot

if __name__ == '__main__':
    logging.basicConfig(filename='WebCheckBot.log', level=logging.INFO)
    bot_instance = bot.WebCheckBot()
    bot_instance.set_params_from_config('bot_config.ini')
    bot_instance.send_to_bot('Bot started!')
    bot_instance.run()






#!/usr/bin/env python3
import logging
import telebot as telegram
import yaml
import random
import json

total_messages = {}

def main(configpath, loglevel=logging.INFO):
    
    
    with open(configpath, "r") as f:
        config = yaml.safe_load(f)
    
    try:        
        with open(config["database"], "r") as f:
            total_messages = json.loads(f.read())
    except Exception as e:
        logging.warning(e)

    bot = telegram.TeleBot(config['bot_token'])

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        logging.info(message)
        bot.reply_to(message, """Hey, I am a bot created by @Kindest96. Please, feel free to use me :)""")
        
    @bot.message_handler(commands=['help'])
    def send_welcome(message):
        logging.info(message)
        bot.reply_to(message, """Type /random to get something.... well? random!! ofcourse
        This bot is made by @Kindest96
        and code is available at github.com/Kindest96""")
        

    @bot.message_handler(commands=['random'])
    def send_anime_meme(message):
        
        while 1:
            
            random_channel_index = random.randint(1, message.date)%len(total_messages)
            channels = list(total_messages.keys())
            random_channel = channels[random_channel_index]

            random_message = random.randint(1, message.date)
            random_message %= total_messages[random_channel]
            
            try:
                bot.forward_message(message.chat.id, random_channel, random_message)
            except:
                pass
            else:
                break
                
        #bot.reply_to(message, random_int)
        
    @bot.channel_post_handler(commands=['cache'])
    def update_messages_count(message):
        
        if message.chat.type != "private":
            total_messages["@"+message.chat.username] = message.message_id - 1
        else:
            bot.reply_to(message,"Sorry, your channel is private :'(")

        
        try:
            with open(config["database"], "w") as f:
                f.write(json.dumps(total_messages))
        except Exception as e:
            logging.warning(e)
        
        try:        
            with open(config["database"], "rb") as f:
                bot.send_document(config["creator"], f)
        except Exception as e:
            logging.warning(e)
    
    @bot.channel_post_handler(func=lambda m: True)
    def echo_all(message):
        if message.chat.type != "private":
            total_messages["@"+message.chat.username] = message.message_id
    
    bot.polling()
    
    logging.basicConfig(format="%(levelname)-7s [%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=loglevel)
    logging.info(config)
    
    print(config)

if __name__ == "__main__":
    
    configpath = "./config.yaml"
    
    loglevel = logging.INFO
    
    main(configpath, loglevel)
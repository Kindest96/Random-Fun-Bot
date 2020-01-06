#!/usr/bin/env python3
import logging
import telebot as telegram
import yaml
import random
import json

total_messages = {}
temp_channel = [""]

def main(configpath, loglevel=logging.INFO):
    
    
    with open(configpath, 'r') as f:
        config = yaml.safe_load(f)
    
    try:        
        with open(config['database'], 'r') as f:
            total_messages = json.loads(f.read())
    except Exception as e:
        logging.warning(e)

    bot = telegram.TeleBot(config['bot_token'])

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        logging.info(message)
        bot.reply_to(message, """Hey, I am a bot created by @Kindest96. Please, feel free to use me :)""")
        
    @bot.message_handler(commands=['help'])
    def send_help(message):
        logging.info(message)
        bot.reply_to(message, 
"""Type /random to get something.... well? random!! ofcourse
This bot is made by @Kindest96
and code is available at github.com/Kindest96""")
        

    @bot.message_handler(commands=['random'])
    def send_random(message):
        
        while 1:
            
            random_channel_index = random.randint(1, message.date)%len(total_messages)
            channels = list(total_messages.keys())
            random_channel = channels[random_channel_index]

            random_message = random.randint(1, message.date)
            random_message %= total_messages[random_channel]
            
            try:
                forwarded_message = bot.forward_message(message.chat.id, random_channel, random_message)
                if ('@'+forwarded_message.forward_from_chat.username) == random_channel:
                    break
                else:
                    bot.delete_message(forwarded_message.chat.id, forwarded_message.message_id)
            except:
                pass
                
        #bot.reply_to(message, random_int)
    
    @bot.message_handler(commands=['random_10'])
    def send_random_10(message):
        if message.chat.type == 'private':
            for count in range(10):
                send_random(message)
        else:
            bot.reply_to(message, '_This command only works in private message_', parse_mode='Markdown')

    
    @bot.message_handler(commands=['get_db'])
    def get_db(message):
        if message.chat.id == config['creator']:
            try:
                with open(config['database'], 'w') as f:
                    f.write(json.dumps(total_messages))
                
                with open(config['database'], 'rb') as f:
                    bot.send_document(config['creator'], f)
            except Exception as e:
                logging.warning(e)
        else:
            bot.reply_to(message, 'Haha! Nice try :)')
            
    @bot.message_handler(commands=['get_channels'])
    def get_channels(message):
        if message.chat.id == config['creator']:
            channel_info = "Channels\tTotal posts"
            for channel, post in total_messages.items():
                channel_info += "\n"+channel+"\t"+str(post)
            bot.reply_to(message, channel_info)
        else:
            bot.reply_to(message, 'Haha! Nice try :)')
            
            
    @bot.channel_post_handler(commands=['add_channel'])
    def add_this_channel(message):
        try:
            if message.chat.type != 'private':
                if ('@'+message.chat.username) not in total_messages:
                    temp_channel[0] = message.chat.username
                    markup = telegram.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.add('Yes', 'No')
                    confirm = bot.send_message(config['creator'], 'Do you want to add @'+message.chat.username+' to your bot?', reply_markup=markup)
                    bot.register_next_step_handler(confirm, confirm_from_creator)
                else:
                    bot.reply_to(message,"Your channel is already in the bot")
            else:
                bot.reply_to(message,"Sorry, your channel is private :'(")
        except Exception as e:
            logging.warning(e)

    
    @bot.channel_post_handler(commands=['cache'])
    def update_messages_count(message):
        try:
            if message.chat.type != 'private':
                if ('@'+message.chat.username) in total_messages.keys():
                    total_messages['@'+message.chat.username] = message.message_id - 1
                    bot.send_message(config['creator'], '@'+message.chat.username+' cached the channel')
                else:
                    bot.reply_to(message,"Permission denied. Use //add_channel to add your channel and ask the creator to allow it")
            else:
                bot.reply_to(message,"Sorry, your channel is private :'(")
        except Exception as e:
            logging.warning(e)

    
    @bot.channel_post_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice'])
    def echo_all(message):
        if message.chat.type != 'private':
            if ('@'+message.chat.username) in total_messages.keys():
                total_messages['@'+message.chat.username] = message.message_id
            
            
    def confirm_from_creator(message):
        markup = telegram.types.ReplyKeyboardRemove()
        username = temp_channel[0]
        if message.text == "Yes":
            total_messages['@'+username] = 0
            bot.reply_to(message, "@"+username+" was added to the bot", reply_markup=markup)
        else:
            bot.reply_to(message, "@"+username+" was not added to the bot", reply_markup=markup)
        temp_channel[0] = ""
            
    bot.polling()
    
    logging.basicConfig(format='%(levelname)-7s [%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=loglevel)
    logging.info(config)
    
    # print(config)

if __name__ == '__main__':
    
    configpath = './config.yaml'
    
    loglevel = logging.INFO
    
    main(configpath, loglevel)
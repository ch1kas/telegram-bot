import telebot
import requests
import GetOldTweets3 as got
from telebot import types
from decouple import config
import os
bot = telebot.TeleBot(config("TOKEN"))

@bot.message_handler(commands=['start', 'go'])
def start_message(message):
    global chat_id
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Hello! Which accounts do you wish to get the tweets from?\n'
                                      'Enter account names with space in between!\n'
                                      'Ex:lifehacker theeconomist ap ')

@bot.message_handler(content_types=['text'])
def send_text(message):
    global list_of_accounts
    list_of_accounts = str(message.text.lower()).split()
    print(list_of_accounts)
    text = message.text
    msg = bot.send_message(chat_id, 'How many tweets do you want from each account? Enter a positive integer')
    bot.register_next_step_handler(msg, ask_number_of_tweets)

@bot.message_handler(content_types=['text'])
def ask_number_of_tweets(message):
    text = message.text
    if int(text) < 0 or not text.isdigit():
        msg = bot.send_message(
            chat_id, 'Number should be a positive integer! Enter one more time')
        bot.register_next_step_handler(msg, ask_number_of_tweets)  # askSource
        return
    maximum = int(text)
    print(maximum)
    msg = bot.send_message(chat_id, 'Sending the tweets...')
    send_tweets(maximum)




def send_tweets(maximum):

    for account in list_of_accounts:
        # print(account)

        tweetCriteria = got.manager.TweetCriteria().setUsername(account)\
            .setMaxTweets(maximum)\
            .setEmoji("unicode")
        bot.send_message(chat_id, account)
        print(account)

        for i in range(maximum):
            try:
                tweet = got.manager.TweetManager.getTweets(tweetCriteria)[i]
                # print(tweet.username)
                print(tweet.text)
                # string = str(tweet.text)
                # print(string)
                bot.send_message(chat_id, tweet.text)
                bot.send_message(chat_id, "------------------------------------------------------")

            except:
                bot.send_message(chat_id, "Some error")
                # continue




bot.polling()

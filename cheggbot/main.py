import telebot
from header_file import *
import time
import pymongo, dns
from pymongo import MongoClient
import pandas as pd
import os
from re import search
import json
from bs4 import BeautifulSoup
import requests
import os.path
from cookies import cookieDict
from cookies import user_agents
from datetime import timedelta
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import requests
import unicodedata
import numpy as np
from api_utils import *

os.system("powershell -command $host.ui.RawUI.WindowTitle = 'Cheggbot'")
TOKEN = ''
bot = telebot.TeleBot(TOKEN)
print(os.getcwd())

ua = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36'
]

cluster = MongoClient(
    "mongodb+srv://unblur:Cheggunblur@cluster0.anpju.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = cluster["data"]

collection = db["data"]

linkdb = cluster["links"]
linkcollection = linkdb["list"]

query = {'_id': 0}

get_user_data = collection.find(query)

for i in get_user_data:
  data1 = i
  print(data1)


adminID = 2110818173
def save_link(link, Id, chances):
  mydict = {'link': link, 'chat_id': Id, 'chances': chances}
  x = linkcollection.insert_one(mydict)
  print('link saved')


bot.send_message(adminID, 'hello')


class User_Data:

  def add_lost_chance(self, chat_id):
    user = collection.find_one({'_id': chat_id})

    current_chance = user['credit']
    updated_chance = current_chance + 2

    update = {"$set": {'credit': updated_chance}}
    collection.update_one({'_id': chat_id}, update)


UserData = User_Data()


class CheggAccount:

  def switch(self):
    cookiesFile = open("cookiefile.txt").read()
    cookiesList = cookiesFile.splitlines()
    global SUScookies
    SUScookies = cookiesList[0]
    global NXTcookies
    try:
      NXTcookies = cookiesList[1]
    except:
      NXTcookies = cookiesList[0]
    changeIndex = cookiesList.pop(0)
    cookiesList.append(SUScookies)
    CookieFile = open("cookiefile.txt", "w")
    for cookies in cookiesList:
      CookieFile.write(cookies + "\n")
    CookieFile.close()

  def delete(self):
    cookiesFile = open("cookiefile.txt").read()
    cookiesList = cookiesFile.splitlines()
    global suscookies
    suscookies = cookiesList[0]
    global nxtcookies
    nxtcookies = cookiesList[1]
    cookiesList.pop(0)
    CookieFile = open("cookiefile.txt", "w")
    for cookies in cookiesList:
      CookieFile.write(cookies + "\n")
    CookieFile.close()

  def using(self):
    cookiesFile = open("cookiefile.txt").read()
    cookiesList = cookiesFile.splitlines()
    global usingcookies
    usingcookies = cookiesList[0]


Account = CheggAccount()


class cookies:

  def get_cookies(self):
    cookiesFile = open("cookiefile.txt").read()
    cookiesList = cookiesFile.splitlines()
    cookies = cookiesList[0]

    COOKIE = cookieDict[cookies]

    return COOKIE, cookies

  def get_user_agent(self):

    return random.choice(user_agents)


Cookies_list = cookies()


def gen_plan():
  plan = InlineKeyboardMarkup()
  plan.row_width = 2
  plan.add(InlineKeyboardButton("Indian", callback_data="cb_yes"),
           InlineKeyboardButton("International", callback_data="cb_no"),
           InlineKeyboardButton("🪙 Pay via Crypto 🪙", callback_data="crypto"))
  return plan


def join_channel():
  plan = InlineKeyboardMarkup()
  plan.row_width = 2
  plan.add(
      InlineKeyboardButton("Join Channel",
                           url='https://t.me/cheggnx'))
  return plan


def gen_start():
  start = InlineKeyboardMarkup()
  start.row_width = 2
  start.add(InlineKeyboardButton("❕How to use❕", callback_data="How"),
            InlineKeyboardButton("❕How to buy❕", callback_data="Buy"))
  start.add(
      InlineKeyboardButton("🔅Check remaining credits🔅",
                           callback_data="Credit"),
      InlineKeyboardButton("⚜️  Contact us  ⚜️", callback_data="Contact"))
  start.add(
      InlineKeyboardButton("Get your first free solution",
                           callback_data="Offers"))
  return start


def gen_Main_menu():
  Main_menu = InlineKeyboardMarkup()
  Main_menu.row_width = 2
  Main_menu.add(
      InlineKeyboardButton("Go to Main Menu", callback_data="Main_menu"))
  return Main_menu


content_types = ["text", "document"]
bot.last_message_sent = {}


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  #print(call)
  try:
    if call.data == "cb_yes":
      try:
        bot.delete_message(call.from_user.id,
                           bot.last_message_sent[call.from_user.id])
      except Exception as e:
        print(e)
      bot.answer_callback_query(call.id, "")
      doc = open("qr.jpg", 'rb')
      msg = bot.send_photo(
          call.from_user.id,
          doc,
          caption=
          '<b>Plans for Indians are as follow</b>\n\nNO EXPIRY DATE OF ANY PLANS\n\n50Rs = 20 soltuions\n100Rs = 45 solutions\n200Rs = 100 solutions\n500Rs = 280 solutions\n1000Rs = 600 solutions\n\n🔅UPI ID : chegg2rs@sbi\n🔅PayTM link : https://paytm.me/b-cK4qV\n\n<b>Rules:-</b>\n\nSend the payment screenshot to @The_admin_freeport within 5 minutes after transaction\n\n<b>--> Late payment screen shot will not accept you have to send with in 5 minutes</b>\n\n<b>--> If transcation failed or under processing inform admin</b>\n\n<b>--> Dont send same payment screen shot from multiple accounts</b>\n\n<b>--> Dont delete bot and admin chats</b>\n\n<b>Thankyou ❤️</b>',
          parse_mode='html',
          reply_markup=gen_Main_menu())
      bot.last_message_sent[call.from_user.id] = msg.message_id
    elif call.data == "crypto":
      try:
        bot.delete_message(call.from_user.id,
                           bot.last_message_sent[call.from_user.id])
      except Exception as e:
        print(e)
      bot.answer_callback_query(call.id, "")
      doc = open("crypto.jpg", 'rb')
      msg = bot.send_photo(
          call.from_user.id,
          doc,
          caption=
          '<b>We accpect BTC , ETH ,BNB , USDT and USD 🤑\n\n2$  = 30 solutions\n5$ = 100 solutions\n10$ = 250 solutions\n\nSend the payment screenshot to @The_admin_freeport within 5 minutes after transaction\n\n--> Failing to send the screenshot within 5 minutes after payment will not be considered\n\n--> If transcation failed or under processing inform admin\n\n--> Dont send same payment screen shot from multiple accounts</b>',
          parse_mode='html',
          reply_markup=gen_Main_menu())
      bot.last_message_sent[call.from_user.id] = msg.message_id

    elif call.data == "cb_no":
      try:
        bot.delete_message(call.from_user.id,
                           bot.last_message_sent[call.from_user.id])
      except Exception as e:
        print(e)
      msg = bot.send_message(
          call.from_user.id,
          '2$ = 30 solutions\n  5$ = 100 solutions\n 10$ = 250 solutions\n\n\nUse Paypal: paypal.me/lodumodi003\n\n\nSend the payment screenshot to @The_admin_freeport within 5 minutes after transaction\n\n<b>--> Late payment screen shot will not accept you have to send with in 5 minutes</b>\n\n<b>--> If transcation failed or under processing inform admin</b>\n\n<b>--> Dont send same payment screen shot from multiple accounts</b>\n\n<b>--> Dont delete bot and admin chats</b>\n\n<b>Thankyou ❤️</b>',
          parse_mode='html',
          reply_markup=gen_Main_menu())
      bot.answer_callback_query(call.id, "")
      bot.last_message_sent[call.from_user.id] = msg.message_id
    elif call.data == "How":
      try:
        bot.delete_message(call.from_user.id,
                           bot.last_message_sent[call.from_user.id])
      except Exception as e:
        print(e)
      bot.answer_callback_query(call.id, "")
      msg = bot.send_message(
          call.from_user.id,
          "🏁PROCESS FOR GETTING ANSWER FROM BOT.\n\nSTEP 1 ➡️  Type the exact question on google. I dont recommend using google lens as it is not accurate .\n\nSTEP 2 ➡️  Verify whether the question is same in chegg.com and it has been solved by an expert .\n\nSTEP 3 ➡️  Now, copy the exact link and paste it on the @chegg1rsbot .\n\nSTEP 4 ➡️  Please avoid sending additional texts just before the chegg link you send to bot. This happens automatically when you share the link from chrome mobile browser. To prevent auto generating such additional links, just copy the link from browser and paste in bot.\n\nThank you!",
          reply_markup=gen_Main_menu())
      bot.last_message_sent[call.from_user.id] = msg.message_id
    elif call.data == "Buy":
      try:
        bot.delete_message(call.from_user.id,
                           bot.last_message_sent[call.from_user.id])
      except Exception as e:
        print(e)
      msg = bot.send_message(call.from_user.id,
                             "*Choose the options according to your region*",
                             parse_mode='Markdown',
                             reply_markup=gen_plan())
      bot.answer_callback_query(call.id, "")
      bot.last_message_sent[call.from_user.id] = msg.message_id
    elif call.data == "Credit":
      try:
        bot.delete_message(call.from_user.id,
                           bot.last_message_sent[call.from_user.id])
      except Exception as e:
        print(e)
      msg = bot.send_message(
          call.from_user.id,
          "*How to check the remaining balance in bot*\n\nType this command 👉🏽 */account* to see your active balance",
          parse_mode='Markdown',
          reply_markup=gen_Main_menu())
      bot.answer_callback_query(call.id, "")
      bot.last_message_sent[call.from_user.id] = msg.message_id
    elif call.data == "Contact":
      try:
        bot.delete_message(call.from_user.id,
                           bot.last_message_sent[call.from_user.id])
      except Exception as e:
        print(e)
      msg = bot.send_message(
          call.from_user.id,
          "<b>Contact US</b>\n\nSend your queries to @The_admin_freeport",
          parse_mode='html',
          reply_markup=gen_Main_menu())
      bot.answer_callback_query(call.id, "")
      bot.last_message_sent[call.from_user.id] = msg.message_id
    elif call.data == "Offers":
      try:
        bot.delete_message(call.from_user.id,
                           bot.last_message_sent[call.from_user.id])
      except Exception as e:
        print(e)
      msg = bot.send_message(
          call.from_user.id,
          "We provide free soltuions to everyone who start this bot. Stop waiting and send links here!",
          parse_mode='Markdown',
          reply_markup=gen_Main_menu())
      bot.answer_callback_query(call.id, "")
      bot.last_message_sent[call.from_user.id] = msg.message_id

    elif call.data == "Main_menu":
      try:
        bot.delete_message(call.from_user.id,
                           bot.last_message_sent[call.from_user.id])
      except Exception as e:
        print(e)
      msg = bot.send_message(call.from_user.id,
                             'Choose the below buttons to interact with bot',
                             reply_markup=gen_start())
      bot.answer_callback_query(call.id, "")
      bot.last_message_sent[call.from_user.id] = msg.message_id

  except Exception as e:
    print(e)
    pass


def save_data(message, user):
  try:
    print('[*] User request processing')
    chat_id = str(message.chat.id)
    link = message.text

    chances_remaining = user['credit']
    chances_remaining -= 2

    update = {"$set": {'credit': chances_remaining}}
    collection.update_one({'_id': chat_id}, update)

    x = link.startswith("http")
    if chances_remaining > -1 and x == True:
      chances = int(chances_remaining / 2)
      QNA = '/questions-and-answers/'

      if search(QNA, link):
        qid = link.rsplit('-q', 1)[1].split('#')[0].split('?')[0]
        filenam = link.rsplit('-q', 1)[1]
        filename = filenam.split('?')[0]
        try:

          save_path = 'qna'
          name = filename + '.html'
          completeName = os.path.join(save_path, name)

          doc = open(completeName, 'rb')
          count = open('databasecount.txt').read()
          coun = int(count)
          coun += 1
          with open('databasecount.txt', 'w') as f:
            f.write(str(coun))
          bot.send_document(
              chat_id,
              doc,
              caption="*" + str(chances) +
              " chances remaining*\n\n *👆🏼Open above file in chrome browser to see answer👆🏼*\n\n 🎁We have *Gifted you free bot* 🎁\n\nClick here *@FREEPORTSUPERBOT* to open Your gift bot, and see yourself the use of it🤫. \n\nContact *@The_Admin_Freeport* for any queires",
              parse_mode='Markdown',
              reply_markup=gen_Main_menu())
          bot.send_message(
            adminID,
              str(chat_id) + ' DB ' + str(chances) + " no.of links= " +
              str(coun) + ' ' + str(qid))
          print('[*] Answer sent from DB\n_____________________________')

        except Exception as e:

          bot.send_message(
            adminID,
              str(message.chat.id) + "\n" + str(message.chat.first_name) +
              "\n" + str(message.chat.username) + "\nProcessing")

          #FINDING THE QUESTION

          headers = {
              'authority': 'gateway.chegg.com',
              'accept': '*/*, application/json',
              'accept-language': 'en-US,en;q=0.9',
              'apollographql-client-name': 'chegg-web',
              'apollographql-client-version': 'main-3a0d6502-6110088613',
              'authorization':
              'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
              'content-type': 'application/json',
              # 'cookie': 'CVID=836da399-d07e-4038-89cf-97497de77ea7; _pxvid=b1fee7de-a7c6-11ee-ac7e-87e118be0fa6; _cs_c=0; _fbp=fb.1.1704018264256.6923973; C=0; O=0; V=d5facd00f36e8cb1b6e922cd8ea2b37365914139f2a170.92238180; exp=C026A; _gcl_au=1.1.22532090.1704018265; _cc_id=1ba1e8c77cfddbe4303014e8f681d322; permutive-id=06ee83e6-316b-4cc3-a846-902ca584e5df; _ga=GA1.2.1301400995.1704018272; _tt_enable_cookie=1; _ttp=IGRJqSbeaB5sEB4yVGVxzEp8o48; _scid=ea51a8cd-0351-4d98-8391-ed50891f3273; _pubcid=74a25028-e914-4f6f-abf3-3f68f528200a; _au_1d=AU1D-0100-001704018520-ON8XALTC-9DAL; opt-user-profile=836da399-d07e-4038-89cf-97497de77ea7%252C25233851370%253A25301220086%252C25840920038%253A25769201400%252C26662330013%253A26666110055; langPreference=en-US; expkey=79A7691F71BAC645D371C3EA9C3C22DD; _sctr=1%7C1706725800000; connectId=%7B%22vmuid%22%3A%22oeKxkhudcRIH1JGQU89QAeGsL2gdU5Xb0brF1uzzfMC7Po4eke4b8zy7Vo57zzm_7upj8HUgoz2_vV20VqfrIA%22%2C%22connectid%22%3A%22oeKxkhudcRIH1JGQU89QAeGsL2gdU5Xb0brF1uzzfMC7Po4eke4b8zy7Vo57zzm_7upj8HUgoz2_vV20VqfrIA%22%2C%22connectId%22%3A%22oeKxkhudcRIH1JGQU89QAeGsL2gdU5Xb0brF1uzzfMC7Po4eke4b8zy7Vo57zzm_7upj8HUgoz2_vV20VqfrIA%22%2C%22ttl%22%3A24%2C%22he%22%3A%223747aeec137077e8949b9106c897b52bebfe6cbacc3e6f20fca21b31c2cb0798%22%2C%22lastSynced%22%3A1706747880678%2C%22lastUsed%22%3A1706747958869%7D; _pubcid_cst=zix7LPQsHA%3D%3D; _iidt=oFp1Ez3HnYUUfaRrcbg9ZeCIgP6jL0j2oY/XWMLvG9Np5djPjjbI2Uf1ZcQfgDnejdcLARfwd2Qc1q3nAc0Bfy0c5WGSb3Hl3cDIigA=; _vid_t=WukSkYm3dxlfFVb5wbcCr1HQhHFPpa9Mm5PgnF76UqsuN65cEnr8+2NKB18MeVYJ6Oc19YUvxnDVYC6SEVuO0ZTCKGjoQ8luH8XXLZw=; DFID=web|GGdhSIsSLWqVmnYy2bGb; _gid=GA1.2.1461184429.1707113641; _ga_ZBG6WLWXBE=GS1.2.1707199933.15.1.1707199951.42.0.0; hwh_order_ref=/homework-help/questions-and-answers/subject-electrical-engineering-1-divide-complete-operational-amplifier-circuit-figure-1-3--q133519292; panoramaId_expiry=1707286348190; panoramaId=5c783d417c0a180ee036f0f05d64a9fb927a3d78c71421d38c2ae725341a553b; panoramaIdType=panoDevice; forterToken=d15c3d20dcd24d5b9db82d98633992a5_1707199987937__UDF43-m4_13ck_; _cs_id=80b069bc-d9fd-abb8-e6cd-c5ecbcd80e40.1704018264.19.1707199994.1707199934.1.1738182264039.1; U=7b8b943f05859e3d6e8e8c4238e0611f; SU=gbVyPIkCbofs6kuAuOC1ucTMUmmkMaTeqlmPxAXphKEwXco5LEZsI7EyebV28HqXWkpRvqidwfG80-9NwqPaeudpRlgO89IjTLodq00EfqbSawrSbsFsccfX2DFNy4Hr; refreshToken=ext.a0.t00.v1.M-r3Rp5XsV_k9i6eJIwwILiLDXqnpKOiVF-bnYaZpEa-jipCfCz2PQHHKodpOhftDGBf1TsRmlZyM52TukO-6d8; refresh_token=ext.a0.t00.v1.M-r3Rp5XsV_k9i6eJIwwILiLDXqnpKOiVF-bnYaZpEa-jipCfCz2PQHHKodpOhftDGBf1TsRmlZyM52TukO-6d8; id_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImplbnU2NjMyN0BnbWFpbC5jb20iLCJpc3MiOiJodWIuY2hlZ2cuY29tIiwiYXVkIjoiQ0hHRyIsImlhdCI6MTcwNzIxNDc1NywiZXhwIjoxNzIyNzY2NzU3LCJzdWIiOiI2NjQ5MjUzZi1mZWE2LTQ2ZDgtODI1OS04M2M0NTkxMzg5ZGUiLCJyZXBhY2tlcl9pZCI6ImFwdyIsImN0eXAiOiJpZCIsImlkc2ciOiJwYXNzd29yZGxlc3MiLCJpZHN0IjoxNzA3MTk5OTUwMDE4LCJpZHNpZCI6ImJiYTI3YTA3In0.PrqTNDpbGWJOxwkYgY4LQ8Ac-dZCiOItIpqZWm7MhLpwCFxaTncHoUTHAE6W1GQI00xfNVI1tcw10b_U6VdJiCZWLAA3_ecYbNpy3cXOEsCxHDoUqLkPxgrvCh33cfhFmdW69CKTdXEy50IdwGgzm_4JHFkv_HUCrpImMCLIaSHeyX0zfT5JQDOF2ZkhOCYS0F-rvxJI3xvfC1QNpR48AXUKOCTG8AfDkcL16TY8F-Ax1o9NCVVDbR-QeZEU4xqlc5FluN6vbfTs6El6JHXBaT8tEY-I7a-UOnrVPUr3trKCRJ_W-zUu8wn3ZRuRFaFXF4wtbmK76N8QOlNX2w06OA; _au_last_seen_pixels=eyJhcG4iOjE3MDcyNDEzMTMsInR0ZCI6MTcwNzI0MTMxMywicHViIjoxNzA3MjQxMzEzLCJydWIiOjE3MDcyNDEzMTMsInRhcGFkIjoxNzA3MjQxMzEzLCJhZHgiOjE3MDcyNDEzMTMsImdvbyI6MTcwNzI0MTMxMywic29uIjoxNzA3MjQxMzEzLCJwcG50IjoxNzA3MjQxMzEzLCJpbXByIjoxNzA3MTk5ODc3LCJ0YWJvb2xhIjoxNzA3MjQxNDIxLCJpbmRleCI6MTcwNzI0MTMxMywic21hcnQiOjE3MDcyNDE0MjEsIm9wZW54IjoxNzA3MjQxNDIxLCJiZWVzIjoxNzA3MjQxNDIxLCJjb2xvc3N1cyI6MTcwNzI0MTQyMSwidW5ydWx5IjoxNzA3MjQxNDIxLCJhZG8iOjE3MDcyNDE0MjEsImFtbyI6MTcwNzI0MTQyMX0%3D; country_code=IN; CSID=1707247983875; local_fallback_mcid=37455296287057007747333274680221633580; s_ecid=MCMID|37455296287057007747333274680221633580; pxcts=91bac4ec-c526-11ee-8ab4-fe0bd335cddf; ab.storage.deviceId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%2274b544bf-6039-bd7a-74d6-dec0b6d85d44%22%2C%22c%22%3A1704018430388%2C%22l%22%3A1707248056439%7D; ab.storage.userId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%226649253f-fea6-46d8-8259-83c4591389de%22%2C%22c%22%3A1704018430380%2C%22l%22%3A1707248056441%7D; CSessionID=d67db99f-cb30-4b30-b2d7-c9d0af9ad98b; IR_gbd=chegg.com; __gads=ID=4d5d123c9ab81947:T=1704018241:RT=1707248966:S=ALNI_MYVEEuUSXWaRDf6Jt2Dlq4XbBwMBA; __gpi=UID=00000cccc859f52f:T=1704018241:RT=1707248966:S=ALNI_Mb00RX1N9vwe58zEAd2cwQd-239sA; __eoi=ID=e474624cf7a33200:T=1706645420:RT=1707248966:S=AA-AfjYSR2eywTIuL50b2x1gTP8_; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Feb+07+2024+01%3A23%3A53+GMT%2B0530+(India+Standard+Time)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=7aecc2c7-f78b-4f0e-a400-23e5b82248ea&interactionCount=1&landingPath=NotLandingPage&groups=fnc%3A1%2Csnc%3A1%2Ctrg%3A1%2Cprf%3A1&AwaitingReconsent=false; ab.storage.sessionId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%227a6867a0-a165-6dce-df97-fa095fd96042%22%2C%22e%22%3A1707251043223%2C%22c%22%3A1707248056437%2C%22l%22%3A1707249243223%7D; _scid_r=ea51a8cd-0351-4d98-8391-ed50891f3273; _uetsid=c07786f0c3ed11ee8ad2b9f15ca54bdc; _uetvid=c52cdae0a7c611eeb8bfa757fe6f2469; _rdt_uuid=1704018442371.2819f98a-e1d1-49c7-a695-340fb7807203; IR_14422=1707249244843%7C0%7C1707248073479%7C%7C; _px3=278225ef86fe20aca260d49dacff62a01935a63489c59f2ca198c504ee7956a2:0GuROhR2gvT1g/QUrIJNGjZJaypsDAbwR9NGDMxeuDJf2UITYl8HgmQ45aFleIP03ogA4A6pCsC74HWs56SeEw==:1000:EFNdoRVaWDA18JP8nAIql5UApV858GLzeIOWjKKLQNtfQCFaMfHJo5Mv3eo1RKx1cQbpI/2bEJvHSLCy8LrI8WIV9GXCTI+N/SIEp/HAruCzouk0OKjwsHG3GWI6hD6zTBi6uLvH+oizpp5mi4DKVBUnvu50vJ6yVRiawdx7v4kGB9ABEEUA0DOfc77MAGkfW7b4RcX7VwUdQRrBCJ1oHDY0Tw9oYhpOkfzeEr8DQIw=; _px=0GuROhR2gvT1g/QUrIJNGjZJaypsDAbwR9NGDMxeuDJf2UITYl8HgmQ45aFleIP03ogA4A6pCsC74HWs56SeEw==:1000:oax8G1tZwo08+fc6PmzeAX85UWxvHzGD5HXBkCwk2O9CcMAD1PJvWYnTrS6N+BOQwUEd70ZMuUESMS4IIk4Hl+Sm0hx+xlVyILVmVDAK371RyBvqiBv8kYF9iPXfJwMWSY2+ht2nYVT8H5i3bRyttlD5PMpHE2v/6cMMS4idwfiw+NNphZrm/8mIumfPyNsnFAgT7U4ykNS6+9jmxzEj7WidV/sGdEzLFsiv/POK9ybFHjNy61TWXO2bQyg9B9tHe3082vyHvpUz/66pRtTmCw==; _pxde=e723f9298c28847658024968ff01a0620c4366bb9ce1c62748dc8a01e48d7d55:eyJ0aW1lc3RhbXAiOjE3MDcyNDk0Nzk1OTd9',
              'origin': 'https://www.chegg.com',
              'referer': 'https://www.chegg.com/',
              'sec-ch-ua':
              '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
              'sec-ch-ua-mobile': '?0',
              'sec-ch-ua-platform': '"Windows"',
              'sec-fetch-dest': 'empty',
              'sec-fetch-mode': 'cors',
              'sec-fetch-site': 'same-site',
              'user-agent': Cookies_list.get_user_agent(),
              'x-chegg-referrer':
              'homework-help/questions-and-answers/use-lrfd-design-bottom-chord-shown-roof-truss-use-double-angle-shapes-throughout-bottom-ch-q52065341',
              'x-chegg-sqnapreviewlenexpvariant': 'MEDIUM',
          }
          question = process_question(qid, headers)

          if question != 'QUESTION_FETCH_FAILED':
            #FINDING THE ANSWER TYPE
            #answer_type_available = identify_answer_type(qid,headers)

            #if answer_type_available == 'ANSWER_TYPE_FAILED':

            #	bot.send_message(chat_id, 'Please send your link again after a minute\n\nYour remaining chances are: '+str(chances+1))
            #	UserData.add_lost_chance(chat_id)
            #	bot.send_message(adminID, "Could not find the answer type\nhttps://www.chegg.com/homework-help/questions-and-answers/-q"+str(qid))

            #elif answer_type_available != None:

            #	answer_type = answer_type_available['__typename']

            #SEND ANSWER USING SUSPEDNED
            #ACCOUNT IF IT IS SQNA
            #	if answer_type == 'SqnaAnswers':

            print(question)
            fetch_answer(chat_id, link, chances, question, headers)
            '''print('[*] Sqna detected')
                Cookies_list.get_suspended_cookies()

                ans_data = {
                  'operationName': 'QnaPageAnswer',
                  'variables': {
                    'id': int(qid),
                  },
                  'extensions': {
                    'persistedQuery': {
                      'version': 1,
                      'sha256Hash': '1c2246681ad020e019aaf2e2393e104c5db65ec57aa04a12fe563cf05fe7097f',
                    },
                  },
                }

                lis = list(headers.items())
                random.shuffle(lis)
                headers = dict(lis)

                response = requests.post('https://gateway.chegg.com/one-graph/graphql', cookies=SUS_COOKIE, headers=headers, json=ans_data)
                jfile = json.loads(response.content)

                try:
                  try:
                    try:
                      sus_error = jfile['errors'][0]['extensions']['metadata']['accessRestrictions']
                    except:
                      sus_error = jfile['errors'][0]['message']
                  except:
                    sus_error = []

                except:
                  pass


                if len(sus_error) > 0:

                  UserData.add_lost_chance(chat_id)
                  bot.send_message(adminID, "❌\nSQNA FAILED!!!!")
                  bot.send_message(chat_id, "! Ongoing Maintainence!\n\nThis type of answer is not working for some hours, it will be fixed in some time ")

                else:
                  pass

                process_sqna(jfile,SUS_COOKIE,headers,question,webhook_script,completeName)
                doc = open(completeName, 'rb')
                bot.send_document(chat_id, doc, caption ="*"+str(chances)+" chances remaining*\n\n *👆🏼Open above file in chrome browser to see answer👆🏼*\n\n 🎁We have *Gifted you free bot* 🎁\n\nClick here *@FREEPORTSUPERBOT* to open Your gift bot, and see yourself the use of it🤫. \n\nContact *@The_Admin_Freeport* for any queires",parse_mode='Markdown',reply_markup=gen_Main_menu())
                bot.send_message(adminID, str(chat_id)+" SQNA "+str(chances)+' '+str(qid))
                print("[*] SQNA Successfully delivered using suspended account\n_____________________________")
                count = open('sqna_count.txt').read()
                coun = int(count)
                coun += 1
                with open('sqna_count.txt', 'w') as f:
                  f.write(str(coun))/'''

            #process_sqna(jfile,SUS_COOKIE,headers,question,webhook_script,completeName)
            #doc = open(completeName, 'rb')
            #bot.send_document(chat_id, doc, caption ="*"+str(chances)+" chances remaining*\n\n *open above file to see answer*\n\n *Use @freeportsuperbot for other sites like,\n\n🔅Transtutors\n🔅Study. com\n🔅Bartleby\n🔅Numerade\n🔅Solutioninn\n\nContact @The_Admin_Freeport for queries*",parse_mode='Markdown',reply_markup=gen_Main_menu())
            #bot.send_message(adminID, str(chat_id)+" SQNA "+str(chances)+' '+str(qid))
            #print("[*] SQNA Successfully delivered using suspended account\n_____________________________")


#CALL THE FUNCTION FOR
#FETCHING HTML OR EC ANSWER
#USING NORMAL ACCOUNT
#else:
#	fetch_answer(chat_id,link,chances,question,headers)

#elif answer_type_available == None:
#	bot.send_message(chat_id, 'The question has not been solved on chegg\n\nYour remaining chances are : '+str(chances+1))
#	UserData.add_lost_chance(chat_id)
#	bot.send_message(adminID, "Unsolved link or error in account\nhttps://www.chegg.com/homework-help/questions-and-answers/-q"+str(qid))

#else:
#	pass
          else:
            bot.send_message(
                chat_id,
                'Please send your link again after a minute\n\nYour remaining chances are : '
                + str(chances + 1))
            UserData.add_lost_chance(chat_id)
            bot.send_message(
              adminID,
                "Could not find the question\nhttps://www.chegg.com/homework-help/questions-and-answers/-q"
                + str(qid))

      else:
        filenam = link.split('homework-help/')[1]
        filename = filenam.split('?')[0]
        try:
          work = True
          save_path = 'tbs'
          name = filename + '.html'
          completeName = os.path.join(save_path, name)

          doc = open(completeName, 'rb')

          bot.send_document(
              chat_id,
              doc,
              caption="*" + str(chances) +
              " chances remaining*\n\n *open above file to see answer*\n\n *Use @freeportsuperbot for other sites like,\n\n🔅Transtutors\n🔅Study. com\n🔅Bartleby\n🔅Numerade\n🔅Solutioninn\n\nContact @The_Admin_Freeport for queries*",
              parse_mode='Markdown',
              reply_markup=gen_Main_menu())
          bot.send_message(
            adminID,
              str(chat_id) + " " + filename + '.html received ' + str(chances))
          print('[*] Answer sent from DB\n_____________________________')
        except:
          bot.send_message(
              chat_id, 'Textbook solutions is not available for some days')
          UserData.add_lost_chance(chat_id)
          #bot.send_message(adminID, str(message.chat.id)+"\n"+str(message.chat.first_name)+"\n"+str(message.chat.username)+"\nProcessing")

          print('\nXXXXXXXXXXXXXXX TBS FAILED XXXXXXXXXXXXXX\n')
    else:
      print("[*] User has 0 credits\n_____________________________")
      bot.send_message(
          chat_id,
          "Top up your cookies 🍪 To get more answers\n\n50Rs = 20 soltuions\n100Rs = 45 solutions\n200Rs = 100 solutions\n500Rs = 280 solutions\n1000Rs = 600 solutions\n\n\nUse chegg2rs@sbi or https://paytm.me/b-cK4qV for payment! \n\nUse any apps listed here using the upi id:-\n\n💲Google Pay\n💲Phonepe\n💲PayTM\n💲AmazonPay\n\n👉🏽UPI ID = chegg2rs@sbi\n\n\nFOR INTERNATIONAL PAYMENTS:\n2$ = 30 Solutions\n5$ = 100 Solutions\n10$ = 250 solutions \n\n👉🏽Paypal: paypal.me/Karanmodi003\n\nAFTER PAYMENT SEND THE DETAILED SCREENSHOT WITH IN 5 MINUTES TO THE ADMIN OF BOT @The_admin_freeport\n\n🚫WE DO NOT RECEIVE PAYMENTS LESS THAN 50Rs"
      )

  except Exception as e:
    print(e)


@bot.message_handler(commands=['plan'])
def send_plan(message):
  bot.send_message(message.chat.id,
                   "*Click on the button to see more details*",
                   parse_mode='Markdown',
                   reply_markup=gen_plan())
  #bot.reply_to(message, "🔅Plans for Cheggbot🔅\n\n30Rs = 15 solutions(2Rs/question)\n60Rs = 35 solutions(1.7Rrs/question\n100Rs = 60 solutions(1.66Rs/question)\n200Rs = 125 solutions(1.60Rs/question)\n500Rs = 320 solutions(1.56Rs/question)\n\n\nUse chegg2rs@sbi or paytm.me/kZoQ-bz for payment! \n\nUse any apps listed here using the upi id:-\n\n💲Google Pay\n💲Phonepe\n💲PayTM\n💲AmazonPay\n\n👉🏽UPI ID = chegg2rs@sbi\n\n\nFOR INTERNATIONAL PAYMENTS:\n1$ = 20 Solutions\n2$ = 42 Solutions\n3$ = 85 Sutions\n5$ = 160 Solutions\n10$ = 330 Solutions\n\n👉🏽Paypal: paypal.me/Karanmodi003\n\nAFTER PAYMENT SEND THE DETAILED SCREENSHOT TO THE ADMIN OF BOT @cheggbotadmin\n\n🚫WE DO NOT RECEIVE PAYMENTS LESS THAN 30Rs")


@bot.message_handler(commands=['how'])
def send_helptouse(message):
  bot.reply_to(
      message,
      "🏁PROCESS FOR GETTING ANSWER FROM BOT.\n\nSTEP 1 ➡️  Type the exact question on google. I dont recommend using google lens as it is not accurate .\n\nSTEP 2 ➡️  Verify whether the question is same in chegg.com and it has been solved by an expert .\n\nSTEP 3 ➡️  Now, copy the exact link and paste it on the @chegg1rsbot .\n\nSTEP 4 ➡️  Please avoid sending additional texts just before the chegg link you send to bot. This happens automatically when you share the link from chrome mobile browser. To prevent auto generating such additional links, just copy the link from browser and paste in bot.\n\nThank you!"
  )


@bot.message_handler(commands=['start'])
def send_welcome(message):
  try:
    bot.delete_message(message.chat.id, bot.last_message_sent[message.chat.id])
  except Exception as e:
    print(e)
  #bot.send_message(message.chat.id, "Payment info:\n\nThe initial payment for an Indian can pay is 30 rupees\n\nFOR INDIANS:\n\n30 Rs = 15 solutions(2rs per question)\n60rs = 35 solutions(1.71rs per question\n100rs = 60 solutions(1.66rs per question)\n200rs = 125 solutions(1.60rs per question)\n500rs = 320 solutions(1.56rs per question)\n\n\nUse chegg2rs@sbi or paytm.me/kZoQ-bz for payment! \n\nUse any apps listed here using the upi id:-\n\nUPI ID = chegg2rs@sbi\n\n\nGoogle Pay\nPhonepe\nPayTM to pay via UPI\n\n\nFOR INTERNATIONAL PEOPLE:\n  1$ = 20 solutions\n  2$ = 42 solutions\n  3$ = 85 solutions\n 5$ = 160 solutions\n 10$ = 330 solutions\n\n\nUse Paypal: paypal.me/Karanmodi003\n\n\ncontact https://t.me/Cheggbotadmin for any queries!\n\n\nRULES TO FOLLOW:\n\n1. MAKE THE PAYMENT AND SEND DETAILED SCREENSHOT TO THE ADMIN (@CHEGGBOTADMIN)\n2. SEND THE LINK AND WAIT TILL THE ARRIVAL OF ANSWER BEFORE YOU SEND NEXT QUESTION!\n\n\n\nHAPPY CHEGGING!")
  bot.send_message(
      message.chat.id,
      "*✨✨Welcome to Cheggbot✨✨\n\nWe provide solved solutions of chegg less than 2Rs!*",
      parse_mode='Markdown')
  msg = bot.send_message(message.chat.id,
                         'Choose the below buttons to interact with bot',
                         reply_markup=gen_start())
  bot.last_message_sent[message.chat.id] = msg.message_id


@bot.message_handler(commands=['menu'])
def send_welcome(message):
  try:
    bot.delete_message(message.chat.id, bot.last_message_sent[message.chat.id])
  except Exception as e:
    print(e)
  bot.send_message(message.chat.id,
                   'Choose the below buttons to interact with bot',
                   reply_markup=gen_Main_menu())


@bot.message_handler(commands=['myid'])
def send_code(message):
  bot.send_message(message.chat.id, str(message.chat.id))


@bot.message_handler(commands=['buy'])
def send_buy(message):
  doc = open("qr.jpg", 'rb')
  bot.send_photo(
      call.from_user.id,
      doc,
      caption=
      '<b>Plans for Indians are as follow</b>\n\n30Rs = 15 solutions(2Rs/question)\n60Rs = 35 solutions(1.7Rrs/question\n100Rs = 60 solutions(1.66Rs/question)\n200Rs = 125 solutions(1.60Rs/question)\n500Rs = 320 solutions(1.56Rs/question)\n\n🔅UPI ID : chegg2rs@sbi\n🔅PayTM link : paytm.me/kZoQ-bz\n\nSend the <b>payment screenshot</b> to @The_admin_freeport </b>within 5 minutes </b>after transaction',
      parse_mode='html',
      reply_markup=gen_Main_menu())


@bot.message_handler(commands=['reset'])
def send_code(message):

  sqna_count = int(open('sqna_count.txt').read())
  db_count = int(open('databasecount.txt').read())
  html_count = int(open('numberoflinkperday.txt').read())

  bot.send_message(
      message.chat.id,
      f'''<b>SQNA : {sqna_count}\nDB : {db_count}\nHTML : {html_count}\n\nTOTAL : {html_count+db_count+sqna_count}</b>''',
      parse_mode='html')

  with open('numberoflinkperday.txt', 'r+') as r:
    r.truncate(0)
    r.write(str(0))
    r.close()
  with open('databasecount.txt', 'r+') as r:
    r.truncate(0)
    r.write(str(0))
    r.close()
  with open('sqna_count.txt', 'r+') as r:
    r.truncate(0)
    r.write(str(0))
    r.close()


@bot.message_handler(commands=['record'])
def send_count(message):

  sqna_count = int(open('sqna_count.txt').read())
  db_count = int(open('databasecount.txt').read())
  html_count = int(open('numberoflinkperday.txt').read())

  bot.send_message(
      message.chat.id,
      f'''<b>SQNA : {sqna_count}\nDB : {db_count}\nHTML : {html_count}\n\nTOTAL : {html_count+db_count+sqna_count}</b>''',
      parse_mode='html')


@bot.message_handler(commands=['get'])
def saheb_add_user(message):
  try:
    if message.chat.id == adminID:

      saheb_client_id = message.text.split(' ')[1]
      saheb_client = collection.find_one({'_id': str(saheb_client_id)})
      saheb_client_points = int(saheb_client['credit'])
      try:
        update = {"$set": {'credit': 0}}
        collection.update_one({'_id': saheb_client_id}, update)

        update = {"$inc": {'credit': saheb_client_points}}
        collection.update_one({'_id': str(message.chat.id)}, update)
        bot.send_message(
            message.chat.id,
            f'{str(saheb_client_points/2)} credits has been grabbed back !')
      except:
        bot.send_message(message.chat.id, 'This user does not exist')
    else:
      bot.send_message(message.chat.id,
                       'This command require Admin privileges')

  except Exception as e:
    bot.send_message(adminID, e)


@bot.message_handler(commands=['give'])
def saheb_add_user(message):
  try:
    if message.chat.id == adminID:
      #message = '/give 100000000 100'

      user_chat_id = message.text.split(' ')[1]
      point = int(message.text.split(' ')[2])
      points = point * 2
      saheb = message.chat.id

      user = collection.find_one({'_id': str(saheb)})

      total_credits = int(user['credit']) / 2

      if total_credits > 0:

        if point <= total_credits:

          try:
            data = {'_id': user_chat_id, 'credit': points}
            collection.insert_one(data)

            saheb_remaining_credit = int(total_credits - point)
            new_credit_saheb = saheb_remaining_credit * 2
            update_saheb_credits = {"$set": {'credit': new_credit_saheb}}
            collection.update_one({'_id': str(message.chat.id)},
                                  update_saheb_credits)
            bot.send_message(
                message.chat.id,
                f'Successful!\n\nRemianing : {str(saheb_remaining_credit)}')
            bot.send_message(
                user_chat_id,
                f'You received {str(point)} credits to use the bot')

            with open('saheb_users_list.json', 'r') as f:
              data = json.load(f)
              f.close()

            data[user_chat_id] = 'user'

            with open('saheb_users_list.json', 'w') as f:
              json.dump(data, f)
              f.close()

          except:
            update = {"$inc": {'credit': points}}
            collection.update_one({'_id': user_chat_id}, update)

            saheb_remaining_credit = int(total_credits - point)
            new_credit_saheb = saheb_remaining_credit * 2
            update_saheb_credits = {"$set": {'credit': new_credit_saheb}}
            collection.update_one({'_id': str(message.chat.id)},
                                  update_saheb_credits)
            bot.send_message(
                message.chat.id,
                f'Successful!\n\nRemianing : {str(saheb_remaining_credit)}')
            bot.send_message(
                user_chat_id,
                f'You received {str(point)} credits to use the bot')

            with open('saheb_users_list.json', 'r') as f:
              data = json.load(f)
              f.close()

            data[user_chat_id] = 'user'

            with open('saheb_users_list.json', 'w') as f:
              json.dump(data, f)
              f.close()

        else:
          bot.send_message(
              message.chat.id,
              f'Sorry, You have only {str(total_credits)} credits to distribute'
          )
      else:
        bot.send_message(message.chat.id,
                         f'Sorry, You ran out of credits, Kindly buy again')
  except Exception as e:
    print(e)


#ADD USER


@bot.message_handler(commands=['add'])
def add_user(message):

  if message.chat.id == adminID:
    bot.send_message(message.chat.id, "DO IT")

    @bot.message_handler(content_types=["text"])
    def send_welcome(message):
      if message.chat.id == adminID:
        add_user = message.text.split(" ")
        PRICE = int(add_user[-1])
        PRICE = int(add_user[-1])
        ID = add_user[0]
        chncs = int(PRICE) / 2
        c = int(chncs)

        try:
          data = {'_id': str(ID), 'credit': PRICE}
          collection.insert_one(data)
          print('inserted')
        except:
          update = {"$set": {'credit': PRICE}}
          collection.update_one({'_id': str(ID)}, update)

        bot.send_message(message.chat.id, "User added")
        bot.send_message(
            ID,
            "Hellow i'm Cheggbot!\n\nThanks for subscribing to me.\nNow you can send your chegg qna links here..\n\nYour remaining chances are "
            + str(c))
      else:
        bot.send_message(
            message.chat.id,
            "Kindly send chegg question link\n\nif still not working, make sure you have joined our channel @cheggnx and send the link again!"
        )
  else:
    bot.send_message(
        message.chat.id,
        "Kindly send chegg question link\n\nif still not working, make sure you have joined our channel @cheggnx and send the link again!"
    )


@bot.message_handler(commands=['count'])
def send_count(message):
  count = collection.count_documents({})
  bot.send_message(adminID, "No.of paid users :" + count)


@bot.message_handler(commands=['account'])
def send_help(message):
  chatt_id = str(message.chat.id)
  user = collection.find_one({'_id': chatt_id})

  if user != None:
    chances_remaining = user['credit']
    chances1 = int(chances_remaining / 2)
    bot.send_message(message.chat.id,
                     "Account Balance:\n\nChances Remaining: " + str(chances1))
  else:
    bot.send_message(message.chat.id, "Sorry you are not in our database")


@bot.message_handler(commands=['help'])
def send_help(message):
  bot.reply_to(
      message,
      "OMG, you seems lost. Please ask your doubt to The Admin \nhttps://t.me/spacenx1"
  )
  print(
      str(message.chat.id) + "::" + str(message.chat.first_name) + "::" +
      str(message.chat.username))


@bot.message_handler(commands=['delete'])
def send_help(message):
  try:
    link = message.text.split(' ')[1]
    filenam = link.rsplit('-q', 1)[1]
    print(filenam)
    filename = filenam.split('?')[0]
    print(filename)
    save_path = 'qna'
    name = filename + '.html'
    completeName = os.path.join(save_path, name)
    os.remove(completeName)
  except Exception as e:
    print(e)


linkcount = 0


@bot.message_handler(func=lambda msg: msg.text is not None and
                     'https://www.chegg.com' and 'homework-help/' in msg.text)
def send_nothing(message):
  if message.forward_date == None:
    x = message.text.startswith("https://www.chegg.com/homework-help/")
    CHAT_ID = -1001726731881
    result = bot.get_chat_member(CHAT_ID, message.chat.id)

    if x == True:
      if result.status == 'member' or result.status == 'creator' or result.status == 'administrator':

        user = collection.find_one({'_id': str(message.chat.id)})

        if user != None:
          bot.send_message(message.chat.id, '🔅 Hold on, sending your answer')
          save_data(message, user)
        else:
          bot.send_message(
              message.chat.id,
              '😃 Hey new user 😃\n\nHold on, i am sending you this answer for free🎁'
          )
          add_person = {"_id": str(message.chat.id), "credit": 2}
          collection.insert_one(add_person)
          user = collection.find_one({'_id': str(message.chat.id)})
          save_data(message, user)

      else:
        bot.send_message(
            message.chat.id,
            "*You have to be a member of our channel to get answers from me.*",
            parse_mode='Markdown',
            reply_markup=join_channel())

    else:
      bot.reply_to(
          message,
          'Please send the pure chegg link which starts with\n👉🏽https://www.chegg.com/homework-help'
      )
  else:
    bot.send_message(message.chat.id, "Bot do not accept forwarded messages!")


def fetch_answer(chat_id, link, chances, question, headers):

  try:
    print('\n[*] Collecting Answer from site\n')
    try:

      global linkcount
      linkcount += 1
      if linkcount >= 5:
        linkcount = 0
        Account.switch()
        bot.send_message(
            adminID,
            "5 links from " + SUScookies + "\nNow using " + NXTcookies + ".")
      else:
        pass
      QNA = '/questions-and-answers/'

      if search(QNA, link):

        filenam = link.rsplit('-q', 1)[1]
        filename = filenam.split('?')[0]

        try:
          cookies = Cookies_list.get_cookies()[0]
          cookiename = Cookies_list.get_cookies()[1]
          print('cookie selected')
        except:
          print('All accounts suspended')
          UserData.add_lost_chance(chat_id)
          bot.send_message(
              chat_id,
              "Unable to fetch the solution! Let the admin know and kindly wait. Sorry"
          )
          bot.send_message(
              adminID,
              "All accounts suspended or ERROR in the name of accs added")

        try:
          save_path = 'qna'
          name = filename + '.html'
          completeName = os.path.join(save_path, name)

          qid = link.split('-q')[-1].split('?')[0].split('#')[0].split('/')[0]

          #_______________________________________  A N S W E R   _______________________________________________

          ans_data = {
              'operationName': 'QnaPageAnswerSub',
              'variables': {
                  'id': int(qid),
              },
              'extensions': {
                  'persistedQuery': {
                      'version':
                      1,
                      'sha256Hash':
                      'f820ff6ecd2a845d20524d72e1a9a06dee761c219c39f5d7f031d09b7823afe8',
                  },
              },
          }

          response = requests.post(
              'https://gateway.chegg.com/one-graph/graphql',
              cookies=cookies,
              headers=headers,
              json=ans_data)
          jfile = json.loads(response.content)
          print(response.content)

          content = jfile['data']['questionByLegacyId']['displayAnswers']

          try:
            try:
              try:
                sus_error = jfile['errors'][0]['extensions']['metadata'][
                    'accessRestrictions']
              except:
                sus_error = []

            except:
              pass

            if len(sus_error) > 0:
              Account.delete()
              UserData.add_lost_chance(chat_id)
              bot.send_message(
                  adminID, "❌❌❌❌❌❌❌❌❌❌❌❌\n" + suscookies +
                  " SUSPENDED!\nUsing " + nxtcookies + " now..")
              count = open('numberoflinkperday.txt').read()
              coun = int(count)
              coun = 0
              with open('numberoflinkperday.txt', 'w') as f:
                f.write(str(coun))
              bot.send_message(
                  chat_id,
                  "Something went wrong :(\n\n1.Send the link after sometimes\n2.Check if the link is answered"
              )

            elif content == None:
              bot.send_message(
                  chat_id,
                  'The question has not been solved on chegg\n\nYour remaining chances are : '
                  + str(chances + 1))
              UserData.add_lost_chance(chat_id)
              bot.send_message(
                  adminID,
                  "Unsolved link or error in account\nhttps://www.chegg.com/homework-help/questions-and-answers/-q"
                  + str(qid))

            elif 'ecAnswers' in content:

              process_ec(jfile, cookies, headers, question, webhook_script,
                         completeName)
              doc = open(completeName, 'rb')
              bot.send_document(
                  chat_id,
                  doc,
                  caption="*" + str(chances) +
                  " chances remaining*\n\n *👆🏼Open above file in chrome browser to see answer👆🏼*\n\n 🎁We have *Gifted you free bot* 🎁\n\nClick here *@FREEPORTSUPERBOT* to open Your gift bot, and see yourself the use of it🤫. \n\nContact *@The_Admin_Freeport* for any queires",
                  parse_mode='Markdown',
                  reply_markup=gen_Main_menu())
              Account.using()
              count = open('numberoflinkperday.txt').read()
              coun = int(count)
              coun += 1
              with open('numberoflinkperday.txt', 'w') as f:
                f.write(str(coun))
              bot.send_message(
                  adminID,
                  str(chat_id) + " EC " + str(chances) + ' ' +
                  str(usingcookies) + ' no.of links =' + str(coun) + ' ' +
                  str(qid))
              print(
                  "[*} Successfully delivered\n_____________________________")

            elif 'htmlAnswers' in content:

              process_html(jfile, cookies, headers, question, webhook_script,
                           completeName)
              doc = open(completeName, 'rb')
              bot.send_document(
                  chat_id,
                  doc,
                  caption="*" + str(chances) +
                  " chances remaining*\n\n *👆🏼Open above file in chrome browser to see answer👆🏼*\n\n 🎁We have *Gifted you free bot* 🎁\n\nClick here *@FREEPORTSUPERBOT* to open Your gift bot, and see yourself the use of it🤫. \n\nContact *@The_Admin_Freeport* for any queires",
                  parse_mode='Markdown',
                  reply_markup=gen_Main_menu())

              Account.using()
              count = open('numberoflinkperday.txt').read()
              coun = int(count)
              coun += 1
              with open('numberoflinkperday.txt', 'w') as f:
                f.write(str(coun))
              bot.send_message(
                  adminID,
                  str(chat_id) + " HTML " + str(chances) + ' ' +
                  str(usingcookies) + ' no.of links=' + str(coun) + ' ' +
                  str(qid))
              print(
                  "[*] Successfully delivered\n_____________________________")

            elif 'sqnaAnswers' in content:

              process_sqna(jfile, cookies, headers, question, webhook_script,
                           completeName)

              doc = open(completeName, 'rb')
              bot.send_document(
                  chat_id,
                  doc,
                  caption="*" + str(chances) +
                  " chances remaining*\n\n *👆🏼Open above file in chrome browser to see answer👆🏼*\n\n 🎁We have *Gifted you free bot* 🎁\n\nClick here *@FREEPORTSUPERBOT* to open Your gift bot, and see yourself the use of it🤫. \n\nContact *@The_Admin_Freeport* for any queires",
                  parse_mode='Markdown',
                  reply_markup=gen_Main_menu())
              Account.using()
              count = open('sqna_count.txt').read()
              coun = int(count)
              coun += 1
              with open('sqna_count.txt', 'w') as f:
                f.write(str(coun))
              bot.send_message(
                  adminID,
                  str(chat_id) + " SQNA " + str(chances) + ' ' + str(qid))
              print(
                  "[*] Successfully delivered\n_____________________________")

            elif content['__typename'] == 'SBSAnswer':

              process_ai_sbs(jfile, cookies, headers, question, webhook_script,
                             completeName)

              doc = open(completeName, 'rb')
              bot.send_document(
                  chat_id,
                  doc,
                  caption="*" + str(chances) +
                  " chances remaining*\n\n *👆🏼Open above file in chrome browser to see answer👆🏼*\n\n 🎁We have *Gifted you free bot* 🎁\n\nClick here *@FREEPORTSUPERBOT* to open Your gift bot, and see yourself the use of it🤫. \n\nContact *@The_Admin_Freeport* for any queires",
                  parse_mode='Markdown',
                  reply_markup=gen_Main_menu())
              Account.using()
              count = open('sbs_count.txt').read()
              coun = int(count)
              coun += 1
              with open('sbs_count.txt', 'w') as f:
                f.write(str(coun))
              bot.send_message(
                  adminID,
                  str(chat_id) + " SBS " + str(chances) + ' ' + str(qid))
              print(
                  "[*] Successfully delivered\n_____________________________")

            elif content['__typename'] == 'TextAnswer':

              process_ai_TextAnswer(jfile, cookies, headers, question,
                                    webhook_script, completeName)

              doc = open(completeName, 'rb')
              bot.send_document(
                  chat_id,
                  doc,
                  caption="*" + str(chances) +
                  " chances remaining*\n\n *👆🏼Open above file in chrome browser to see answer👆🏼*\n\n 🎁We have *Gifted you free bot* 🎁\n\nClick here *@FREEPORTSUPERBOT* to open Your gift bot, and see yourself the use of it🤫. \n\nContact *@The_Admin_Freeport* for any queires",
                  parse_mode='Markdown',
                  reply_markup=gen_Main_menu())
              Account.using()
              count = open('sbs_count.txt').read()
              coun = int(count)
              coun += 1
              with open('sbs_count.txt', 'w') as f:
                f.write(str(coun))
              bot.send_message(
                  adminID,
                  str(chat_id) + " SBS " + str(chances) + ' ' + str(qid))
              print(
                  "[*] Successfully delivered\n_____________________________")

            else:
              bot.send_message(
                  chat_id,
                  'The question has not been solved on chegg\n\nYour remaining chances are : '
                  + str(chances + 1))
              UserData.add_lost_chance(chat_id)
              bot.send_message(
                  adminID,
                  "Unsolved link or error in account\nhttps://www.chegg.com/homework-help/questions-and-answers/-q"
                  + str(qid))

          except Exception as e:
            qid = link.split('-q')[-1].split('?')[0].split('#')[0].split(
                '/')[0]
            UserData.add_lost_chance(chat_id)
            bot.send_message(
                adminID, "ERROR " + str(e) +
                '\nhttps://www.chegg.com/homework-help/questions-and-answers/-q'
                + str(qid))
            bot.send_message(
                chat_id,
                'Something went wrong. Kindly inform Admin or try a different link'
            )
            pass

        except Exception as e:

          qid = link.split('-q')[-1].split('?')[0].split('#')[0].split('/')[0]
          bot.send_message(
              adminID, "ERROR " + str(e) +
              '\nhttps://www.chegg.com/homework-help/questions-and-answers/-q'
              + str(qid))
          UserData.add_lost_chance(chat_id)
          bot.send_message(chat_id,
                           'The question has not been solved on chegg')

  #TextBook Soln
      else:
        filenam = link.split('homework-help/')[1]
        filename = filenam.split('?')[0]
        save_path = 'tbs'
        name = filename + '.html'
        completeName = os.path.join(save_path, name)

        try:
          cookies = Cookies_list.get_cookies()[0]
          cookiename = Cookies_list.get_cookies()[1]
          print('cookie selected')
        except:
          print('All accounts suspended')
          UserData.add_lost_chance(chat_id)
          bot.send_message(
              chat_id,
              "Unable to fetch the solution! Let the admin know and kindly wait. Sorry"
          )
          bot.send_message(adminID, "All accounts suspended")

        try:
          main_headers = {
              'authority':
              'gateway.chegg.com',
              'accept':
              '*/*',
              'accept-language':
              'en-US,en;q=0.9',
              'apollographql-client-name':
              'chegg-web',
              'apollographql-client-version':
              'main-75635ba6-3092331520',
              'authorization':
              'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
              'origin':
              'https://www.chegg.com',
              'referer':
              'https://www.chegg.com/',
              'sec-ch-ua':
              '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
              'sec-ch-ua-mobile':
              '?0',
              'sec-ch-ua-platform':
              '"Windows"',
              'sec-fetch-dest':
              'empty',
              'sec-fetch-mode':
              'cors',
              'sec-fetch-site':
              'same-site',
              'user-agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
              'x-chegg-page-type':
              'tbs-page',
              'x-chegg-referrer':
              'https://www.chegg.com/homework-help/simple-log-bridge-remote-area-consists-two-parallel-logs-pla-chapter-5.9-problem-2p-solution-9781111577735-exc',
          }
          session = requests.Session()
          lis = list(main_headers.items())
          random.shuffle(lis)
          headers = dict(lis)
          res = session.get(link, cookies=cookies, headers=main_headers)
          res = res.text
          soup = BeautifulSoup(res, 'html.parser')
          answer_data = soup.find('div', class_="csp-content")

          if answer_data != None:
            chapterId = res.split('&amp;isbn=')[0].split('?id=')[1]
            problemId = res.split('"problemId":"')[1].split('",')[0]
            isbn13 = res.split('"isbn13":"')[1].split('",')[0]
            token = res.split('"token":"')[1].split('","')[0]

            json_data = {
                'operationName': 'SolutionContent',
                'variables': {
                    'ean': isbn13,
                    'problemId': problemId,
                },
                'extensions': {
                    'persistedQuery': {
                        'version':
                        1,
                        'sha256Hash':
                        '0322a443504ba5d0db5e19b8d61c620d5cab59c99f91368c74dcffdbea3e502f',
                    },
                },
            }

            response = requests.post(
                'https://gateway.chegg.com/one-graph/graphql',
                cookies=cookies,
                headers=main_headers,
                json=json_data)
            jfile = json.loads(response.content)
            step_count = jfile['data']['tbsSolutionContent'][0]['totalSteps']
            contentId = jfile['data']['tbsSolutionContent'][0]['id']

            ans = []

            for step in range(step_count):
              ans.append('<div class="steps">Step ' + str(step + 1) + ' of ' +
                         str(step_count) + '</div>')
              html = jfile['data']['tbsSolutionContent'][0]['stepsLink'][step][
                  'html']
              link = jfile['data']['tbsSolutionContent'][0]['stepsLink'][step][
                  'link']

              if html != None and link != None:
                print('This tbs has both html and link')
                ans.append('<img src="' + str(link) + '" alt>')
                ans.append(html)
              elif html != None and link == None:
                print('\nThis Tbs has only html')
                ans.append(html)
              elif html == None and link != None:
                ans.append('<img src="' + str(link) + '" alt>')
                print('\nThis Tbs has only link')
            print(ans)
            json_data = {
                'operationName': 'Reviews',
                'variables': {
                    'reviewForContentQueryArguments': {
                        'contentId': contentId,
                        'contentReviewType': 'LIKE_DISLIKE',
                        'contentType': 'SOLUTION',
                    },
                },
                'extensions': {
                    'persistedQuery': {
                        'version':
                        1,
                        'sha256Hash':
                        '2044a012e91d0bdd2959ed33ac5c0113c9315c48cf513a59c2c4281914ba01e8',
                    },
                },
            }

            response = requests.post(
                'https://gateway.chegg.com/one-graph/graphql',
                cookies=cookies,
                headers=headers,
                json=json_data)
            review_data = json.loads(response.content)

            try:
              if review_data['data']['allReviews'][0][
                  'contentReviewValue'] == 'LIKE':
                likes = review_data['data']['allReviews'][0]['count']
                try:
                  if review_data['data']['allReviews'][1][
                      'contentReviewValue'] == 'DISLIKE':
                    dislikes = review_data['data']['allReviews'][1]['count']
                  else:
                    pass
                except:
                  dislikes = 0

              elif review_data['data']['allReviews'][0][
                  'contentReviewValue'] == 'DISLIKE':
                dislikes = review_data['data']['allReviews'][0]['count']
                likes = 0
            except:
              likes = 0
              dislikes = 0

            html = '''<html>
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width">
              <title>MathJax example</title>
             <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=AM_CHTML"></script>
            <style>pre.code {
              white-space: pre-wrap;
              background-color:#ededed;
            display: inline-block;
            width: 65em;
              padding-left: auto; /* now works */
              margin-left: 10;  /* now works */

            }
            pre.code::before {
              counter-reset: listing;

            }
            pre.code code {
              counter-increment: listing;
            }
            pre.code code::before {
              content: counter(listing) " ";
              display: inline-block;
              width: 2em;         /* now works */
              padding-left: auto; /* now works */
              margin-left: auto;  /* now works */
              text-align: right;  /* now works */
              background-color:#d9d7d7;
            color:red;
            }
            </style>
            <style>p {
              font-family: "Leelawadee UI";
            }</style>
            <style>
            .steps {
              width: 100%;
              background-color: rgb(255 203 203);
              line-height: 1;
              font-size: 0.875rem;
              font-weight: bold;
              padding: 0.75rem 1rem;
              border: 1px solid rgb(231, 231, 231);
              box-sizing: border-box;
              display: flex;
              -webkit-box-pack: justify;
              justify-content: space-between;
              cursor: pointer;
            }
            </style>
            </head>
            <body>'''
            rating = '<div class="rating"><h3 style="background-color:powderblue;">Likes =' + str(
                likes
            ) + '</h3><h3 style="background-color:powderblue;">Dislikes =' + str(
                dislikes
            ) + '</h3></div><style>.rating{font-size:20px;font-family:"Courier New";text-align-last: justify;margin-right: 100px;font-weight: bolder;}</style>'

            save_path = 'tbs'
            name = filename + '.html'
            completeName = os.path.join(save_path, name)
            with open(completeName, 'w', encoding='UTF-8') as f:
              f.write(html)
              f.write(rating)
              f.write(
                  '<head><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"><style>h1 ,.rating, .container {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}.Question {width:1000;margin-left: auto;margin-right: auto;max-width: border-box}div {width: 100vh;}img{max-width: 100%;height: auto;}.Question, .container {background-color:white;box-shadow: 0 0 2px 0px #666;border-radius: 5px;padding: 20px;margin-bottom: 1rem;} body{background-color:#F5F5F5;}</style></head>'
              )
              f.write(question)
              f.write('<div class="container">' + str(''.join(ans)) + '</div>')

            doc = open(completeName, 'rb')
            bot.send_document(
                chat_id,
                doc,
                caption="*" + str(chances) +
                " chances remaining*\n\n *open above file to see answer*\n\n *Use @freeportsuperbot for other sites like,\n\n🔅Transtutors\n🔅Study. com\n🔅Bartleby\n🔅Numerade\n🔅Solutioninn\n\nContact @The_Admin_Freeport for queries*",
                parse_mode='Markdown',
                reply_markup=gen_Main_menu())
            count = open('numberoflinkperday.txt').read()
            coun = int(count)
            coun += 1
            with open('numberoflinkperday.txt', 'w') as f:
              f.write(str(coun))
            bot.send_message(chat_id, str(chances) + " chances remaining")
            Account.using()
            bot.send_message(
                adminID,
                str(chat_id) + " " + filename + '.html received' +
                str(chances) + ", no.of links = " + str(coun) + ' ' +
                str(usingcookies))
            print(
                "\n********************Successfully delivered***********************"
            )
            bot.send_message(adminID, "tbs from site")

          else:
            bot.send_message(chat_id, "Error in providing textbook solution")

        except:
          bot.send_message(chat_id, "Something went wrong")

    except Exception as e:
      print(e)

  except Exception as e:
    print(e)

  print('_____________________________')


while True:
  try:
    bot.polling(none_stop=False, interval=1, timeout=300)
  except Exception:
    pass

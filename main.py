import binascii
import os
import random
import re
from turtle import teleport
import requests
import json
import mimetypes
from bs4 import BeautifulSoup
import requests
import telebot
import logging
import os
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
import boto3, secrets

# Replace 'YOUR_TOKEN' with the token you received from BotFather
TOKEN = '6970521351:AAGDVQF-S-hn_Kw5psMOg7ATIgNwEPZ8Uk4'
bot = telebot.TeleBot(TOKEN)

# ADMIN ID
sudos = [5511507580]

# Configure logging to save errors to a file
logging.basicConfig(filename='error.log', level=logging.ERROR)

# POINT FOLDER
directories = ["points", "messagstore", "photos"]

for directory in directories:
    if not os.path.exists(directory):
        os.mkdir(directory)
    else:
        print(f"Directory {directory} already exists.")


# ADDED POINT & CHECK POINT FUNCTION
def get_2_point_2_days(user):
    try:
        file_path = f"./points/{user}.txt"

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                exc = file.read().split("||")
                if int(exc[0]) < 1 or datetime.strptime(exc[1], "%Y-%m-%d") < datetime.today():
                    os.remove(file_path)
                    return [0, 0]
                else:
                    earlier = datetime.now()
                    later = datetime.strptime(exc[1], "%Y-%m-%d")
                    abs_diff = (later - earlier).days
                    return [int(exc[0]), abs_diff + 1]
        else:
            return [0, 0]
    except Exception as e:
        print(f"Error: {e}")
        logging.exception(f"Error on {user}: {e}")

# ADDED POINT FUNCTION
def add_2_point_2_days(user, points, days):
    try:
        file_path = f"./points/{user}.txt"

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                exc = file.read().split("||")

                if datetime.strptime(exc[1], "%Y-%m-%d") >= datetime.today():
                    earlier = datetime.now()
                    later = datetime.strptime(exc[1], "%Y-%m-%d")
                    abs_diff = (later - earlier).days
                    adays = days + abs_diff + 1
                    apoints = points + int(exc[0])
                else:
                    adays = days
                    apoints = points
        else:
            adays = days
            apoints = points

        dt = datetime.now().strftime("%Y-%m-%d")
        txt = f"{apoints}||{datetime.strftime(datetime.strptime(dt, '%Y-%m-%d') + timedelta(days=adays), '%Y-%m-%d')}"

        with open(file_path, 'w') as file:
            file.write(txt)

        return [apoints, adays]
    except Exception as e:
        print(f"Error: {e}")
        logging.exception(f"Error on {user}: {e}")   

# ADDED DEDUCT POINT FUNCTION
def deduct_point(user):
    try:
        file_path = f"./points/{user}.txt"

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                exc = file.read().split("||")

                if datetime.strptime(exc[1], "%Y-%m-%d") >= datetime.today():
                    earlier = datetime.now()
                    later = datetime.strptime(exc[1], "%Y-%m-%d")
                    abs_diff = (later - earlier).days
                    adays = abs_diff + 1

                    if int(exc[0]) > 0:
                        apoints = int(exc[0]) - 1
                    else:
                        apoints = 0
                else:
                    adays = 0
                    apoints = 0

                dt = datetime.now().strftime("%Y-%m-%d")
                txt = f"{apoints}||{datetime.strftime(datetime.strptime(dt, '%Y-%m-%d') + timedelta(days=adays), '%Y-%m-%d')}"

                with open(file_path, 'w') as file:
                    file.write(txt)

                return [apoints, adays]
        else:
            return [0, 0]

    except Exception as e:
        print(f"Error: {e}")
        logging.exception(f"Error on {user}: {e}")

#check point  & send message        
def check_points(message):
  user_id = message.from_user.id 
  chat_id = message.chat.id
  user = message.from_user.first_name
  pi = get_2_point_2_days(user_id)
  if pi[0] < 1 or pi[1] < 1:
    text22 = f"Hey {user}, Points must be purchased to get the solution.... to buy!"
    reply_markup = telebot.types.InlineKeyboardMarkup()
    reply_markup.add(telebot.types.InlineKeyboardButton(text='Contact Here 💚', url='t.me/spacenx1'))
    bot.send_message(chat_id, text22, reply_markup=reply_markup) 
    print("User does not have enough points.")
    exit()
  else:
    return 

# TOKEN GENERATE
def generate_unique_token(existing_tokens):
  while True:
    gen_token = binascii.hexlify(os.urandom(8)).decode(
        'utf-8')  # 8 bytes = 16 characters in hex
    if gen_token not in existing_tokens:
      return gen_token


# UPLOAD TO AWS S3
def upload_to_s3(file_answer):
  s3 = boto3.client(
      's3',
      region_name='us-east-1',
      aws_access_key_id='YOUR AWS KEY ID',
      aws_secret_access_key='YOUR AWS ACCESS ID',
      config=boto3.session.Config(signature_version='s3v4'))

  bucket_name = 'supernova558866'
  s3.upload_file(file_answer, 'supernova558866', file_answer)
  link = s3.generate_presigned_url('get_object',
                                   Params={
                                       'Bucket': 'AWSBucketName',
                                       'Key': file_answer
                                   },
                                   ExpiresIn=100000)
  print("\033[92mlink\033[0m")
  existing_tokens = set()  # Assume you're keeping track of generated tokens
  GenToken = generate_unique_token(existing_tokens)
  s3.upload_file(file_answer,
                 bucket_name,
                 f'{GenToken}.html',
                 ExtraArgs={'ContentType': 'text/html'})
  url3 = s3.generate_presigned_url(
      ClientMethod='get_object',
      Params={
          'Bucket': bucket_name,
          'Key': f'{GenToken}.html'
      },
      ExpiresIn=86400  # 1 Day
  )
  return url3

def get_random_cookie(json_file_path):
    with open(json_file_path, 'r') as file:
        json_contents = file.read()
        try:
            cookie_array = json.loads(json_contents)
        except json.JSONDecodeError:
            return 'Error decoding JSON.'
        
        cookies = cookie_array.get('cookies', [])
        if cookies:
            random.shuffle(cookies)
            return cookies
        else:
            return []

def check_and_update_cookie(cookies, json_file_path):
    try:
        for cookie in cookies:
            url = "https://gateway.chegg.com/one-graph/graphql"

            payload2 = json.dumps({
            "operationName": "hasActiveCheggStudy",
            "variables": {},
            "extensions": {
                "persistedQuery": {
                "version": 1,
                "sha256Hash": "f6707940e697a3a359f218b04ad23eee36b4d11cea2b8b59221a572fdd8c554b"
                }
            }
            })
            headers = {
            'accept': '*/*, application/json',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6',
            'apollographql-client-name': 'chegg-web',
            'apollographql-client-version': 'main-228958ec-6525977630',
            'authorization': 'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
            'content-type': 'application/json',
            'cookie': cookies,
            'dnt': '1',
            'origin': 'https://www.chegg.com',
            'referer': 'https://www.chegg.com/',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            }

            response = requests.request("POST", url, headers=headers, data=payload2)
            
            response_data = json.loads(response.text)
            print(response.text)
            if response_data['data']['me']['hasCheggStudy']:
                payload = json.dumps({
                "operationName": "resetBanner",
                "variables": {},
                "extensions": {
                    "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "c78e259d8e022c643865405d193982aaa3c4a8167ea978dda04ce6b440cfdb55"
                    }
                }
                })

                response2 = requests.request("POST", url, headers=headers, data=payload)

                response_data = json.loads(response2.text)
                print(response2.text)

                if response_data['data']['me']['accountSharing']['userStatus'] in ['RELEASED', 'OK']:
                    return cookie
        
        return '' 
    except Exception as e:
        print(f"Error : {e}")

def answerresponse(numero):
    try:
        json_file_path = "cookieschegg.json"
        cookies = get_random_cookie(json_file_path)
        validCookie = check_and_update_cookie(cookies, json_file_path)
        url = "https://gateway.chegg.com/one-graph/graphql"

        payload = json.dumps({
        "operationName": "QnaPageAnswerNonSub",
        "variables": {
            "id": numero
        },
        "extensions": {
            "persistedQuery": {
            "version": 1,
            "sha256Hash": "62ba61083983d2d69daf48dfb6d319177c4d4aca206a00e766104c07391ed8eb"
            }
        }
        })
        headers = {
        'accept': '*/*, application/json',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'apollographql-client-name': 'chegg-web',
        'apollographql-client-version': 'main-3e92a96e-6513519426',
        'authorization': 'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
        'content-type': 'application/json',
        'cookie': validCookie,
        'dnt': '1',
        'origin': 'https://www.chegg.com',
        'referer': 'https://www.chegg.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"Response Status : {response.status_code}")
        if(response.status_code == 200):
            return response.text
        else:
            return None
    except Exception as e:
       print(f"Error : {e}")     

def getlikedislike(legacyId):
    try:
        url = "https://gateway.chegg.com/one-graph/graphql"

        payload = json.dumps({
            "operationName": "ReviewsV2",
            "variables": {
                "reviewForContentQueryArguments": {
                "contentReviewType": "LIKE_DISLIKE",
                "contentType": "ANSWER",
                "contentId": f"{legacyId}"
                }
            },
            "extensions": {
                "persistedQuery": {
                "version": 1,
                "sha256Hash": "9b54ed3b84cc1267ff0a42418c41de9b79b40b0dd22043c4d5583f7022f16aa1"
                }
            }
        })
        headers = {
        'accept': '*/*, application/json',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'apollographql-client-name': 'chegg-web',
        'apollographql-client-version': 'main-3e92a96e-6513519426',
        'authorization': 'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
        'content-type': 'application/json',
        'cookie': 'country_code=IN; langPreference=en-US; CVID=b0de5b8c-22d7-42b2-971d-755881ff2fdd; CSID=1711834236436; V=b6feb14c7c50bdf707eff45d1b2d58a4660884806ccccc.10898450; pxcts=c0eba53e-eedc-11ee-b1da-2b9d92fac212; _pxvid=c0eb9653-eedc-11ee-b1da-85e339a00831; _cc_id=34a8d73670155dc8dea4ca42ef740ae7; panoramaId_expiry=1711920647526; cto_bundle=QOsms19qJTJCMjZOcGRDTG12YXV1a0Foc1A2SElDeVp6S1ZPcHdWJTJCJTJCSFRFUlltUEVpeUF4MSUyQllWc3FGQVQwUTdXNWd0amVpbnRIeDFXbDZyNEI4YWxsNHB1UTRTNnY3Qmx6ZTF3dDVMc0Zoa1MlMkJhd2FPdDQ1M3R6Wm9rR0xFVVlTNXBXNmlwM0hJJTJGQzl3ZFZkQ1RkbGhNbUJrUXclM0QlM0Q; permutive-id=49f7995f-19d0-4617-b78b-c566261503c2; forterToken=4f972adef55042a68c6f155dc347eba4_1711834244640__UDF43-m4_13ck_; _oa_sso=https%253A%252F%252Fwww.chegg.com; refreshToken=ext.a0.t00.v1.MU9hYvhspga07EiLcaNRb3NcnycNpKkoJVmKkv1vJ4J4V9g5eeyDTbAZgBn6gPXc7SR5sBja3n3KXVJpxiBzM_A; refresh_token=ext.a0.t00.v1.MU9hYvhspga07EiLcaNRb3NcnycNpKkoJVmKkv1vJ4J4V9g5eeyDTbAZgBn6gPXc7SR5sBja3n3KXVJpxiBzM_A; id_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im11c3RrZWVtMzI0QGdtYWlsLmNvbSIsImlzcyI6Imh1Yi5jaGVnZy5jb20iLCJhdWQiOiJDSEdHIiwiaWF0IjoxNzExODM0MjU1LCJleHAiOjE3MjczODYyNTUsInN1YiI6IjRjYzI3NThiLTEzMDMtNDBlNi1hNjI1LTcyZGQ2ZmRkMTEwMSIsInJlcGFja2VyX2lkIjoiYXB3IiwiY3R5cCI6ImlkIiwiaWRzaWQiOiJlOTBmYmU2NSIsImlkc3QiOjE3MTE4MzQyNTUwMjgsImlkc2ciOiJwYXNzd29yZGxlc3MifQ.0IXeZkGOytaBsL2LkFQzXr2i2gqCMk6PCpUIG9SzdxuwbU-TOPj8omUaeXW6vWzkzipR1w3M8nx-RAXwETpiUiQtfqCTWM-Mj7AsQH0812R1yDK5aGhJ7xH3NzY82EbP6i1Ll2NPXulM0_G2GvaT2HSdaR2e9At4YB4S4Nhy_bw4xCP2JCggiE9yx9YHSMYAA6YlFqG7alkRnKLTdekRSngRRvuEvMBRU2nL6x1DGSKrazeq1S-j14BKQDsFlHoufidhWfuvA5r-1EjpZsKo1G4pRdNZc5uP1nB5MKJssmeVuU2n1v3QlEPpwdwtuxJhQRW0eLlcUp-0sl3P01oLcg; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL3Byb3h5LmNoZWdnLmNvbS9jbGFpbXMvYXBwSWQiOiJDSEdHIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsInN1YiI6IjRjYzI3NThiLTEzMDMtNDBlNi1hNjI1LTcyZGQ2ZmRkMTEwMSIsImF1ZCI6WyJ0ZXN0LWNoZWdnIiwiaHR0cHM6Ly9jaGVnZy1wcm9kLmNoZWdnLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MTE4MzQyNTQsImV4cCI6MTcxMTgzNTY5NCwiYXpwIjoiRmlwajNhbkY0VXo4TlVZSE9jYmpMTXg2cTR6VktFT2UiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIGFkZHJlc3MgcGhvbmUgb2ZmbGluZV9hY2Nlc3MiLCJndHkiOiJwYXNzd29yZCIsInJlcGFja2VyX2lkIjoiYXB3IiwiY2hnaHJkIjp0cnVlLCJjdHlwIjoiYWNjZXNzIn0.2cguWX6tZSsTB3Zs_XaXKdfYEwyBLO_eD9oQwkqFwDe7dLWsYMkk9LeVRpD_3KkYL5lYnT321czwwk9568QkgEdff9NxcqNo2PakUnuzqQIos5gql677BgwQ1cfdNhRXVBRJwtm86OPoUyt0fk7JkUgNeusgRQWu5i37DL2MoVQ1Ddp6OIy6fbd9LrlLGo3Z97gaHY6vmoPbuxcHP_QU8aBuHSIoSVIQSndBNiOdn-8Gsv-AHpPHuyQcCnqEdwJ4FdG2o-oebEsJzjyFgYJOICNu1WgTPqjLx9EX1UUcT1q7s7FyTQo9R-bTQbDEujVXH-TH4aNmYh78YLIOfnWLBw; access_token_expires_at=1711835695035; opt-user-profile=b0de5b8c-22d7-42b2-971d-755881ff2fdd%252C27775730017%253A27763050017%252C27986810248%253A27952530505; CSessionID=3840acc4-cd25-4ca9-91b5-11adcf0bf208; hwh_order_ref=/homework-help/questions-and-answers/p10-198-increasing-demand-xylene-petrochemical-industry-production-xylene-toluene-dispropo-q63956832?auth_provider=oa&nruuid=d8a1d3de; _px3=732ba025cf64d34a2a7d91a176de5befaca1f1e666b7e0c615005383bb8a9cd5:EYzZYXAcA+/3eLpshvS6t0gZdCJs8vXdMgjgbL1xE2B8MHVydS7+ovPBcBa0if12nIJVJP1oeo/8T0JSVwzu2Q==:1000:W0N6rr4lbIHWvy11S2Jr8yOrX+qn5R4KHFfau/74dbXQWX1a9DAqYfjfDxiso+aIiZt/TVmt1UhK978bpBpfGMqxpL3aUX0NyjMe1uNxnjrCnFIlu4IBrKrFvjeVbEOGdi3xXmwovJ1dN8xuTIV2bpon4La/sC5Jr6iA+61uqsicSNEYf1ThvXJdlbtFO4pC/Uyya2ycDhD2pZtzxjSROz3tnWyvxfT/SsX52DobsAE=; _px=EYzZYXAcA+/3eLpshvS6t0gZdCJs8vXdMgjgbL1xE2B8MHVydS7+ovPBcBa0if12nIJVJP1oeo/8T0JSVwzu2Q==:1000:XwFiCwfwznLtLN/73//n5oGPrfZ6I0p8UJYQx92atxbVFZs8ODowqL5zrS3ZgLtOZubIPBKu/le/m7zR/R6gg/5UyCpWPjK+opm82BRNj0YW7OMX9wYsgDv62JlVMO673PQ1NLAfEkAz4CKoB8Q71ihVjJjjhr2ezpvvfur1pwoyn1Rs6bUQvF0rgptlPsBUx9DxN1x+hly9lVgaItbpBv8rg5QZttW1j4rmlnKMhaP3fS0VPNUK6JBtb5hxch/V0WnOI9bx9yw4Wt54/q9rTQ==; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Mar+31+2024+03%3A01%3A20+GMT%2B0530+(India+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5b062e91-f141-4f04-be56-51109e6ae0ac&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=fnc%3A0%2Csnc%3A1%2Ctrg%3A0%2Cprf%3A0&AwaitingReconsent=false; _pxde=8a5c5079f09d6c2be5f69f35d2b276503887a1b03435837d86520035d8755ae4:eyJ0aW1lc3RhbXAiOjE3MTE4MzQyODMwNzd9',
        'dnt': '1',
        'origin': 'https://www.chegg.com',
        'referer': 'https://www.chegg.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-chegg-referrer': 'homework-help/questions-and-answers/p10-198-increasing-demand-xylene-petrochemical-industry-production-xylene-toluene-dispropo-q63956832?auth_provider=oa&nruuid=d8a1d3de',
        'x-chegg-search-id': 'f6d5356f-28a4-430e-9206-9d17d2413e60'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"Response Status : {response.status_code}")
        if(response.status_code == 200):
            data = json.loads(response.text)
            like = data['data']['allReviews'][0]['count']
            dislike= data['data']['allReviews'][1]['count']
            return [like,dislike]
        else:
            return [None,None]
    except Exception as e:
        print(f"Error : {e}")    


def Transformlink(text):
    try:
        url = "https://gateway.chegg.com/one-graph/graphql"

        payload = json.dumps({
                "operationName": "TransformUrl",
                "variables": {
                    "url": {
                        "url": text,
                        "hostPrefix": False
                    }
                },
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "03e0153ed664185b1ec608f1e30ed431054d03d09e308ad0a4ff19b6e5725512"
                    }
                }
            }
        )
        headers = {
        'accept': '*/*, application/json',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'apollographql-client-name': 'chegg-web',
        'apollographql-client-version': 'main-3e92a96e-6513519426',
        'authorization': 'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
        'content-type': 'application/json',
        'cookie': 'country_code=IN; langPreference=en-US; CVID=b0de5b8c-22d7-42b2-971d-755881ff2fdd; CSID=1711834236436; V=b6feb14c7c50bdf707eff45d1b2d58a4660884806ccccc.10898450; pxcts=c0eba53e-eedc-11ee-b1da-2b9d92fac212; _pxvid=c0eb9653-eedc-11ee-b1da-85e339a00831; _cc_id=34a8d73670155dc8dea4ca42ef740ae7; panoramaId_expiry=1711920647526; cto_bundle=QOsms19qJTJCMjZOcGRDTG12YXV1a0Foc1A2SElDeVp6S1ZPcHdWJTJCJTJCSFRFUlltUEVpeUF4MSUyQllWc3FGQVQwUTdXNWd0amVpbnRIeDFXbDZyNEI4YWxsNHB1UTRTNnY3Qmx6ZTF3dDVMc0Zoa1MlMkJhd2FPdDQ1M3R6Wm9rR0xFVVlTNXBXNmlwM0hJJTJGQzl3ZFZkQ1RkbGhNbUJrUXclM0QlM0Q; permutive-id=49f7995f-19d0-4617-b78b-c566261503c2; forterToken=4f972adef55042a68c6f155dc347eba4_1711834244640__UDF43-m4_13ck_; _oa_sso=https%253A%252F%252Fwww.chegg.com; refreshToken=ext.a0.t00.v1.MU9hYvhspga07EiLcaNRb3NcnycNpKkoJVmKkv1vJ4J4V9g5eeyDTbAZgBn6gPXc7SR5sBja3n3KXVJpxiBzM_A; refresh_token=ext.a0.t00.v1.MU9hYvhspga07EiLcaNRb3NcnycNpKkoJVmKkv1vJ4J4V9g5eeyDTbAZgBn6gPXc7SR5sBja3n3KXVJpxiBzM_A; id_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im11c3RrZWVtMzI0QGdtYWlsLmNvbSIsImlzcyI6Imh1Yi5jaGVnZy5jb20iLCJhdWQiOiJDSEdHIiwiaWF0IjoxNzExODM0MjU1LCJleHAiOjE3MjczODYyNTUsInN1YiI6IjRjYzI3NThiLTEzMDMtNDBlNi1hNjI1LTcyZGQ2ZmRkMTEwMSIsInJlcGFja2VyX2lkIjoiYXB3IiwiY3R5cCI6ImlkIiwiaWRzaWQiOiJlOTBmYmU2NSIsImlkc3QiOjE3MTE4MzQyNTUwMjgsImlkc2ciOiJwYXNzd29yZGxlc3MifQ.0IXeZkGOytaBsL2LkFQzXr2i2gqCMk6PCpUIG9SzdxuwbU-TOPj8omUaeXW6vWzkzipR1w3M8nx-RAXwETpiUiQtfqCTWM-Mj7AsQH0812R1yDK5aGhJ7xH3NzY82EbP6i1Ll2NPXulM0_G2GvaT2HSdaR2e9At4YB4S4Nhy_bw4xCP2JCggiE9yx9YHSMYAA6YlFqG7alkRnKLTdekRSngRRvuEvMBRU2nL6x1DGSKrazeq1S-j14BKQDsFlHoufidhWfuvA5r-1EjpZsKo1G4pRdNZc5uP1nB5MKJssmeVuU2n1v3QlEPpwdwtuxJhQRW0eLlcUp-0sl3P01oLcg; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL3Byb3h5LmNoZWdnLmNvbS9jbGFpbXMvYXBwSWQiOiJDSEdHIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsInN1YiI6IjRjYzI3NThiLTEzMDMtNDBlNi1hNjI1LTcyZGQ2ZmRkMTEwMSIsImF1ZCI6WyJ0ZXN0LWNoZWdnIiwiaHR0cHM6Ly9jaGVnZy1wcm9kLmNoZWdnLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MTE4MzQyNTQsImV4cCI6MTcxMTgzNTY5NCwiYXpwIjoiRmlwajNhbkY0VXo4TlVZSE9jYmpMTXg2cTR6VktFT2UiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIGFkZHJlc3MgcGhvbmUgb2ZmbGluZV9hY2Nlc3MiLCJndHkiOiJwYXNzd29yZCIsInJlcGFja2VyX2lkIjoiYXB3IiwiY2hnaHJkIjp0cnVlLCJjdHlwIjoiYWNjZXNzIn0.2cguWX6tZSsTB3Zs_XaXKdfYEwyBLO_eD9oQwkqFwDe7dLWsYMkk9LeVRpD_3KkYL5lYnT321czwwk9568QkgEdff9NxcqNo2PakUnuzqQIos5gql677BgwQ1cfdNhRXVBRJwtm86OPoUyt0fk7JkUgNeusgRQWu5i37DL2MoVQ1Ddp6OIy6fbd9LrlLGo3Z97gaHY6vmoPbuxcHP_QU8aBuHSIoSVIQSndBNiOdn-8Gsv-AHpPHuyQcCnqEdwJ4FdG2o-oebEsJzjyFgYJOICNu1WgTPqjLx9EX1UUcT1q7s7FyTQo9R-bTQbDEujVXH-TH4aNmYh78YLIOfnWLBw; access_token_expires_at=1711835695035; opt-user-profile=b0de5b8c-22d7-42b2-971d-755881ff2fdd%252C27775730017%253A27763050017%252C27986810248%253A27952530505; CSessionID=3840acc4-cd25-4ca9-91b5-11adcf0bf208; hwh_order_ref=/homework-help/questions-and-answers/p10-198-increasing-demand-xylene-petrochemical-industry-production-xylene-toluene-dispropo-q63956832?auth_provider=oa&nruuid=d8a1d3de; _px3=732ba025cf64d34a2a7d91a176de5befaca1f1e666b7e0c615005383bb8a9cd5:EYzZYXAcA+/3eLpshvS6t0gZdCJs8vXdMgjgbL1xE2B8MHVydS7+ovPBcBa0if12nIJVJP1oeo/8T0JSVwzu2Q==:1000:W0N6rr4lbIHWvy11S2Jr8yOrX+qn5R4KHFfau/74dbXQWX1a9DAqYfjfDxiso+aIiZt/TVmt1UhK978bpBpfGMqxpL3aUX0NyjMe1uNxnjrCnFIlu4IBrKrFvjeVbEOGdi3xXmwovJ1dN8xuTIV2bpon4La/sC5Jr6iA+61uqsicSNEYf1ThvXJdlbtFO4pC/Uyya2ycDhD2pZtzxjSROz3tnWyvxfT/SsX52DobsAE=; _px=EYzZYXAcA+/3eLpshvS6t0gZdCJs8vXdMgjgbL1xE2B8MHVydS7+ovPBcBa0if12nIJVJP1oeo/8T0JSVwzu2Q==:1000:XwFiCwfwznLtLN/73//n5oGPrfZ6I0p8UJYQx92atxbVFZs8ODowqL5zrS3ZgLtOZubIPBKu/le/m7zR/R6gg/5UyCpWPjK+opm82BRNj0YW7OMX9wYsgDv62JlVMO673PQ1NLAfEkAz4CKoB8Q71ihVjJjjhr2ezpvvfur1pwoyn1Rs6bUQvF0rgptlPsBUx9DxN1x+hly9lVgaItbpBv8rg5QZttW1j4rmlnKMhaP3fS0VPNUK6JBtb5hxch/V0WnOI9bx9yw4Wt54/q9rTQ==; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Mar+31+2024+03%3A01%3A20+GMT%2B0530+(India+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5b062e91-f141-4f04-be56-51109e6ae0ac&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=fnc%3A0%2Csnc%3A1%2Ctrg%3A0%2Cprf%3A0&AwaitingReconsent=false; _pxde=8a5c5079f09d6c2be5f69f35d2b276503887a1b03435837d86520035d8755ae4:eyJ0aW1lc3RhbXAiOjE3MTE4MzQyODMwNzd9',
        'dnt': '1',
        'origin': 'https://www.chegg.com',
        'referer': 'https://www.chegg.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-chegg-referrer': 'homework-help/questions-and-answers/p10-198-increasing-demand-xylene-petrochemical-industry-production-xylene-toluene-dispropo-q63956832?auth_provider=oa&nruuid=d8a1d3de',
        'x-chegg-search-id': 'f6d5356f-28a4-430e-9206-9d17d2413e60'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"Response Status : {response.status_code}")
        if(response.status_code==200):
            data = json.loads(response.text)
            uuid_string = data['data']['transformUrl']['iosDeeplinkEncoded']
            parts = uuid_string.split('%2F')
            uuid = parts[-1]
            return uuid
        else:
            return None
    except Exception as e:
        print(f"Error:{e}")    

def questionBody(uuid):
    try:
        url = "https://gateway.chegg.com/one-graph/graphql"
        payload = json.dumps({
            "operationName": "QuestionById",
            "variables": {
                "uuid": uuid
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "6fb6122e78f35ff4ef1005cadc05efa7359480ce0581b949ae946fef51659f59"
                }
            }
        })
        headers = {
        'accept': '*/*, application/json',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'apollographql-client-name': 'chegg-web',
        'apollographql-client-version': 'main-3e92a96e-6513519426',
        'authorization': 'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
        'content-type': 'application/json',
        'cookie': 'CVID=d1f9c6c8-ec7b-4399-9b4b-d2ff2f278c23; V=b0434a206185d1248be05d0946eae46264326471c20c48.54596028; _scid=6c255f11-eeeb-4952-9f47-f526ef3502ac; OneTrustWPCCPAGoogleOptOut=true; _pxvid=adcf6dfd-d6bc-11ed-8e6d-0faf9f3ee8a1; C=0; O=0; exp=C026A; sbm_country=IN; _pubcid=ca273e29-6149-470c-a834-33f240966d09; _lr_env_src_ats=false; gid=1; gidr=MA; pbjs-unifiedid_cst=0Cw6LNAs7Q%3D%3D; _pubcid_cst=zix7LPQsHA%3D%3D; permutive-id=a8230da6-f7e3-4894-822f-5ee4d8850c78; _ga=GA1.1.323224641.1698858627; _hjSessionUser_3091164=eyJpZCI6ImQ4MTY0ZTRkLWZkZTctNTY0OS05OGRkLTA2MTU0NGY3ZjA0ZCIsImNyZWF0ZWQiOjE2OTg4NTg2MjY2NTQsImV4aXN0aW5nIjp0cnVlfQ==; expkey=031A203D5924CDC5B25EB8E2333DF41C; exp_id=c902e93cd0626069a79faa54c3bcd02a654558a8f95810.66458786; ab.storage.sessionId.49cbafe3-96ed-4893-bfd9-34253c05d80e=%7B%22g%22%3A%22e5ac116f-243c-5471-fc60-267be20c5a74%22%2C%22e%22%3A1699045297078%2C%22c%22%3A1699043497079%2C%22l%22%3A1699043497079%7D; ab.storage.deviceId.49cbafe3-96ed-4893-bfd9-34253c05d80e=%7B%22g%22%3A%22e37fbffa-c67e-998e-455e-e6c03776bf68%22%2C%22c%22%3A1699043497086%2C%22l%22%3A1699043497086%7D; _ga_1Y0W4H48JW=GS1.1.1699043401.3.1.1699043675.0.0.0; _ga_HRYBF3GGTD=GS1.1.1699043400.3.1.1699043675.0.0.0; _sp_id.ad8a=8598e398-146e-457a-ad6c-1ef557423766.1696510704.4.1699680974.1698097029.30db20cc-8a0f-459f-b64a-824613ad4e52; opt-user-profile=b0434a206185d1248be05d0946eae46264326471c20c48.54596028%2C24115930466%3A24157310052%2C24985571146%3A24987031066; _vid_t=0f2pITEI2LF8uIGMF1tT5v18DlnwBpT9bjW45MyUPSlwXJGNcvDWWkxSUIgV77AUbG2EpwC2BAc/viEn9qSzJqcQTw==; DFID=web|yXBiJB2k7XUWqDDjbm7C; _pbjs_userid_consent_data=3524755945110770; _sharedid=000d51b9-597f-42d5-b061-9809491ad0c9; pbjs-unifiedid=%7B%22TDID%22%3A%223bc55e1c-a5d4-4638-b877-8d9a5af9ce43%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-10-15T11%3A23%3A53%22%7D; connectId=%7B%22vmuid%22%3A%22KySDV45ROVyHmZA4nFaxcz9r2Ly3IzoTzFHASjHpbJdjgz0g9u4H1U_ZRIbZjS6nR9cg_jk2U5SJCl9oq7dH-g%22%2C%22connectid%22%3A%22KySDV45ROVyHmZA4nFaxcz9r2Ly3IzoTzFHASjHpbJdjgz0g9u4H1U_ZRIbZjS6nR9cg_jk2U5SJCl9oq7dH-g%22%2C%22connectId%22%3A%22KySDV45ROVyHmZA4nFaxcz9r2Ly3IzoTzFHASjHpbJdjgz0g9u4H1U_ZRIbZjS6nR9cg_jk2U5SJCl9oq7dH-g%22%2C%22ttl%22%3A24%2C%22he%22%3A%225ecf6d62dc5d50beea8797f84ab271ff4dc634f5f4fb408cfdf46be53bc94e02%22%2C%22lastSynced%22%3A1700047434018%2C%22lastUsed%22%3A1700047434018%7D; connectid=%7B%22vmuid%22%3A%22KySDV45ROVyHmZA4nFaxcz9r2Ly3IzoTzFHASjHpbJdjgz0g9u4H1U_ZRIbZjS6nR9cg_jk2U5SJCl9oq7dH-g%22%2C%22connectid%22%3A%22KySDV45ROVyHmZA4nFaxcz9r2Ly3IzoTzFHASjHpbJdjgz0g9u4H1U_ZRIbZjS6nR9cg_jk2U5SJCl9oq7dH-g%22%2C%22connectId%22%3A%22KySDV45ROVyHmZA4nFaxcz9r2Ly3IzoTzFHASjHpbJdjgz0g9u4H1U_ZRIbZjS6nR9cg_jk2U5SJCl9oq7dH-g%22%2C%22ttl%22%3A24%2C%22he%22%3A%225ecf6d62dc5d50beea8797f84ab271ff4dc634f5f4fb408cfdf46be53bc94e02%22%2C%22lastSynced%22%3A1700047434018%2C%22lastUsed%22%3A1700047434018%7D; connectid_cst=0Cw6LNAs7Q%3D%3D; _sctr=1%7C1700159400000; __gads=ID=36304ba78a4a5160:T=1700047432:RT=1700253304:S=ALNI_MZ295J3vDa5ej2Bd0IXVMeI1TBoPw; __gpi=UID=00000c87d1bc609c:T=1700047432:RT=1700253304:S=ALNI_MYhff7elPkh8EWtC5_2gHFU8OB9uw; _awl=2.1700253381.5-c627b420b5c568406859e7b7638f97e9-6763652d617369612d6561737431-1; usprivacy=1YYY; _scid_r=6c255f11-eeeb-4952-9f47-f526ef3502ac; country_code=IN; hwh_order_ref=/homework-help/questions-and-answers/task2-curriculum-bachelor-science-task-create-knowledge-base-describing-courses-prerequisi-q119964027; CSID=1700499233437; pxcts=6547d14b-87c5-11ee-bf10-2842ecff1d6f; schoolapi=null; PHPSESSID=62flk55dgq1863cihkpquhbu78; CSessionID=b335218c-5a62-4353-8f1e-3e114296be20; user_geo_location=%7B%22country_iso_code%22%3A%22IN%22%2C%22country_name%22%3A%22India%22%2C%22region%22%3A%22DL%22%2C%22region_full%22%3A%22National+Capital+Territory+of+Delhi%22%2C%22city_name%22%3A%22Delhi%22%2C%22postal_code%22%3A%22110008%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22en-IN%22%2C%22hi-IN%22%2C%22gu-IN%22%2C%22kn-IN%22%2C%22kok-IN%22%2C%22mr-IN%22%2C%22sa-IN%22%2C%22ta-IN%22%2C%22te-IN%22%2C%22pa-IN%22%5D%7D%7D; _pxff_fp=1; sbm_a_b_test=1-control; ftr_blst_1h=1700499241699; _cc_id=5224b6adb348393dbd27b58a4198feea; panoramaId_expiry=1701104043476; panoramaId=d7959165730aa3084965a088e79516d5393847885fb7239a0429c8ad63ad8577; panoramaIdType=panoIndiv; forterToken=051b65f74be54aecbe9e6cd210cc9e81_1700499240767__UDF43-m4_13ck; id_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im11c3RrZWVtb2ZmaWNpYWxAZ21haWwuY29tIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsImF1ZCI6IkNIR0ciLCJpYXQiOjE3MDA0OTkyNTAsImV4cCI6MTcxNjA1MTI1MCwic3ViIjoiNzdkZGU2ZDgtZGIwYi00YzkwLTgyMzUtMzk1YzFlYmU0Yzg3IiwicmVwYWNrZXJfaWQiOiJhcHciLCJjdHlwIjoiaWQiLCJpZHNpZCI6IjEyZGJkODYzIiwiaWRzdCI6MTcwMDQ5OTI1MDU1NiwiaWRzZyI6InBhc3N3b3JkbGVzcyJ9.OAkMcZUd_pOsNyZzAqIyq9VLjc3BFNw_TnS7baSx3IAZMce1U2DXL3VbRLNNvwz29jMISVQPaTet8b64hBEU7wXyN2JT8rncmcnlrG-fo1KH0gJiWuLcVzu9X9Z-unIspH2xUQp26J-iMzmbz4li5lFb7Ach5V_tfM973hNWzeiWezE8ajJ2RMA73ZInfi188xwAgCVs8HwEhE0KK1q8IBcG4WCKs6qv8LXAQz9GbgJX6dQ_Zpweuh18j1ghbrQKJpnSJS2wk2dcAGPUAEZIgsV4SUV4_NzQyaGUctV5VpMoeln8WyIXXkvnE5zQa0JO2Bdnvk1yepoeNTOCOoI5vw; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL3Byb3h5LmNoZWdnLmNvbS9jbGFpbXMvYXBwSWQiOiJDSEdHIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsInN1YiI6Ijc3ZGRlNmQ4LWRiMGItNGM5MC04MjM1LTM5NWMxZWJlNGM4NyIsImF1ZCI6WyJ0ZXN0LWNoZWdnIiwiaHR0cHM6Ly9jaGVnZy1wcm9kLmNoZWdnLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MDA0OTkyNTAsImV4cCI6MTcwMDUwMDY5MCwiYXpwIjoiRmlwajNhbkY0VXo4TlVZSE9jYmpMTXg2cTR6VktFT2UiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIGFkZHJlc3MgcGhvbmUgb2ZmbGluZV9hY2Nlc3MiLCJndHkiOiJwYXNzd29yZCIsInJlcGFja2VyX2lkIjoiYXB3IiwiY2hnaHJkIjp0cnVlLCJjdHlwIjoiYWNjZXNzIn0.sFEXOHtw_2GqIhUqve-fOMudZu1b5h1pEWr8YywiD5rxfl0dO0smsnM4xLahzycOTylFZIs2AHBw60IKlL1DDuwL8NHmmQedKsUlba-DeP8eShySf5btWijVIGKh-7-M1pxXow3iquV_CDEHcn4GG0YalQP4laC6q6huxeTmmtOAYfO-Xp-7lNTu7BTGVmEgdXvJHR_9PV4x71_Yi1CtAsy0UY-_9mZ0iu5kPlJZFzW_bW1ZRgVtx5ZwQSZ_S3yc2wI3BqPw-O5uJk_1tD_MBLs1_mo3lj9RgefV_FvYDtGW1vv2UZ-HienaVhsggH3QMnvPOXlGl_gsMjumIu26xg; U=35e10940cc1e405f15beb1aa71c2eecd; SU=cgFvt3lxMoj2nk36qeMlDtBVR434GeWMgb6kH_oUpvZ342Jfjja7zQMGcOPECCyCguX5mCrpVMHh9J9GCvgVAY9vnJWiR36GHxYY0cq7QNwz5j416uHwJYg9P-JTeN4Q; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Nov+20+2023+22%3A24%3A16+GMT%2B0530+(India+Standard+Time)&version=202310.2.0&isIABGlobal=false&hosts=&consentId=ec54b66b-f6a4-4247-8a8a-d0311a89fe7d&interactionCount=1&landingPath=NotLandingPage&groups=fnc%3A0%2Csnc%3A1%2Ctrg%3A0%2Cprf%3A0&AwaitingReconsent=false&browserGpcFlag=0; _px3=57ec2b6d526da01f42a30ac6d49681513fe427c70b4eae93bc6c5014495d69a4:946lUVQ4sH0OiYszVxKgx8E4vgzBayxW0uthG2SvP6pqEIRRDEDGj6YZ5S3rVsKT3H2j7Sj+rJ4RceLUlS6Y+A==:1000:4nfPJWldk4gWKjt5AvoopdLb1VnDMqNQB7T3qF1pW528FruTofUT3bZMo1UagUEjfdOMr+9bArV0a7g+pCs4YqtpmS5Whki0Tpx2qewQ+WpMP9/SDvu82ErCJdreTeM3mrrRHxJw45EAyi5tyUnnGbz7oZi0/rx+LL617mYqjME/o54ruCKdhLCEffepRnqLNVv05rLShk4kw1x9PJMabXFX8TBOh2vN6mQ4Tpl67V4=; _px=946lUVQ4sH0OiYszVxKgx8E4vgzBayxW0uthG2SvP6pqEIRRDEDGj6YZ5S3rVsKT3H2j7Sj+rJ4RceLUlS6Y+A==:1000:3w4jtF3awNF+UNeSSy7Ha918mL7NJGC+vMh60lw/YORQWPUnmhzYK7GXzXP9xUM0n73oQEmvjK1oKTwL8Y4eCKy1ut2i4K7wZdqVWHmSH62vSn6xK080cO6++0AVNA1Ti/mgzqCYrildo+QRdico/dkU7F+cVyQVQxv9DbcY5PVMNL7v6JAHL43+6Yr0a4VK3mJsJFc4suF9kTa8GZRZTelgwVAO2vkBl+tsjyJcTENXBZWdDDXIxmYe/FbH0TO6RiLPRgoZf6x0nAb/CWZjaQ==; _pxde=6b1c1d8e0736f7489d8ba26072b05c3fb65c3c43e10a9cd3d119abf7b6225cc6:eyJ0aW1lc3RhbXAiOjE3MDA0OTkyNjExMDd9',
        'dnt': '1',
        'origin': 'https://www.chegg.com',
        'referer': 'https://www.chegg.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"Response Status : {response.status_code}")
        if(response.status_code==200):
            data = json.loads(response.text)
            question_body = data['data']['questionByUuid']['content']['body']
            question_tran = data['data']['questionByUuid']['content']['transcribedData']
            return [question_body,question_tran]
        else:
            return None
    except Exception as e:
        print(f"Error:{e}")    

def getProblemID(urlchegg):
    try:
        pattern = r'chapter-(.*)-problem-(.*)-solution-(.*)'
        matches = re.findall(pattern, urlchegg)
        isbn13 = matches[0][2]
        print(matches[0][2])
        
        url = "https://gateway.chegg.com/study-bff-web/graphql"

        payload = json.dumps({"operationName":"tbsProblemDetailsSignedOut","variables":{"isbn13":isbn13,"chapterName":matches[0][0].upper(),"problemName":matches[0][1].upper()},"query":"query tbsProblemDetailsSignedOut($isbn13: String, $chapterName: String, $problemName: String) {\n  textbook_solution(isbn13: $isbn13) {\n    isbn13\n    isbn10\n    editionName\n    editionNumber\n    editionNumberOrdinal\n    tbsOrganicUrl\n    solutionManualSM3Url\n    book {\n      title\n      languageId\n      __typename\n    }\n    bookAuthor {\n      name\n      url\n      __typename\n    }\n    alternateISBNDetails {\n      isPrimary\n      secondaryIsbn13s\n      primaryBookTitle\n      primaryBookEdition\n      primaryBookURL\n      bookURL\n      __typename\n    }\n    subjectData {\n      subjectData {\n        id\n        name\n        __typename\n      }\n      subSubjectData {\n        id\n        name\n        __typename\n      }\n      parentSubjectData {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    pdpUrl\n    coverImageURL {\n      coverImageLargeURL\n      __typename\n    }\n    solutionCount {\n      totalSolutionCount\n      __typename\n    }\n    chapter(chapterName: $chapterName) {\n      problems(problemName: $problemName, chapterName: $chapterName) {\n        problemHtml\n        canonicalUrl\n        problemOrganicUrl\n        hasSolution\n        problemBreadCrumb {\n          name\n          url\n          label\n          __typename\n        }\n        problemName\n        problemId\n        __typename\n      }\n      __typename\n    }\n    TOC: chapter {\n      chapterId\n      chapterOrganicUrl\n      chapterName\n      problems(chapterName: $chapterName) {\n        problemName\n        problemOrganicUrl\n        problemId\n        __typename\n      }\n      __typename\n    }\n    bookmarkData {\n      id\n      __typename\n    }\n    __typename\n  }\n}\n"})
        headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'CVID=9eddd9da-79c1-4c67-989d-6101c6fb6006; CSID=1712077263890; pxcts=9884e25b-f112-11ee-a684-53e253468241; _pxvid=9884d0f6-f112-11ee-a684-73f04791e533; V=de33e069b11168251328ebe543b1737d660c39d3aa7ef8.44251717; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Apr+02+2024+22%3A31%3A16+GMT%2B0530+(India+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=6e9011d2-fea4-4e10-8e5c-a6175187ca23&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.chegg.com%2Fhomework-help%2Fsequential-version-simulation-takes-90-min-compute-10-000-it-chapter-6-problem-5qe-solution-9780124201583-exc&groups=fnc%3A0%2Csnc%3A1%2Ctrg%3A0%2Cprf%3A0; hwh_order_ref=/homework-help/sequential-version-simulation-takes-90-min-compute-10-000-it-chapter-6-problem-5qe-solution-9780124201583-exc; _px3=9c2341009d76c94f56e7bcba6b73c5168f7eecf9eddd5d0fc451bc32d24cb9ab:vjS7FZ4TDVwRZFcfssqWppNuyTTiETu2ex2OfTJMHLR5Ayt/nxawcXopvf8kRur+wZYxangmJmn9f91pnnDxcg==:1000:GJ1248KQnWM2TPNimHwlIR4+pGfyi3LB5ho8u9f352U1EJZVZLdu34T1FE3UA33iXmqkfASgoTMGCcCrH/Pfv7TWUp+3KmCcFqm+Vqm6KwkGF0flnoptm4erhHwBXdTtCdJ6HQgvdeOuPaMPR4XpDDrg77jkU0Tjs4/csWdlFdcd3Fv4MKlnVTtbgbS2t8T1CGiy4J2rb/6X2bnr8zLgVN7RUfju35W/b1iwLj6YPRE=; _px=vjS7FZ4TDVwRZFcfssqWppNuyTTiETu2ex2OfTJMHLR5Ayt/nxawcXopvf8kRur+wZYxangmJmn9f91pnnDxcg==:1000:ccM81WZ4O+NzEHmNj1+eA920C+boewk8Qx+TmuiPuKDuVdukQgqTzfJFxhcuq6/3AI/0KQBU7xUpqJLJMdKAfbrwQqCD/yeM1W7jVkTslg4ce/dnCM0i7WCg9wKjnggRGo7kb0yyWvTkH2vrHVyatV6logZQPHlMMturL2NgWhW07OtP8zmvF2cvaGcqIv/QlMyzyV0j6gJaiqircHQcl73HNO0fdZBb41qe1HA66XZ8XgA097xeUh8UoQ8BK/98fnbe4Gn7EZfQw2MnPiB6/A==; _pxde=405e86f7846eef468026844863cceb6226b7f2fe2ea4a6c37f600cb38e3ff5ea:eyJ0aW1lc3RhbXAiOjE3MTIwNzc3NTcyNTF9',
        'dnt': '1',
        'origin': 'https://www.chegg.com',
        'referer': 'https://www.chegg.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"Response Status : {response.status_code}")
        if(response.status_code==200):
            data = json.loads(response.text)
            chapter = data['data']['textbook_solution']['chapter']
            question_html = chapter[0]['problems'][0]['problemHtml']
            problem_id = None
            for x in chapter:
                for problem_name in x['problems']:
                    if problem_name['problemName'] == matches[0][1].upper():
                        problem_id = problem_name['problemId']
                        break
            isbn13 = data['data']['textbook_solution']['isbn13']
            return [problem_id, isbn13, question_html]
        else:
            return[None,None,None]
    except Exception as e:
        print(f"Error:{e}")

def textbookrating(contentId):
    try:
        jsonPosttbslike = {
            "operationName": "AllReviews",
            "variables": {
                "reviewForContentQueryArguments": {
                    "contentId": contentId,
                    "contentReviewType": "LIKE_DISLIKE",
                    "contentType": "SOLUTION"
                }
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "e34176a12c96329dc705bdd05c1b6e3a65bd819be9be754f99ca806524acf6f8"
                }
            }
        }

        headers = {
            'authority': 'gateway.chegg.com',
            'accept': '*/*',
            'accept-language': 'ar',
            'apollographql-client-name': 'chegg-web',
            'apollographql-client-version': 'main-61879f0a-5319065108',
            'authorization': 'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
            'content-type': 'application/json',
            'cookie': 'id_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im11c3RrZWVtb2ZmaWNpYWxAZ21haWwuY29tIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsImF1ZCI6IkNIR0ciLCJpYXQiOjE3MDE4NjUzODksImV4cCI6MTcxNzQxNzM4OSwic3ViIjoiNzdkZGU2ZDgtZGIwYi00YzkwLTgyMzUtMzk1YzFlYmU0Yzg3IiwicmVwYWNrZXJfaWQiOiJhcHciLCJjdHlwIjoiaWQiLCJpZHNpZCI6Ijc1ZTJkM2JiIiwiaWRzdCI6MTcwMTg2NTM4OTM1MSwiaWRzZyI6InBhc3N3b3JkIn0.QRqSGtZ5OE2A_ImxXJ_T7K-FmX4J_egIMOBCLKMASlhQX7hdrPqQcUZrs4AdtqvnyR3yHlNKq1TJmy2JGRq7zLoYJamZmvZJQ5Ymz5lSXzHP67VuvyR0deTkx0CvvDDVQ25Z9prQq3OLvqDnWLTmFE3lsDgjvlQgcBjv-rCiJaoxRpdLUUJ5DZvisOmU2uTVQ_gZJ4ljN6noJBxvnREkGvt4qxrufF_dS5kzQMyFCRFSVHF7F-kDhzSE6Plc5bVXZ2vsaQwipF26c1FOSNwmvbBDGp6zQABt0aExqS0y50mQIXuAdMJjW-I1ThzMkzTeJexRmiB-GiI-FdOTLBaXew',
            'dnt': '1',
            'origin': 'https://www.chegg.com',
            'referer': 'https://www.chegg.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

        try:
            response = requests.post('https://gateway.chegg.com/one-graph/graphql', json=jsonPosttbslike, headers=headers)
            response.raise_for_status()
            data = json.loads(response.text)

            like = data['data']['reviewForContent'][0]['count'] if 'count' in data['data']['reviewForContent'][0] else 0
            dislike = data['data']['reviewForContent'][1]['count'] if 'count' in data['data']['reviewForContent'][1] else 0

        except requests.exceptions.RequestException as e:
            print('Error:', e)
            like = 0
            dislike = 0

        return [like, dislike]
    except Exception as e:
        print(f"Error:{e}")


def textbookanswer(urls):
    try:
        json_file_path = "cookieschegg.json"
        cookies = get_random_cookie(json_file_path)
        validCookie = check_and_update_cookie(cookies, json_file_path)
        allnumber = getProblemID(urls)  # Assuming getProblemID is already defined

        jsonPosttbs = {
            "operationName": "SolutionContent",
            "variables": {
                "ean": allnumber[1],
                "problemId": allnumber[0]
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "0322a443504ba5d0db5e19b8d61c620d5cab59c99f91368c74dcffdbea3e502f"
                }
            }
        }

        headers = {
            'authority': 'gateway.chegg.com',
            'accept': '*/*, application/json',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6',
            'apollographql-client-name': 'chegg-web',
            'apollographql-client-version': 'main-61879f0a-5319065108',
            'authorization': 'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
            'content-type': 'application/json',
            'cookie': validCookie,
            'origin': 'https://www.chegg.com',
            'referer': 'https://www.chegg.com/',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }

        response = requests.post('https://gateway.chegg.com/one-graph/graphql', json=jsonPosttbs, headers=headers)
        data = response.text
        return data
    except Exception as e:
        print(f"Error:{e}")

# START
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  try:
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    profile_link = f'<a href="https://t.me/{username}">{first_name}</a>'
    reply_message = f"✨✨Welcome {profile_link}! to VIP Get Answer Bot✨✨\nWe provide Unsolved solutions!"
    reply_message4 ='''YOUR CHEGG ANSWER CODE HERE'''
    bot.send_message(message.chat.id, reply_message, parse_mode='HTML')
    bot.send_message(message.chat.id, reply_message4, parse_mode='HTML')
    bot.send_message(
        -1001636291714,
        f"✅Status: Ok\nQuestion: {message.text}\nUser Id: {user_id}\nProfile Link: {profile_link}",
        parse_mode='HTML')
  except Exception as e:
    print(f"Error: {e}")
    logging.exception(f"Error on {user_id}: {e}")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        user = message.from_user.first_name
        text = re.findall(r'https?://\S+', message.text)
        match1 = re.search(r'-?q(\d+)', text)
        match2 = re.search(r'q(\d+)$', text)
        match3 = re.search(r'-q(\d+)', text)

        if match1 or match2 or match3:
            idQ = match1.group(1) if match1 else match2.group(1) if match2 else match3.group(1)
            # print("Question ID:", idQ)
            responsecurl = answerresponse(idQ)
            response = responsecurl
            '''
            For Full Code Conatct @spacenx1 in telegram it premium & fulll support version
            '''
        else:
            print("no chegg link")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
  try:
    print("\033[92mBot is online!")
    bot.send_message(-1001636291714, f"Bot is online!") 
    bot.polling(none_stop=True)
  except Exception as e:
    print(f"Error: {e}")
    logging.error(f"Error: {e}")    

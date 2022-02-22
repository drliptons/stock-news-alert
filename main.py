import requests
from twilio.rest import Client
import discord
import time

DISCORD_WEBHOOK_STOCK = "ADD_WEBHOOK_HERE"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "ADD_STOCK_API_KEY_HERE"
NEWS_API = "ADD_NEWS_API_HERE"
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_VIRTUAL_NUMBER = ""
TWILIO_SEND_TO = ""

# SET MESSANGER HERE
SEND_MSG_TO = 0  # 0 = Discord, 1 = Twilio


# --------------------------- SEND MSG ---------------------------------
def send_msg_to_discord(articles_to_send):
    for article in articles_to_send:
        discord.send_msg(DISCORD_WEBHOOK_STOCK, article)
        time.sleep(2)
    print("Send Msg Complete")


def send_msg_to_twilio(articles_to_send):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in articles_to_send:
        message = client.messages.create(
            body=article,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_SEND_TO,
        )
    print("Send Msg Complete")


# --------------------------- CORE -----------------------------
# See alphavantage api doc: https://www.alphavantage.co/documentation/#daily

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
print(difference)

diff_percent = round(difference / float(yesterday_closing_price) * 100, 2)
print(f"diff_percent: {diff_percent}| abs(diff_percent): {abs(diff_percent)}")

if abs(diff_percent) > 3:
    # See news api doc: https://newsapi.org/docs/endpoints
    news_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)

    formatted_article = [f"{STOCK_NAME}: {up_down}{diff_percent}% \nHeadLine: {article['title']}. \nBrief: " \
                         f"{article['description']} \nMore: {article['url']}" for article in three_articles]

    # chose to send msg to
    if SEND_MSG_TO == 0:
        send_msg_to_discord(formatted_article)
    elif SEND_MSG_TO == 1:
        send_msg_to_twilio(formatted_article)
    else:
        print("ERROR SEND MSG")

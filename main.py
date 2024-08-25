import requests
import datetime as dt
from twilio.rest import Client


# STOCK = "ADANIENT.BSE"
# COMPANY_NAME = "ADANI ENTERPRISES"
STOCK = "TSLA"
COMPANY_NAME = "TESLA INC"
APLHA_API_KEY = "USE_A_API"
NEWS_API= "MY_NEWS_API"
auth_token = "A_TOKEN"
account_sid = "SID_TO_USE"
twilio_phone = "+PHONE"


#Variables
today = dt.datetime.today().astimezone().date()
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# res = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={APLHA_API_KEY}")
res = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={APLHA_API_KEY}")

data = res.json()["Time Series (Daily)"]
data_list = [value for (key,value)  in data.items()]
yesterday_data = data_list[0]
yesterday_cls = float(yesterday_data["4. close"])
print(yesterday_cls)
day_before_yesterday = data_list[1]
day_before_yesterday_cls = float(day_before_yesterday["4. close"])
up_down = None
if yesterday_cls-day_before_yesterday_cls < 0:
    up_down = "🔻"
else:
    up_down = "▲"

change = abs(((yesterday_cls - day_before_yesterday_cls)/day_before_yesterday_cls)*100)
print(change)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_param= {
    "apiKey":NEWS_API,
    "q": COMPANY_NAME,
}
get_news = requests.get(url="https://newsapi.org/v2/everything", params=news_param)
full_news_data = get_news.json()["articles"]
news_data = full_news_data[:3]
print(news_data)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.f
formatted_data = [f"{STOCK}: {up_down}{change}\nHeadlines:{article['title']}  \nBrief:{article['description']}" for article in news_data]

client = Client(account_sid, auth_token)
for article in formatted_data:
    message = client.messages \
        .create(
        body=article,
        from_=twilio_phone,
        to='+916266023624'
    )

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
# Can be done easily of the twilio

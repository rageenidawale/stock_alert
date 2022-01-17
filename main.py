import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
FROM_NUMBER = ""
TO_NUMBER = ""

stock_api_key = ""
news_api_key = ""
account_sid = ""
auth_token = ""

# required for twilio to work
client = Client(account_sid, auth_token)

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "apikey": stock_api_key
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()

# get stock data from the api
stock_data = response.json()

# get closing rates of yesterday and day before yesterday
last_exchange = stock_data["Meta Data"]["3. Last Refreshed"]
last_exchange = last_exchange.split("-")
last_exchange_date = f"{last_exchange[0]}-{last_exchange[1]}-{last_exchange[2]}"
last_to_last_exchange_date = f"{last_exchange[0]}-{last_exchange[1]}-{int(last_exchange[2]) - 1}"

stock_price = float(stock_data["Time Series (Daily)"][f"{last_exchange_date}"]["4. close"])
previous_stock_price = float(stock_data["Time Series (Daily)"][f"{last_to_last_exchange_date}"]["4. close"])

# find the difference and percentage and see if the price went up or down
difference = previous_stock_price - stock_price
arrow = "🔺" if difference >= 0 else "🔻"
percentage = abs(round(difference / stock_price))

# check if there is a huge difference and if yes send a message
if percentage < -5 or percentage > 5:
    news_parameters = {
        "apiKey": news_api_key,
        "qInTitle": COMPANY_NAME,
        "language": "en",
        "from": last_to_last_exchange_date,
        "to": last_exchange_date,
        "sortBy": "relevancy"
    }

    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    response.raise_for_status()

    # get news articles to send
    news_articles = response.json()["articles"]

    # check if there are news articles for that date and make sure the list is not empty
    if news_articles:
        # split the news articles in a list called articles
        articles = news_articles[:len(news_articles)]

        # format the articles according to the message
        formatted_articles = [f"Headline: {article['title']}, \nBrief: {article['description']}" for article in
                              articles]

        # iterate through the list to send one article at a time
        for article in formatted_articles:
            message = client.messages \
                .create(
                body=f"{STOCK_NAME}: {arrow}{percentage}% \n{article}",
                from_=FROM_NUMBER,
                to=TO_NUMBER
            )

            print(message.status)
    else:
        # if the articles list is empty, only send the percentage
        message = client.messages \
            .create(
            body=f"{STOCK_NAME}: {arrow}{percentage}% \n No related news found.",
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )

        print(message.status)

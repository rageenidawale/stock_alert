# 📈 Stock Price & News Alert App 📊  

A Python-based **stock price tracker** that sends an **SMS alert** via Twilio when a significant stock price change occurs. If the price moves more than **±5%**, the app also fetches related news articles from the **NewsAPI**.

---

## ✨ Features  
- Fetches **daily stock data** using Alpha Vantage API.  
- Tracks stock price changes of **Tesla Inc (TSLA)** (modifiable).  
- Sends **Twilio SMS alerts** for stock price movements **above 5% or below -5%**.  
- Fetches **relevant news articles** about the company when major price changes occur.  

---

## 🛠 Setup Instructions  

### 1️⃣ Install Dependencies  

Ensure Python is installed, then install the required libraries:  

```bash
pip install requests twilio
```

---

### 2️⃣ Get API Keys  

- Sign up for **[Alpha Vantage](https://www.alphavantage.co/)** and get a free **stock API key**.  
- Sign up for **[NewsAPI](https://newsapi.org/)** and get a **news API key**.  
- Create a **[Twilio](https://www.twilio.com/)** account and get:  
  - `ACCOUNT_SID`  
  - `AUTH_TOKEN`  
  - `FROM_NUMBER` (Twilio phone number)  

---

### 3️⃣ Configure API Keys  

In `main.py`, replace the placeholders with your credentials:  

```python
stock_api_key = "your_alpha_vantage_api_key"
news_api_key = "your_newsapi_key"
account_sid = "your_twilio_account_sid"
auth_token = "your_twilio_auth_token"
FROM_NUMBER = "your_twilio_phone_number"
TO_NUMBER = "your_phone_number"
```

You can also modify the stock and company name:  

```python
STOCK_NAME = "TSLA"  # Change this to any stock symbol
COMPANY_NAME = "Tesla Inc"  # Change this to the relevant company name
```

---

### 4️⃣ Run the Application  

Execute the script:  

```bash
python main.py
```

If the stock price moves **more than 5%**, you'll receive an **SMS alert with the stock change and latest news**.

---

## 📜 How It Works  

1. Fetches **daily stock data** from **Alpha Vantage API**.  
2. Calculates the **percentage difference** in closing prices of the last two days.  
3. If the change is **>5% or <-5%**, fetches **latest news articles** from **NewsAPI**.  
4. Sends an **SMS alert via Twilio** with stock movement and news.  

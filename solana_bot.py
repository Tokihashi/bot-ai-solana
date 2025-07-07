
import requests
import time
import openai
from telegram import Bot

TELEGRAM_TOKEN = "8033446361:AAHKFByJgP05OYxBM4m2ZSHlpQcDyDQFBWs"
OPENAI_API_KEY = "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"
CHAT_ID = "@deadshxgxn"

SOLANA_ENDPOINT = "https://api.dexscreener.com/latest/dex/pairs/solana"
openai.api_key = OPENAI_API_KEY
bot = Bot(token=TELEGRAM_TOKEN)

def generate_ai_comment(token_data):
    prompt = f"""
    Монета: {token_data['baseToken']['symbol']}
    Цена: {token_data['priceUsd']}$ 
    Объём: {token_data['volume']['h1']} за 1 час
    Рост за 1ч: {token_data['priceChange']['h1']}%
    Ликвидность: {token_data['liquidity']['usd']}$

    Заключение: стоит ли входить? Почему сигнал был выдан? Когда выходить?
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            { "role": "system", "content": "Ты крипто-аналитик. Комментируй сигналы понятно и по существу." },
            { "role": "user", "content": prompt }
        ]
    )
    return response.choices[0].message["content"]

def check_solana_pairs():
    response = requests.get(SOLANA_ENDPOINT)
    if response.status_code != 200:
        return

    data = response.json()
    for pair in data.get("pairs", []):
        try:
            price_change = float(pair["priceChange"]["h1"])
            volume = float(pair["volume"]["h1"])
            if price_change > 50 and volume > 10000:
                comment = generate_ai_comment(pair)
                message = (
                    f"💥 Сигнал по монете {pair['baseToken']['symbol']}\n"
                    f"Цена: {pair['priceUsd']}$\n"
                    f"Объём (1ч): {volume}$\n"
                    f"Рост (1ч): {price_change}%\n\n"
                    f"🧠 AI-комментарий:\n{comment}"
                )
                bot.send_message(chat_id=CHAT_ID, text=message)
        except:
            continue

while True:
    check_solana_pairs()
    time.sleep(60 * 5)

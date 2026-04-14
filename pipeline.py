import duckdb
import json
import requests
import os
from google import genai
from datetime import datetime

# Keys
FIRECRAWL_KEY = 'fc-072618b7a6cb420f89fb85d905a01ffd'
GEMINI_KEY = 'AIzaSyDi8TMBmvE7w5qcjZarjqK8CTX8q1pZR5g'

client = genai.Client(api_key=GEMINI_KEY)

def run_pipeline():
    # 1. Scrape
    endpoint = "https://api.firecrawl.dev/v1/scrape"
    headers = {"Authorization": f"Bearer {FIRECRAWL_KEY}"}
    payload = {"url": "https://www.google.com/finance/markets/most-active", "formats": ["markdown"]}
    
    response = requests.post(endpoint, headers=headers, json=payload)
    markdown_text = response.json().get("data", {}).get("markdown", "")

    # 2. Transform
    prompt = f"Extract most active stocks as JSON list: ticker, name, price, change. Return ONLY JSON. TEXT: {markdown_text[:5000]}"
    ai_response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    
    clean_json = ai_response.text.strip().replace("```json", "").replace("```", "")
    data = json.loads(clean_json)

    # 3. Load & Clean
    db = duckdb.connect('market_data.db')
    db.execute("DROP TABLE IF EXISTS prices")
    db.execute("CREATE TABLE prices (ticker TEXT, name TEXT, price DOUBLE, change TEXT, updated_at TEXT)")
    
    now = datetime.now().strftime("%H:%M:%S")
    
    for item in data:
        # Clean the price string (remove $, commas, etc.)
        raw_price = str(item.get('price', '0')).replace('$', '').replace(',', '').strip()
        try:
            clean_price = float(raw_price)
        except:
            clean_price = 0.0
            
        db.execute("INSERT INTO prices VALUES (?, ?, ?, ?, ?)", 
                   [item.get('ticker'), item.get('name'), clean_price, item.get('change'), now])
    db.close()

if __name__ == "__main__":
    run_pipeline()
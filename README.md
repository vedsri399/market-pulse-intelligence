# 🏛️ Market Pulse Intelligence
**Building a web tracker that doesn't break every Tuesday.**

## Why I built this
If you’ve ever maintained a web scraper, you know the "maintenance loop." You write the perfect script, the target website shifts a single CSS class, and suddenly your pipeline is dead. 

I wanted to see if I could use LLMs to build something **resilient**. This project uses **Gemini 2.5 Flash** to "read" the page content like a human would. It doesn’t care about the underlying HTML structure; it just looks for the data it knows should be there.

## How it works (The Simple Version)
1. **The Scrape:** Firecrawl grabs the raw markdown from Google Finance.
2. **The Brain:** Gemini 2.5 Flash extracts the Tickers, Prices, and Trends into clean JSON.
3. **The Storage:** Everything flows into **DuckDB** every few seconds.
4. **The View:** A **Streamlit** dashboard shows the live feed without ever flickering or refreshing the whole page.

## The Tech I Used
* **Python** (The glue holding it all together)
* **Gemini 2.5 Flash** (The extraction engine)
* **DuckDB** (For lightning-fast local data snapshots)
* **Streamlit** (To make the data look good in real-time)

## Challenges I Solved
* **Data Cleaning:** Real-world stock data is messy. I built a sanitization layer to strip out currency symbols and commas so the math stays accurate.
* **UI Flow:** I used fragmented updates in Streamlit so the results "flow" into the dashboard smoothly rather than the screen going blank every time

## 🔧 Getting Started
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/vedsri399/market-pulse-intelligence.git](https://github.com/vedsri399/market-pulse-intelligence.git)

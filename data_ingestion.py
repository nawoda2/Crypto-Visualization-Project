import os
import psycopg2
import requests

def fetch_coingecko_market_data(api_key=None, pages=1):
    """
    Fetch market data for multiple pages from the CoinGecko API and store in Postgres.
    """

    url = "https://api.coingecko.com/api/v3/coins/markets"

    # If CoinGecko Pro API key is needed (paid plan), it might look like this:
    # headers = {"x_cg_pro_api_key": api_key} if api_key else {}
    # Otherwise, if you don't need a key:
    headers = {}

    # Connect to Postgres. Adjust host/user/password as needed.
    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    cursor = conn.cursor()

    # Create table if it doesn’t exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_data (
            id SERIAL PRIMARY KEY,
            coin_id VARCHAR(50),
            symbol VARCHAR(50),
            name VARCHAR(100),
            current_price NUMERIC,
            market_cap NUMERIC,
            total_volume NUMERIC,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Loop over pages
    for page in range(1, pages + 1):
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "sparkline": "false",
            "per_page": 250,
            "page": page
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}, status code: {response.status_code}")
            continue

        data = response.json()

        # Insert each coin’s data into the table
        for coin in data:
            coin_id = coin.get("id")
            symbol = coin.get("symbol")
            name = coin.get("name")
            current_price = coin.get("current_price")
            market_cap = coin.get("market_cap")
            total_volume = coin.get("total_volume")

            cursor.execute("""
                INSERT INTO crypto_data (coin_id, symbol, name, current_price, market_cap, total_volume)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (coin_id, symbol, name, current_price, market_cap, total_volume))

        conn.commit()  # Commit after each page

    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Fetch API key from environment if you have a Pro plan
    api_key = os.environ.get("COINGECKO_API_KEY")  
    # Example: fetch 5 pages (5 * 250 = 1250 coins, if that many exist)
    fetch_coingecko_market_data(api_key=api_key, pages=5)

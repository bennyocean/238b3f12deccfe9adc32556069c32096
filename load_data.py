import os                                                                                                                                                                                                          
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import yfinance as yf
from dune_client.client import DuneClient

# Define relative paths
base_dir = Path(__file__).resolve().parent  
env_path = base_dir / ".env"
data_dir = base_dir / "data"

# Load environment variables
load_dotenv(env_path)
api_key = os.getenv("DUNE_API_KEY")


##############################
### Load Dune Data ###
##############################

# Initialize DuneClient
dune = DuneClient(api_key)

# Dune Query IDs for daily transaction volumes on DEXs in 2024
dune_query_ids_dex = [
    {"token": "USDT", "query_id": 4584748},
    {"token": "USDC", "query_id": 4584862},
    {"token": "UNI", "query_id": 4584868},
    {"token": "POL", "query_id": 4584876},
]

# Fetch and save transaction volumes and trade counts for each token
for entry in dune_query_ids_dex:
    token = entry["token"]
    query_id = entry["query_id"]

    # Fetch data from Dune
    query_result = dune.get_latest_result(query_id)
    rows = query_result.result.rows
    df = pd.DataFrame(rows)

    # Ensure the 'day' column is in datetime format and set it as the index
    df['day'] = pd.to_datetime(df['day'], format='%Y-%m-%d %H:%M:%S.%f %Z', utc=True).dt.date

    csv_path = data_dir / f"on-chain/{token.lower()}_dex_volumes_2024.csv"
    df.to_csv(csv_path, index=False)

    print(f"Data for {token} saved to {csv_path}")


##############################
### Load Ethereum Gas Fees ###
##############################

gas_fee_query_id = 4585679

# Fetch and save Ethereum gas fees
query_result_gas_fee = dune.get_latest_result(gas_fee_query_id)
rows_gas_fee = query_result_gas_fee.result.rows
gas_fee_df = pd.DataFrame(rows_gas_fee)

# Ensure the 'day' column is in datetime format and set it as the index
gas_fee_df['day'] = pd.to_datetime(gas_fee_df['day'], format='%Y-%m-%d %H:%M:%S.%f %Z', utc=True).dt.date

gas_fee_csv_path = data_dir / "on-chain/eth_gas_fees_2024.csv"
gas_fee_df.to_csv(gas_fee_csv_path, index=False)

print(f"Gas fee data saved to {gas_fee_csv_path}")


##############################
### Load BTC and ETH Prices ###
##############################

crypto_tickers = {
    "ETH-USD": "eth_prices.csv",
    "BTC-USD": "btc_prices.csv"
}

for ticker, filename in crypto_tickers.items():
    data = yf.download(ticker, start="2024-01-01", end="2025-01-01", progress=False)
    data = data[['Close']].rename(columns={'Close': 'price'})
    data.reset_index(inplace=True)

    # Drop any remaining column levels (e.g., ticker name like BTC-USD)
    if isinstance(data.columns, pd.MultiIndex):  # Check for MultiIndex
        data.columns = data.columns.get_level_values(0)  # Use only the first level

    file_path = data_dir / f"off-chain/{filename}"
    data.to_csv(file_path, index=False)
    print(f"Saved {ticker} data to {file_path}.")
import os
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

import requests
from datetime import datetime

def get_token_price(symbol: str) -> dict:
    """
    使用 symbol 获取价格时，先映射为 coingecko id。
    """
    id_map = {
        "ETH": "ethereum",
        "SOL": "solana",
        "BTC": "bitcoin",
        "USDC": "usd-coin",
        # 如有其他常用代币，可继续补充
    }
    coin_id = id_map.get(symbol.upper(), symbol.lower())
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin_id, "vs_currencies": "usd"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    price = data.get(coin_id, {}).get("usd")
    return {
        "symbol": symbol.upper(),
        "price_usd": price,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

import os
import json
import openai
from tool import get_token_price

# 加载 OpenAI API Key（前提是环境变量已设置）
openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = (
    "You are PriceAgent. For ANY question about token prices, "
    "you MUST call get_token_price and provide the returned real-time USD price. "
    "Do NOT answer from memory or fallback."
)

functions = [{
    "name": "get_token_price",
    "description": "Fetch current USD price of a crypto token by symbol",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "Token symbol, e.g., ETH or SOL"}
        },
        "required": ["symbol"]
    }
}]

def call_agent(user_query: str) -> str:
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        functions=functions,
        function_call="auto"
    )
    choice = resp.choices[0]
    msg = choice.message
    fc = getattr(msg, "function_call", None)

    # 调试输出
    print("🔍 finish_reason:", choice.finish_reason)
    print("🔍 function_call:", fc)

    if fc:
        args = json.loads(fc.arguments)
        result = get_token_price(args["symbol"])
        if result["price_usd"] is None:
            return f"⚠️ 无法获取 {result['symbol']} 的当前价格，请确认 symbol 是否正确。"
        return f"✅ {result['symbol']} 当前价格为 ${result['price_usd']:.2f}，时间戳：{result['timestamp']}"
    else:
        return "⚠️ PriceAgent 未调用函数，可能未识别为价格查询。"

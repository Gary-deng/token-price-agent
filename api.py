from fastapi import FastAPI
from agent import call_agent

app = FastAPI()

@app.post("/price")
def price_endpoint(body: QueryBody):
    return {"query": body.query, "answer": call_agent(body.query)}

# 可选：本地开发
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

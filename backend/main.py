import uvicorn
from fastapi import FastAPI
#import postgres package
import psycopg2
app = FastAPI(debug=True)

@app.get('/status')
async def check_status():
    return "Hello World"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
import uvicorn
from fastapi import FastAPI
#import postgres package
import psycopg2
from routers import post_get_photo
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/status')
def check_status():
    return {"Hello: World"}


app.include_router(post_get_photo.router)

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
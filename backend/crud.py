from fastapi import APIRouter, UploadFile, File
from models import PhotoModel
from typing import List
# from s3bucket import 


router = APIRouter()

@app.get("/photos", response_model=List[PhotoModel])
async def get_all_photos():
    # connect to database
    conn = psycopg2.connect(
        database="mydb", user='docker', password='docker', host="0.0.0.0"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM photo ORDER BY id DESC")
    rows = cur.fetchall()

    formatted_photo = []
    for row in rows:
        formatted_photo.append(
            PhotoModel(
                id=row[0],
                photo_name=row[1],
                photo_url=row[2],
                is_deleted=row[3]

            )
        )
    cur.close()
    conn.close()
    return formatted_photo

@app.post("/photos", status_code=201)
async def add_photo(file: UploadFile):
    print("Create endpoint hit")
    print(file.filename)
    # store  upload file to aws s3

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.upload_file_obj(file.file, file.filename, ExtraArgs={'ACL': "public-read"})

    uploaded_file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"
    # store url to database

    conn = psycopg2.connect(
        database="mydb", user='docker', password='docker', host="0.0.0.0"
    )
    cur = conn.cursor()
    cur.execute(f"INSERT INTO photo (photo_name, photo_url) VALUES ('{file.filename}', '{uploaded_file_url}')")

    conn.commit()
    cur.close()
    conn.close()


from fastapi import APIRouter, UploadFile,status, HTTPException
from models import PhotoModel
from typing import List
import psycopg2
import boto3
from loguru import logger
from uuid import uuid4
import magic




router = APIRouter()




@router.get('/photos', response_model=List[PhotoModel])
async def get_all_photos():
    try:
        # connect to the database
        conn = psycopg2.connect(
               database="mydbphoto", user="docker", password="docker", host="localhost", port="5433"
        )
        # create cursor for the connection
        cur = conn.cursor()
        # execute query in descending order
        cur.execute("SELECT * FROM photo ORDER BY photo_name")
        rows = cur.fetchall()

        # create a return list by iterating over the rows in the database table
        formatted_photo = []
        for row in rows:
            # Add error handling to ensure the data is in the correct format
            try:
                photo_name = str(row[0])
                photo_url = str(row[1])

                # Check for None values before converting to the expected data types
                if photo_name is not None:
                    photo_name = str(photo_name)
                if photo_url is not None:
                    photo_url = str(photo_url)
            
                
                formatted_photo.append(
                    PhotoModel(
                        photo_name=photo_name,
                        photo_url=photo_url,
                    )
                )
            except (ValueError, TypeError) as e:
                # Handle invalid data in the database
                logger.error(f"Invalid data in the database: {str(e)}")
        cur.close()
        conn.close()
        return formatted_photo
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


KB = 1024
MB = 1024 * KB

SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}


# Configure AWS credentials
aws_access_key_id = '********************'
aws_secret_access_key = '******************'

# Specify the AWS region
aws_region = 'us-west-1'  # Replace with your desired region

# Create an S3 client
s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
S3_BUCKET_NAME = "photo-123-magda"
# s3 = boto3.resource('s3')
bucket = s3.Bucket(S3_BUCKET_NAME)

async def s3_upload(contents: bytes, key: str):
    logger.info(f'Uploading {key} to s3')
    bucket.put_object(Key=key, Body=contents)


@router.post('/upload', status_code=201)
async def add_photo(file: UploadFile):
    print("Create endpoint hit")
    print(file.filename)
    
    try:
        # Your existing code for /upload
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file found!"
            )
        contents = await file.read()
        size = len(contents)

        if not 0 < size <= 1 * MB:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Supported file size is 0 - 1 MB'
            )
        file_type = magic.from_buffer(buffer=contents, mime=True)
        if file_type not in SUPPORTED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Unsupported file type: {file_type}. Supported types are {SUPPORTED_FILE_TYPES}'
            )
        file_name = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'
        uploaded_file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"

        conn = psycopg2.connect(
            database="mydbphoto", user="docker", password="docker", host="localhost", port="5433"
            
        )
        cur = conn.cursor()
    #     photo_name: str
    # photo_url: str
        cur.execute(
        f"INSERT INTO photo (photo_name, photo_url) VALUES ('{file.filename}', '{uploaded_file_url}' )"
        )
        conn.commit()
        cur.close()
        conn.close()
        await s3_upload(contents=contents, key=file_name)
        return {'file_name': file_name}
    
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e  # Re-raise the exception for FastAPI to handle

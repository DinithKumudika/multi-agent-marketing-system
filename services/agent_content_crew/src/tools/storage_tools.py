import os
import io
from minio import Minio
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

# --- Tool 1: MinIO Upload Tool ---

class MinioUploadTool(BaseTool):
    name: str = "MinIO File Uploader"
    description: str = "Uploads text content to a specified MinIO bucket as a new object (file)."

    def _run(self, object_name: str, content: str) -> str:
        try:
            # Initialize MinIO client
            client = Minio(
                os.getenv("MINIO_ENDPOINT"),
                access_key=os.getenv("MINIO_ACCESS_KEY"),
                secret_key=os.getenv("MINIO_SECRET_KEY"),
                secure=False # Set to True if using HTTPS
            )
            
            bucket_name = os.getenv("MINIO_BUCKET_NAME")

            # Check if bucket exists
            found = client.bucket_exists(bucket_name)
            if not found:
                client.make_bucket(bucket_name)
                print(f"Bucket '{bucket_name}' did not exist. Created successfully.")
            else:
                print(f"Bucket '{bucket_name}' already exists.")

            # Convert string content to bytes
            content_bytes = content.encode('utf-8')
            content_stream = io.BytesIO(content_bytes)
            content_length = len(content_bytes)

            # Upload the object
            client.put_object(
                bucket_name,
                object_name,
                content_stream,
                content_length,
                content_type="text/markdown"
            )

            return f"Successfully uploaded '{object_name}' to bucket '{bucket_name}'."

        except Exception as e:
            return f"Error uploading to MinIO: {str(e)}"

# Instantiate the tool so it can be imported in YAML
minio_upload_tool = MinioUploadTool()
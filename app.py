# ==========================================================
# Create Group
# ==========================================================
# az group create --name storage-group --location westus2

# ==========================================================
# Create the storage account
# ==========================================================
# az storage account create -n mmosconii -g storage-group

# ==========================================================
# Get the blob service account url for the storage account
# ==========================================================
# az storage account show -n mmosconii -g storage-group --query "primaryEndpoints.blob"

# ==========================================================
# Get connection-string
# ==========================================================
# az storage account show-connection-string -n mmosconii -g storage-group | grep -o '"connectionString": "[^"]*' | grep -o '[^"]*$'

# ==========================================================
# Install Python Package
# ==========================================================
# pip install -r requirements.txt

import os
from azure.storage.blob import ContainerClient, BlobClient

from dotenv import load_dotenv
load_dotenv()

conn_str = os.getenv("CONNECTION_STRING")
container_name = "mycontainer"
blob_name = "SampleSource.txt"

# ==========================================================
# Create a container
# ==========================================================
container_client = ContainerClient.from_connection_string(conn_str=conn_str, container_name=container_name)
container_client.create_container()

# ==========================================================
# Upload File
# ==========================================================
blob = BlobClient.from_connection_string(conn_str=conn_str, container_name=container_name, blob_name='images/'+blob_name)

with open("./" + blob_name, "rb") as data:
  blob.upload_blob(data)

# ==========================================================
# List the blobs in container 
# ==========================================================
container = ContainerClient.from_connection_string(conn_str=conn_str, container_name=container_name)

blob_list = container.list_blobs()
for blob in blob_list:
  print(blob.name)

# ==========================================================
# Download a blob from container
# ==========================================================
blob = BlobClient.from_connection_string(conn_str=conn_str, container_name=container_name, blob_name='images/'+blob_name)
fileName, fileExtension = os.path.splitext(blob_name)

with open("./" + fileName + "-download" + fileExtension, "wb") as my_blob:
    blob_data = blob.download_blob()
    blob_data.readinto(my_blob)

# ==========================================================
# Delete blob
# ==========================================================
blob = BlobClient.from_connection_string(conn_str=conn_str, container_name=container_name, blob_name='images/'+blob_name)
blob.delete_blob()

# ==========================================================
# Delete container
# ==========================================================
container_client = ContainerClient.from_connection_string(conn_str=conn_str, container_name=container_name)
container_client.delete_container() 
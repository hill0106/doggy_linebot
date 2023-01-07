from azure.storage.blob import BlobServiceClient
import os

storage_key = "3t0d2MKVMQzcYMG3v8KLSSPYnMchGLz2Lxf5s5ySi+eCsSoFS+WHClaSlvkhF/CKpOSb3x0YPgih+ASt5V3Avw=="
storage_account_name = "1111ainutrition"
connection_string = "DefaultEndpointsProtocol=https;AccountName=1111ainutrition;AccountKey=/Z0+zkkW593yYmZmWidzwm6nrVk1lr2Re7+Xi6O/Jhfev32IUH/VxY/XqhgJaf9TT5kqAkPC2H+5+AStn8t1kA==;EndpointSuffix=core.windows.net"
container_name = "dog"

def uploadImage(path, filename):
    blob_name = filename
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container_name, blob=blob_name)
    with open(path, 'rb') as data:
        blob_client.upload_blob(data, overwrite = True)
    url = "https://" + storage_account_name + ".blob.core.windows.net/" + container_name + "/" + blob_name
    print("uploaded")
    os.remove(path)
    return url

def deleteImage(filename):
    try:
        blob_name = filename + '.jpeg'
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container_name, blob=blob_name)
        blob_client.delete_blob()
    except:
        return False
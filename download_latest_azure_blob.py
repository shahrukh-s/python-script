from azure.storage.blob import BlockBlobService
import zipfile
from datetime import datetime
import os
block_blob_service = BlockBlobService(account_name='ACCNAME', sas_token='SASTOKEN')
container_name = 'CONATINERNAME'
generator = block_blob_service.list_blobs(container_name,  prefix='PREFIXOFFILE')

y = sorted(generator, key=lambda x: x.properties.last_modified, reverse=True)

if y:
    blob = y[0]
    file = blob.name
    print('latest file name : ' +  file)
    head, tail = os.path.split("{}".format(blob.name))
    if (os.path.isdir(os.getcwd()+ "/" + head)):
        block_blob_service.get_blob_to_path(container_name, blob.name, os.getcwd()+ "/" + head + "/" + tail)
        print("file is downloading")
cwd = (os.getcwd())
d = (cwd + "\\" + blob.name)
zip_ref = zipfile.ZipFile(d, 'r')
target = (cwd + "\\" + "tempDir")
zip_ref.extractall(target)
zipout = (zip_ref.filename)
zip_ref.close()

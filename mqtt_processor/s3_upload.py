import boto3
import json
from botocore.exceptions import ClientError

# upload_to_s3("abc.png", 1)
def upload_to_s3(file_name, node_number):
    try:
        key_info_json = open("awsinfo.json").read()
    except FileNotFoundError:
        print("awsinfo.json is not exist in dir.")
        exit(-1)

    data=json.loads(key_info_json)

    s3 = boto3.client(
        's3',
        aws_access_key_id = data['accessKeyId'],
        aws_secret_access_key = data['secretAccessKey']
    )

    with open(file_name, "rb") as f:
        s3.upload_fileobj(f,"capstone12", str(node_number)+"/"+file_name,
            ExtraArgs={'ACL' : 'public-read-write'}
        )
    print("File Upload Complete to " + str(node_number) + "/" + file_name)
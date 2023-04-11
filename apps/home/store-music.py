from google.cloud import storage
import datetime


def store_music(file_path):
    #store music in google cloud storage
    # Set the name of your Google Cloud Storage bucket
    bucket_name = "ringledingle"

    # Set the path to the local file you want to upload
    file_path = "/apps/static/media/output.mp3"

    #make the name of the file the date and time:
    now = datetime.datetime.now()
    file_name = now.strftime("%Y-%m-%d-%H-%M-%S")

    # Set the destination name for the file in your bucket
    destination_blob_name = f"{file_name}.mp3"

    # GOOGLE_JSON = json.loads(os.getenv('GOOGLE_JSON'))
    # print('The Google Creds are found')
    client = storage.Client().from_service_account_file('apps/home/google.json')
    
    # Instantiate a client object
    # client = storage.Client()

    # Get a reference to the bucket
    bucket = client.bucket(bucket_name)

    # Create a blob object and upload the file
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

    # Print the URL of the uploaded file
    print(blob.public_url)





store_music('file_path')
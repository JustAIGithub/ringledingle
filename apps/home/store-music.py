from google.cloud import storage
from google.oauth2.credentials import Credentials
import json
import qrcode
import datetime
import os

def upload_file (filename='apps/static/media/output.mp3'):
    try:
        GOOGLE_JSON = json.loads(os.getenv('GOOGLE_JSON'))
        storage_client = storage.Client.from_service_account_info(GOOGLE_JSON)
        print('The Google Creds are found')
    except:
        storage_client = storage.Client.from_service_account_json('apps/home/google.json')
        print('The Google KEY environment variable is not set. Using google.json')

    # Create a bucket object for our bucket
    bucket = storage_client.get_bucket('ringledingle')

    # print timestamp to be used as filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # filename = 'apps/static/media/output.mp3'
    blob = bucket.blob(f'ringledingle{timestamp}.mp3')
    blob.upload_from_filename(filename)


def generate_qr_code(url):
    """Generates a QR code from a URL."""
    qr = qrcode.QRCode(version=None, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a file
    img.save("qr_code.png")
    print("QR code saved to qr_code.png.")

# Example usage:
generate_qr_code('https://www.google.com/maps')



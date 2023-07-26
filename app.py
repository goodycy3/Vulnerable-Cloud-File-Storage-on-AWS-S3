from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import boto3
import os

app = Flask(__name__)

# AWS S3 configuration
AWS_ACCESS_KEY_ID = 'AKIASUL6TUBYR5BLLX33'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 'my-d3m0-files'
S3_BASE_URL = f'https://my-d3m0-files.s3.us-east-1.amazonaws.com/'

# Configure AWS SDK
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Upload the file to S3
    try:
        s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
        flash('File successfully uploaded!')
    except Exception as e:
        flash('An error occurred while uploading the file: ' + str(e))

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_url = f"{S3_BASE_URL}{filename}"
        return redirect(file_url)
    except Exception as e:
        flash('An error occurred while downloading the file: ' + str(e))
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = '1IpAaADF8g9NZkJwAtmY0uwTZUFcKFLGieFzXUsI'  # Change this to a random secret key
    app.run(debug=True)

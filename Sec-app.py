from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import boto3
import botocore.exceptions

app = Flask(__name__)

# AWS S3 configuration
AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 'my-d3m0-files'
S3_BASE_URL = f'https://my-d3m0-files.s3.my-d3m0-files.amazonaws.com/'

# Configure AWS SDK using environment variables or IAM roles
s3 = boto3.client('s3', region_name=AWS_REGION)

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

    # File validation (example: limit to 10MB)
    if not allowed_file(file.filename):
        flash('Invalid file type')
        return redirect(request.url)
    if not allowed_file_size(file):
        flash('File size exceeds the limit (10MB)')
        return redirect(request.url)

    # Upload the file to S3
    try:
        s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
        flash('File successfully uploaded!')
    except botocore.exceptions.ClientError as e:
        flash('An error occurred while uploading the file')
        app.logger.error(str(e))
    except Exception as e:
        flash('An error occurred while uploading the file')
        app.logger.error(str(e))

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_url = f"{S3_BASE_URL}{filename}"
        return redirect(file_url)
    except Exception as e:
        flash('An error occurred while downloading the file')
        app.logger.error(str(e))
        return redirect(url_for('index'))
    
# Whitelist of allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'docx'}

def allowed_file_size(file):
    # 10 MB limit (10 * 1024 * 1024 bytes)
    return len(file.read()) <= 10485760

if __name__ == '__main__':
    app.secret_key = os.environ.get('AKIASUL6TUBYR5BLLX33', '1IpAaADF8g9NZkJwAtmY0uwTZUFcKFLGieFzXUsI')  # Use environment variable or a default value
    app.run(debug=True)

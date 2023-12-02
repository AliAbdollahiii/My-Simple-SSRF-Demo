from flask import Flask, request, send_file
import requests
from urllib.parse import urlparse
import random

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html>
        <head>
            <style>
                body {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }

                h1 {
                    font-size: 2em;
                    margin-bottom: 10px;
                }

                p {
                    font-size: 1.5em;
                    margin-bottom: 20px;
                }

                img {
                    max-width: 80%;
                    height: auto;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>My simple SSRF demo!</h1>
            <p>This page simulates a realistic scenario, allowing data retrieval from local files via SSRF.</p>
            <img src="/image" alt="SSRF Demo Graphic">
        </body>
    </html>
    """

def is_valid_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in {'http', 'https'}

@app.route('/ssrf')
def ssrf():
    url = request.args.get('url', '')
    if url and is_valid_url(url):
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return 'Please provide a valid URL parameter.'

@app.route('/image')
def display_image():
    # Assuming the image is located on your desktop
    image_path = "/home/kali/Desktop/MyPic1.png"
    return send_file(image_path, mimetype='image/png')

@app.route('/read_local_file')
def read_local_file():
    file_path = request.args.get('file_path', '')
    print(f"Attempting to read file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return f"File content:\n\n{content}"
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == '__main__':
    # Use a random port between 5000 and 9999
    port = random.randint(5000, 9999)
    app.run(host='127.0.0.1', port=port, debug=True)

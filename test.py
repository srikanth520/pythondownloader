import pytube
import os
import requests
from pytube import YouTube
from tqdm import tqdm
from flask import Flask,request


app=Flask(__name__)

# @app.route('/')
# def home():
#     return 'hello this is test application'

# @app.route('/youtubedownloader')
# def youtubedownloader():
#     return 'this is youtube download page'

# @app.route('/timeconverter')
# def timeconverter():
#     return 'time format converter'

# @app.route('/<name>')
# def features(name):
#     if name=='youtubedownloader':
#         return redirect(url_for('youtubedownloader'))
#     if name=='timeconverter':
#         return redirect(url_for('timeconverter'))

# @app.route('/')
# def mainpage():
#     return render_template('homepage.html')

@app.route('/', methods=['GET'])
def download():
    url = request.args.get('url')
    if url:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        # Determine the default downloads directory
        downloads_dir = os.path.expanduser('~')  # This gets the user's home directory
        default_downloads_path = os.path.join(downloads_dir, 'Downloads')  # Append 'Downloads' to the home directory path

        # Specify the output file path
        output_path = os.path.join(default_downloads_path, stream.default_filename)

        # Create a progress bar
        with requests.get(stream.url, stream=True) as response:
            file_size = int(response.headers.get('content-length', 0))
            progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Downloading {stream.default_filename}")

            with open(output_path, 'wb') as file:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    progress_bar.update(len(data))

        # Close the progress bar
        progress_bar.close()

        print(f"Video downloaded to: {output_path}")
        return f"Video downloaded successfully to {default_downloads_path}"

    else:
        return "Please enter a URL using the 'url' query parameter."

if __name__=='__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/')
def index():
    return 'Backend is working 👀'

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()

    video_url = data.get('url')
    format_type = data.get('format', 'mp4')
    quality = data.get('quality', 'best')

    if not video_url:
        return jsonify({'error': 'Missing video URL'}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': f'bestvideo[ext={format_type}][height<={quality}]+bestaudio/best',
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_url = info.get('url')  # Fallback if no formats found
            if 'requested_downloads' in info:
                direct_url = info['requested_downloads'][0]['url']
            
            return jsonify({'download_url': direct_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()

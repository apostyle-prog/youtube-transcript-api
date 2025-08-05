from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route('/')
def index():
    return 'YouTube Transcript API is running!'

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('videoId')
    lang = request.args.get('lang', 'en')

    if not video_id:
        return jsonify({"error": "Missing videoId"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        full_text = " ".join([item['text'] for item in transcript])
        return jsonify({"videoId": video_id, "text": full_text})
    except (TranscriptsDisabled, NoTranscriptFound):
        return jsonify({"error": "Transcript not available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

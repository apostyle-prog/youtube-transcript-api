from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

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
        api = YouTubeTranscriptApi()
        transcript_list = api.list_transcripts(video_id)

        transcript = transcript_list.find_transcript([lang])
        formatted = TextFormatter().format_transcript(transcript.fetch())

        return jsonify({
            "videoId": video_id,
            "text": formatted
        })

    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video."}), 404
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

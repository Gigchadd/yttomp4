import os
import re
import yt_dlp
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

# Function to clean filenames
def sanitize_filename(filename):
    return re.sub(r'[^\w\s.-]', '_', filename)

# Route to download YouTube video
@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            raw_filename = ydl.prepare_filename(info)
            filename = info.get("title", "video") + ".mp4"
            filename = sanitize_filename(filename)

            final_path = os.path.join(DOWNLOAD_FOLDER, filename)
            os.rename(raw_filename, final_path)  # Ensure correct filename

        return jsonify({"download_link": f"/downloads/{filename}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to serve files
@app.route("/downloads/<path:filename>")
def download_file(filename):
    sanitized_name = sanitize_filename(filename)
    full_path = os.path.join(app.config["DOWNLOAD_FOLDER"], sanitized_name)

    if not os.path.exists(full_path):
        return "File not found", 404

    return send_from_directory(app.config["DOWNLOAD_FOLDER"], sanitized_name, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

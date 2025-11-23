
import os
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from yt_dlp import YoutubeDL

app = Flask(__name__)
app.secret_key = "secret123"  # For flash messages

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        if not url.strip():
            flash("Please enter a valid Facebook video URL.", "danger")
            return redirect(url_for("index"))

        try:
            ydl_opts = {
                "format": "best",
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s")
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            # Send file to browser
            return send_file(filename, as_attachment=True)

        except Exception as e:
            print(e)
            flash("Failed to download video. Ensure link is PUBLIC.", "danger")
            return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

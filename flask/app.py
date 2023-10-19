#!/usr/bin/env python3
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import subprocess
import os
import tempfile
from pywavefront import Wavefront

app = Flask(__name__)


ALLOWED_EXTENSIONS = {"obj"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/codes/greeble", methods=["POST"])
def greeble():
    if "file" not in request.files:
        return "No file part"

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return "No selected file"

    if uploaded_file and allowed_file(uploaded_file.filename):
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(uploaded_file.read())
            # need to flush the contents to disk, otherwise the with block with cause the file to
            # be deleted before send_file finishes sending it
            temp_file.flush()
            # try:
            #     obj_file = Wavefront(temp_file.name, strict=True)
            #     # You can further process the obj_file object or perform other validations here
            # except Exception as e:
            #     return "Error 1", 503

            # Sanitize the filename
            sanitized_filename = secure_filename(uploaded_file.filename)

            # Create a new file name
            base_name, extension = os.path.splitext(sanitized_filename)
            processed_filename = f"{base_name}-greeble{extension}"

            return send_file(
                temp_file.name, as_attachment=True, download_name=processed_filename
            )

    return "Error 2", 503


# This handler will return a 404 error for any unmatched routes
@app.errorhandler(404)
def not_found(error):
    return "Sorry, wrong page", 404


if __name__ == "__main__":
    app.run()

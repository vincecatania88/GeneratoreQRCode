from flask import Flask, render_template, request
import qrcode
from PIL import Image
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_filename = None
    filename = None

    if request.method == "POST":
        url = request.form.get("url")
        filename = request.form.get("filename")
        logo_file = request.files.get("logo")

        if not filename:
            filename = "qrcode"  # nome di default

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="#000000", back_color="white").convert("RGB")

        if logo_file:
            logo = Image.open(logo_file)
            logo = logo.resize((60, 60))
            qr_center_x = (qr_image.size[0] - logo.size[0]) // 2
            qr_center_y = (qr_image.size[1] - logo.size[1]) // 2
            qr_image.paste(logo, (qr_center_x, qr_center_y), mask=logo)

        qr_filename = f"static/{filename}.png"
        qr_image.save(qr_filename)

    return render_template("index.html", qr_filename=qr_filename, filename=filename)


if __name__ == "__main__":
    app.run(debug=True)

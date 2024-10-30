"""Convert coordinates from L-Est97 to WGS84 and vice versa."""

from flask import Flask, render_template, request
from coordinates_package import coordinates

app = Flask(__name__)

choice = ""


@app.route('/', methods=['GET', 'POST'])
def index():
    """Return home page."""
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    """Return form of entered input data."""
    unit = []
    global choice
    form_data = request.form
    if form_data.get("lest97") == "CONVERT COORDINATES FROM L-Est97 TO WGS84":
        unit = ["X: ", "Y: "]
        choice = "lest97"
    if form_data.get("wgs84") == "CONVERT COORDINATES FROM WGS84 TO L-Est97":
        unit = ["Latitude: ", "Longitude: "]
        choice = "wgs84"
    return render_template('form.html', form_data=unit)


@app.route('/result', methods=['GET', 'POST'])
def result():
    """Calculate coordinates and return results."""
    global choice
    form_data = request.form
    data = list(form_data.values())
    results = tuple()
    if choice == "lest97":
        results = coordinates.coordinates_lest_to_wgs(data[0], data[1])
    if choice == "wgs84":
        results = coordinates.coordinates_wgs_to_lest(data[0], data[1])
    return render_template('result.html', form_data=results, index=index())


if __name__ == '__main__':
    app.run()

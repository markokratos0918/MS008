"""Flask web app for temperature conversion using OOP style."""

from flask import Flask, request, render_template
from temp_converter import TemperatureConverter

app = Flask(__name__)
converter = TemperatureConverter()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main route for displaying and processing the temperature conversion form."""
    result = None
    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            unit_from = request.form['unit_from']
            unit_to = request.form['unit_to']
            converted = converter.convert(value, unit_from, unit_to)
            result = f"{value} {unit_from} = {converted:.2f} {unit_to}"
        except (ValueError, KeyError) as error:
            result = f"Error: {error}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

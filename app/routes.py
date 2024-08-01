from flask import Flask, jsonify
from datetime import datetime
from flask import Flask, jsonify, render_template
from .checker import fetch_availability

last_checked = None


def create_app():
    app = Flask(__name__)

    @app.route('/api/availability', methods=['GET'])
    def availability():
        global last_checked
        data = fetch_availability()  # Your function to get the availability data
        last_checked = datetime.utcnow()
        return jsonify({
            'availability': data,
            'last_checked': last_checked.isoformat() + 'Z'  # ISO format with Z for UTC
        })

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

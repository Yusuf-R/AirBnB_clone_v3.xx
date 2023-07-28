#!/usr/bin/python3
"""module for index route"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def index():
    """index route"""
    status = {"status": "OK"}
    return jsonify(status)
    

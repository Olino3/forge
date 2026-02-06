# Flask Mock Server Template
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os
from datetime import datetime
from typing import Dict, Any

app = Flask(__name__)
CORS(app)

# Configuration
PORT = int(os.getenv('PORT', {{PORT}}))
MOCK_DELAY_MS = int(os.getenv('MOCK_DELAY_MS', 100))

# In-memory data store
data_store: Dict[str, Any] = {
    # {{DATA_STORE}}
}

# Delay middleware
@app.before_request
def add_delay():
    """Simulate network delay"""
    time.sleep(MOCK_DELAY_MS / 1000.0)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'service': '{{SERVICE_NAME}}',
        'timestamp': datetime.now().isoformat()
    })

# {{ENDPOINT_NAME}} - GET list
@app.route('/{{ENDPOINT_PATH}}', methods=['GET'])
def get_items():
    # Query parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    scenario = request.args.get('scenario') or request.headers.get('X-Mock-Scenario')
    
    # Simulate error scenario
    if scenario == 'error':
        return jsonify({
            'error': 'internal_server_error',
            'message': 'Simulated server error'
        }), 500
    
    # Success response
    items = list(data_store.values())
    start = (page - 1) * limit
    end = start + limit
    
    return jsonify({
        'data': items[start:end],  # {{RESPONSE_DATA}}
        'page': page,
        'limit': limit,
        'total': len(items)
    })

# {{ENDPOINT_NAME}} - GET by ID
@app.route('/{{ENDPOINT_PATH}}/<item_id>', methods=['GET'])
def get_item(item_id: str):
    item = data_store.get(item_id)
    
    if not item:
        return jsonify({
            'error': 'not_found',
            'message': f'Item {item_id} not found'
        }), 404
    
    return jsonify(item)

# {{ENDPOINT_NAME}} - POST
@app.route('/{{ENDPOINT_PATH}}', methods=['POST'])
def create_item():
    data = request.get_json()
    
    # Validation
    if not data:
        return jsonify({
            'error': 'validation_error',
            'message': 'Request body is required'
        }), 400
    
    # Simulate specific error scenarios
    if data.get('trigger_error'):
        return jsonify({
            'error': 'unprocessable_entity',
            'message': 'Unable to process request',
            'details': data.get('trigger_error')
        }), 422
    
    # Create new item
    item_id = f"id_{int(time.time() * 1000)}"
    new_item = {
        'id': item_id,
        **data,
        'created_at': datetime.now().isoformat()
    }
    
    data_store[item_id] = new_item
    
    return jsonify(new_item), 201

# {{ENDPOINT_NAME}} - PUT
@app.route('/{{ENDPOINT_PATH}}/<item_id>', methods=['PUT'])
def update_item(item_id: str):
    data = request.get_json()
    
    if item_id not in data_store:
        return jsonify({
            'error': 'not_found',
            'message': f'Item {item_id} not found'
        }), 404
    
    updated_item = {
        **data_store[item_id],
        **data,
        'updated_at': datetime.now().isoformat()
    }
    
    data_store[item_id] = updated_item
    
    return jsonify(updated_item)

# {{ENDPOINT_NAME}} - DELETE
@app.route('/{{ENDPOINT_PATH}}/<item_id>', methods=['DELETE'])
def delete_item(item_id: str):
    if item_id not in data_store:
        return jsonify({
            'error': 'not_found',
            'message': f'Item {item_id} not found'
        }), 404
    
    del data_store[item_id]
    
    return '', 204

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'not_found',
        'message': f'Endpoint {request.method} {request.path} not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'internal_server_error',
        'message': str(error)
    }), 500

if __name__ == '__main__':
    print(f"🎭 Mock Service: {{SERVICE_NAME}}")
    print(f"📍 Running on port: {PORT}")
    print(f"🔗 Health check: http://localhost:{PORT}/health")
    print(f"\nAvailable endpoints:")
    print(f"  GET    http://localhost:{PORT}/{{ENDPOINT_PATH}}")
    print(f"  GET    http://localhost:{PORT}/{{ENDPOINT_PATH}}/<id>")
    print(f"  POST   http://localhost:{PORT}/{{ENDPOINT_PATH}}")
    print(f"  PUT    http://localhost:{PORT}/{{ENDPOINT_PATH}}/<id>")
    print(f"  DELETE http://localhost:{PORT}/{{ENDPOINT_PATH}}/<id>")
    print(f"\nMock delay: {MOCK_DELAY_MS}ms")
    
    app.run(host='0.0.0.0', port=PORT, debug=True)

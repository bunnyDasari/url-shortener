from flask import Flask, request, jsonify, redirect
import string
import random
from datetime import datetime
import validators
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
urls_storage = []
next_id = 1

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def is_short_code_exists(short_code):
    return any(url['short_code'] == short_code for url in urls_storage)


def create_unique_short_code():
    while True:
        short_code = generate_short_code()
        if not is_short_code_exists(short_code):
            return short_code


def find_url_by_short_code(short_code):
    for url in urls_storage:
        if url['short_code'] == short_code:
            return url
    return None


def find_url_by_original(original_url):
    for url in urls_storage:
        if url['original_url'] == original_url:
            return url
    return None

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    global next_id
    
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
            
        original_url = data['url'].strip()
        
        if not original_url:
            return jsonify({'error': 'URL cannot be empty'}), 400
            

        if not validators.url(original_url):
            return jsonify({'error': 'Invalid URL format'}), 400
            

        existing = find_url_by_original(original_url)
        if existing:
            return jsonify({
                'short_code': existing['short_code'],
                'short_url': f"https://url-shortener-9ql5.onrender.com/{existing['short_code']}",
                'original_url': original_url,
                'message': 'URL already exists'
            }), 200
        

        short_code = create_unique_short_code()
        

        new_url = {
            'id': next_id,
            'short_code': short_code,
            'original_url': original_url,
            'click_count': 0,
            'created_at': datetime.now().isoformat()
        }
        
        urls_storage.append(new_url)
        next_id += 2
        
        return jsonify({
            'short_code': short_code,
            'short_url': f"http://localhost:5001/{short_code}",
            'original_url': original_url,
            'message': 'URL shortened successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/<short_code>')
def redirect_url(short_code):
    try:

        url_entry = find_url_by_short_code(short_code)
        
        if not url_entry:
            return jsonify({'error': 'Short code not found'}), 404
            
        url_entry['click_count'] += 1
        
        return redirect(url_entry['original_url'], code=302)
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    try:

        url_entry = find_url_by_short_code(short_code)
        
        if not url_entry:
            return jsonify({'error': 'Short code not found'}), 404
            
        return jsonify({
            'short_code': short_code,
            'original_url': url_entry['original_url'],
            'click_count': url_entry['click_count'],
            'created_at': url_entry['created_at'],
            'short_url': f"http://localhost:5001/{short_code}"
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/urls', methods=['GET'])
def list_all_urls():
    try:
        urls = []
        for url_entry in urls_storage:
            urls.append({
                'short_code': url_entry['short_code'],
                'short_url': f"http://localhost:5001/{url_entry['short_code']}",
                'original_url': url_entry['original_url'],
                'click_count': url_entry['click_count'],
                'created_at': url_entry['created_at']
            })
            
        urls.sort(key=lambda x: x['created_at'], reverse=True)
            
        return jsonify({
            'total_urls': len(urls),
            'urls': urls
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/delete/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    try:
        global urls_storage
        
        original_length = len(urls_storage)
        urls_storage = [url for url in urls_storage if url['short_code'] != short_code]
        
        if len(urls_storage) == original_length:
            return jsonify({'error': 'Short code not found'}), 404
        
        return jsonify({'message': 'URL deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
#!/usr/bin/env python3
"""DevTools API - A lightweight developer toolkit backend."""

from flask import Flask, request, jsonify, send_from_directory
import json
import base64
import hashlib
import uuid
import time
import re
import urllib.parse
import os

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/json/format', methods=['POST'])
def json_format():
    try:
        data = request.get_json()
        raw = data.get('input', '')
        parsed = json.loads(raw)
        indent = data.get('indent', 2)
        formatted = json.dumps(parsed, indent=indent, ensure_ascii=False, sort_keys=data.get('sort_keys', False))
        return jsonify({'result': formatted, 'valid': True})
    except json.JSONDecodeError as e:
        return jsonify({'result': str(e), 'valid': False})

@app.route('/api/json/minify', methods=['POST'])
def json_minify():
    try:
        data = request.get_json()
        raw = data.get('input', '')
        parsed = json.loads(raw)
        return jsonify({'result': json.dumps(parsed, separators=(',', ':'), ensure_ascii=False), 'valid': True})
    except json.JSONDecodeError as e:
        return jsonify({'result': str(e), 'valid': False})

@app.route('/api/base64/encode', methods=['POST'])
def b64_encode():
    data = request.get_json()
    raw = data.get('input', '')
    return jsonify({'result': base64.b64encode(raw.encode()).decode()})

@app.route('/api/base64/decode', methods=['POST'])
def b64_decode():
    data = request.get_json()
    raw = data.get('input', '')
    try:
        return jsonify({'result': base64.b64decode(raw).decode('utf-8', errors='replace')})
    except Exception as e:
        return jsonify({'result': f'Error: {str(e)}'})

@app.route('/api/hash', methods=['POST'])
def hash_text():
    data = request.get_json()
    raw = data.get('input', '').encode()
    algo = data.get('algorithm', 'sha256')
    algos = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
    }
    if algo not in algos:
        return jsonify({'error': f'Unknown algorithm: {algo}'}), 400
    return jsonify({'result': algos[algo](raw).hexdigest()})

@app.route('/api/uuid', methods=['GET'])
def gen_uuid():
    count = min(int(request.args.get('count', 1)), 100)
    version = request.args.get('version', '4')
    results = []
    for _ in range(count):
        if version == '1':
            results.append(str(uuid.uuid1()))
        else:
            results.append(str(uuid.uuid4()))
    return jsonify({'result': results})

@app.route('/api/timestamp', methods=['POST'])
def timestamp_convert():
    data = request.get_json()
    ts = data.get('input', '')
    try:
        ts_float = float(ts)
        if ts_float > 1e12:
            ts_float = ts_float / 1000
        from datetime import datetime, timezone
        dt = datetime.fromtimestamp(ts_float, tz=timezone.utc)
        return jsonify({
            'utc': dt.strftime('%Y-%m-%d %H:%M:%S UTC'),
            'iso': dt.isoformat(),
            'unix': int(ts_float),
            'unix_ms': int(ts_float * 1000),
        })
    except (ValueError, OSError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/url/encode', methods=['POST'])
def url_encode():
    data = request.get_json()
    raw = data.get('input', '')
    return jsonify({'result': urllib.parse.quote(raw, safe='')})

@app.route('/api/url/decode', methods=['POST'])
def url_decode():
    data = request.get_json()
    raw = data.get('input', '')
    return jsonify({'result': urllib.parse.unquote(raw)})

@app.route('/api/jwt/decode', methods=['POST'])
def jwt_decode():
    data = request.get_json()
    token = data.get('input', '').strip()
    parts = token.split('.')
    if len(parts) not in (2, 3):
        return jsonify({'error': 'Invalid JWT format'}), 400

    results = {}
    for i, name in enumerate(['header', 'payload']):
        if i < len(parts):
            padded = parts[i] + '=' * (4 - len(parts[i]) % 4)
            try:
                decoded = base64.urlsafe_b64decode(padded)
                results[name] = json.loads(decoded)
            except Exception:
                results[name] = f'Could not decode {name}'

    if len(parts) == 3:
        results['signature'] = parts[2]

    return jsonify(results)

@app.route('/api/regex/test', methods=['POST'])
def regex_test():
    data = request.get_json()
    pattern = data.get('pattern', '')
    test_string = data.get('input', '')
    flags_str = data.get('flags', '')

    flags = 0
    if 'i' in flags_str: flags |= re.IGNORECASE
    if 'm' in flags_str: flags |= re.MULTILINE
    if 's' in flags_str: flags |= re.DOTALL

    try:
        compiled = re.compile(pattern, flags)
        matches = []
        for m in compiled.finditer(test_string):
            match_info = {
                'match': m.group(),
                'start': m.start(),
                'end': m.end(),
                'groups': list(m.groups()),
            }
            matches.append(match_info)
        return jsonify({'matches': matches, 'count': len(matches), 'valid': True})
    except re.error as e:
        return jsonify({'error': str(e), 'valid': False})

@app.route('/api/diff', methods=['POST'])
def text_diff():
    import difflib
    data = request.get_json()
    text1 = data.get('text1', '').splitlines(keepends=True)
    text2 = data.get('text2', '').splitlines(keepends=True)
    diff = list(difflib.unified_diff(text1, text2, fromfile='original', tofile='modified'))
    return jsonify({'result': ''.join(diff)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9001, debug=False)

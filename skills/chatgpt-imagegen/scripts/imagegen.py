#!/usr/bin/env python3
"""Generate one image with an OpenAI-compatible API, using local configuration."""
import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import sys
import uuid
from urllib import error, parse, request

SKILL = Path(__file__).resolve().parent.parent


def multipart(fields, filename, content):
    boundary = '----imagegen' + uuid.uuid4().hex
    parts = []
    for key, value in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode())
    mime = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="reference"\r\nContent-Type: {mime}\r\n\r\n'.encode())
    parts.extend([content, f'\r\n--{boundary}--\r\n'.encode()])
    return b''.join(parts), f'multipart/form-data; boundary={boundary}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=SKILL / 'config.json')
    parser.add_argument('--prompt-file', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--reference', type=Path)
    parser.add_argument('--force', action='store_true', help='Allow overwriting an existing output')
    args = parser.parse_args()
    if args.output.exists() and not args.force:
        raise ValueError('Output exists; choose another path or pass --force.')
    config = json.loads(args.config.read_text(encoding='utf-8-sig'))
    key = config.get('api_key', '').strip()
    base = config.get('base_url', '').strip().rstrip('/')
    model = config.get('model', '').strip()
    parsed = parse.urlparse(base)
    if not key or not model or parsed.scheme not in ('http', 'https') or not parsed.netloc:
        raise ValueError('Configure a valid base_url, api_key, and model in config.json.')
    prompt = args.prompt_file.read_text(encoding='utf-8-sig').strip()
    if not prompt:
        raise ValueError('Prompt file is empty.')
    fields = {'model': model, 'prompt': prompt, 'n': 1}
    for field in ('size', 'quality', 'response_format'):
        if config.get(field):
            fields[field] = config[field]
    if args.reference:
        body, content_type = multipart(fields, args.reference.name, args.reference.read_bytes())
        endpoint = '/images/edits'
    else:
        body, content_type = json.dumps(fields, ensure_ascii=False).encode('utf-8'), 'application/json'
        endpoint = '/images/generations'
    req = request.Request(base + endpoint, data=body, headers={'Authorization': 'Bearer ' + key, 'Content-Type': content_type}, method='POST')
    try:
        with request.urlopen(req, timeout=float(config.get('timeout_seconds', 600))) as response:
            result = json.load(response)
    except error.HTTPError as exc:
        message = exc.read(2048).decode('utf-8', errors='replace').replace(key, '[REDACTED]')
        raise ValueError(f'API HTTP {exc.code}: {message}') from None
    data = result.get('data', [])
    if isinstance(data, dict):
        data = [data]
    if not data or not isinstance(data[0], dict):
        raise ValueError('API response contains no image data.')
    item = data[0]
    encoded = item.get('b64_json') or item.get('base64') or item.get('b64')
    url = item.get('url') or item.get('image_url')
    if isinstance(url, dict):
        url = url.get('url')
    if encoded:
        raw = base64.b64decode(encoded.split(',', 1)[-1], validate=True)
    elif isinstance(url, str) and url.startswith('data:'):
        raw = base64.b64decode(url.split(',', 1)[1], validate=True)
    elif isinstance(url, str):
        address = parse.urljoin(base + '/', url)
        if parse.urlparse(address).scheme not in ('http', 'https'):
            raise ValueError('Unsupported image URL scheme.')
        with request.urlopen(address, timeout=180) as response:
            raw = response.read()
    else:
        raise ValueError('API returned an unsupported image field.')
    if not raw:
        raise ValueError('API returned an empty image.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('wb' if args.force else 'xb') as output:
        output.write(raw)
    print(f'Saved: {args.output.resolve()}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, error.URLError) as exc:
        print(f'Image generation failed: {exc}', file=sys.stderr)
        sys.exit(1)

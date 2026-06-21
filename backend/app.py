import os
import uuid
from flask import Flask, request, jsonify
from PIL import Image, ImageOps
import db

app = Flask(__name__)

UPLOAD_DIR = os.environ.get('UPLOAD_DIR', os.path.join(os.path.dirname(__file__), 'uploads'))
THUMB_DIR = os.path.join(UPLOAD_DIR, 'thumbs')
ORIG_DIR = os.path.join(UPLOAD_DIR, 'originals')

os.makedirs(THUMB_DIR, exist_ok=True)
os.makedirs(ORIG_DIR, exist_ok=True)

db.init_db()


def ok(data=None):
    return jsonify({'success': True, 'data': data, 'error': None})


def err(msg, status=400):
    return jsonify({'success': False, 'data': None, 'error': msg}), status


def save_photo(file):
    name = uuid.uuid4().hex + '.jpg'
    img = Image.open(file)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ('RGB',):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode in ('RGBA', 'LA'):
            bg.paste(img, mask=img.split()[-1])
        else:
            bg.paste(img.convert('RGB'))
        img = bg
    img.save(os.path.join(ORIG_DIR, name), 'JPEG', quality=90)
    w, h = img.size
    size = min(w, h)
    img = img.crop(((w - size) // 2, (h - size) // 2, (w + size) // 2, (h + size) // 2))
    img = img.resize((400, 400), Image.LANCZOS)
    img.save(os.path.join(THUMB_DIR, name), 'JPEG', quality=78)
    return name


def attach_photos(bottle_id):
    for f in request.files.getlist('photos'):
        if f and f.filename:
            db.add_photo(bottle_id, save_photo(f))


@app.route('/api/breweries/autocomplete')
def breweries_autocomplete():
    return ok(db.brewery_autocomplete(request.args.get('q', '')))


@app.route('/api/styles/autocomplete')
def styles_autocomplete():
    return ok(db.style_autocomplete(request.args.get('q', '')))


@app.route('/api/bottles', methods=['GET'])
def bottles_list():
    return ok(db.list_bottles(
        search=request.args.get('search'),
        brewery=request.args.get('brewery'),
        style=request.args.get('style'),
        country=request.args.get('country'),
    ))


@app.route('/api/bottles', methods=['POST'])
def bottles_create():
    brewery_name = request.form.get('brewery_name', '').strip()
    if not brewery_name:
        return err('Brauerei erforderlich')
    bezeichnung = request.form.get('bezeichnung', '').strip()
    if not bezeichnung:
        return err('Bezeichnung erforderlich')
    bottle_id = db.create_bottle(
        brewery_name,
        request.form.get('brewery_country', '').strip(),
        bezeichnung,
        request.form.get('style', '').strip(),
        request.form.get('notes', '').strip(),
    )
    attach_photos(bottle_id)
    return ok({'id': bottle_id})


@app.route('/api/bottles/<int:bottle_id>', methods=['GET'])
def bottle_detail(bottle_id):
    bottle = db.get_bottle(bottle_id)
    return ok(bottle) if bottle else err('Nicht gefunden', 404)


@app.route('/api/bottles/<int:bottle_id>', methods=['PUT'])
def bottle_update(bottle_id):
    brewery_name = request.form.get('brewery_name', '').strip()
    if not brewery_name:
        return err('Brauerei erforderlich')
    bezeichnung = request.form.get('bezeichnung', '').strip()
    if not bezeichnung:
        return err('Bezeichnung erforderlich')
    db.update_bottle(
        bottle_id,
        brewery_name,
        request.form.get('brewery_country', '').strip(),
        bezeichnung,
        request.form.get('style', '').strip(),
        request.form.get('notes', '').strip(),
    )
    attach_photos(bottle_id)
    return ok({'id': bottle_id})


@app.route('/api/bottles/<int:bottle_id>', methods=['DELETE'])
def bottle_delete(bottle_id):
    db.delete_bottle(bottle_id)
    return ok(None)


@app.route('/api/photos/<int:photo_id>', methods=['DELETE'])
def photo_delete(photo_id):
    filename = db.delete_photo(photo_id)
    if filename:
        for d in (THUMB_DIR, ORIG_DIR):
            p = os.path.join(d, filename)
            if os.path.exists(p):
                os.remove(p)
    return ok(None)


@app.route('/api/breweries', methods=['GET'])
def breweries_list():
    return ok(db.list_breweries())


@app.route('/api/breweries/<int:brewery_id>', methods=['PUT'])
def brewery_update(brewery_id):
    name = request.form.get('name', '').strip()
    if not name:
        return err('Brauerei-Name erforderlich')
    success, error = db.update_brewery(brewery_id, name, request.form.get('country', '').strip())
    return ok({'id': brewery_id}) if success else err(error)


@app.route('/api/breweries/<int:brewery_id>', methods=['DELETE'])
def brewery_delete(brewery_id):
    success, error = db.delete_brewery(brewery_id)
    return ok(None) if success else err(error)


@app.route('/api/breweries/<int:brewery_id>/bottles', methods=['GET'])
def brewery_bottles(brewery_id):
    brewery, bottles = db.get_brewery_with_bottles(brewery_id)
    if brewery is None:
        return err('Nicht gefunden', 404)
    return ok({'brewery': brewery, 'bottles': bottles})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005, debug=False)

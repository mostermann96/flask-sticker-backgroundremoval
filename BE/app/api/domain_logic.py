from BE.app.database.models import Image as db_Image
from BE.app.database.db import db
import os
from werkzeug.utils import secure_filename
from rembg.bg import remove
from BE import settings
import numpy as np
import io
from PIL import ImageFile, Image

ImageFile.LOAD_TRUNCATED_IMAGES = True

def create_cutout(file):
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    file.save(os.path.join(settings.UPLOAD_FOLDER, filename))
    f=np.fromfile(os.path.join(settings.UPLOAD_FOLDER, filename))
    old_filename = filename
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    filename = secure_filename(name + ".png")
    img.save(os.path.join(settings.UPLOAD_FOLDER, filename))
    if os.path.exists(os.path.join(settings.UPLOAD_FOLDER, old_filename)):
        os.remove(os.path.join(settings.UPLOAD_FOLDER, old_filename))
    image = db_Image(username=filename, filepath=filename)
    db.session.add(image)
    #db.add_image(filename,filename)
    db.session.commit()
    return image.id

def delete_cutout(filename):
    filename = secure_filename(filename)
    if os.path.exists(os.path.join(settings.UPLOAD_FOLDER, filename)):
        os.remove(os.path.join(settings.UPLOAD_FOLDER, filename))
    else:
        print("File doesn't exist")

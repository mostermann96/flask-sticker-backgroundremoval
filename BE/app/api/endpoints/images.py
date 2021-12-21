import json

from flask import request, flash, redirect, send_file, url_for, jsonify
from flask_restx import Resource, Namespace
from BE.app.database.models import Image as dbImage
from BE.app.api.domain_logic import create_cutout, delete_cutout
from BE import settings
from flask_restx import fields, reqparse
from BE.app.database.db import db
from werkzeug.datastructures import FileStorage
import werkzeug, os
from flask_jwt_extended import jwt_required, get_jwt_identity
from BE.app.extensions import jwt


ns = Namespace('image', description='Available Ops')
image = ns.model('Image', {
    'id': fields.Integer(readOnly=True, description='The identifier of the image'),
    'username': fields.String(required=True, description='Username of uploader'),
})
upload_parser = ns.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@ns.route('/<int:image_id>')
class Image(Resource):
    @ns.doc('Get single image by ID')
    @jwt_required()
    def get(self, image_id):
        #potential difference between query.filter and query.entities.filter
        # https://stackoverflow.com/questions/24560945/sqlalchemy-get-list-of-ids-from-a-query
        try:
            db_image = dbImage.query.filter(dbImage.id == image_id).one()
        except Exception as e:
            return e, 500
        filename = db_image.filepath
        return send_file(os.path.join(settings.UPLOAD_FOLDER, filename), mimetype='image/png')

    @jwt_required()
    def delete(self, image_id):
        image = dbImage.query.filter_by(id=image_id).first()
        try:
            delete_cutout(image.filepath)
        except Exception as e:
            print(e)
        db.session.delete(image)
        db.session.commit()


@ns.route('/images')
class Images(Resource):
    @ns.doc(security="Bearer Auth")
    @ns.doc('Get list of available image IDs')
    @jwt_required()
    def get(self):
        result = []
        query_result = dbImage.query.with_entities(dbImage.id).all()
        for id in query_result:
            if isinstance(id[0], int):
                result.append(id[0])
        return jsonify(result)

    #@ns.expect(image)
    @ns.doc('Upload a single image, no other payload required')
    @ns.expect(upload_parser)
    @jwt_required()
    def post(self):
        args = upload_parser.parse_args()
        image_file = args['file']  # This is FileStorage instance
        testname = image_file.filename
        image_id = create_cutout(image_file)
        return str(image_id), 200

            # return redirect(url_for('Image.get', image_id=img_id))




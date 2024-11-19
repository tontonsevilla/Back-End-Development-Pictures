from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    pictures = data
    
    if pictures:
        return jsonify(pictures), 200

    return {"message": "Internal server error"}, 500
    
######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = [pic for pic in data if pic['id'] == id]

    if picture:
        return jsonify(picture[0]), 200
    
    return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json

    pictures = [pic for pic in data if pic['id'] == picture['id']]

    if pictures and pictures[0]:
        return {"Message": f"picture with id {picture['id']} already present"}, 302
    else:
        data.append(picture)
        return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pictures = [pic for pic in data if pic['id'] == id]

    if pictures and pictures[0]:
        idx = data.index(pictures[0])
        data[idx] = request.json
        return jsonify(data[idx]), 200

    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pictures = [pic for pic in data if pic['id'] == id]

    if pictures and pictures[0]:
        data.remove(pictures[0])
        return "", 204

    return {"message": "picture not found"}, 404

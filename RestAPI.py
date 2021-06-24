#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from recommendation import *
import requests 
# import cv2, os
# from cv2 import __version__
app = Flask(__name__)
api = Api(app)
CORS(app)


class findfood(Resource):
    def get(selfd,item_id):
        num = 3
        # item_id = 3
        print(item_id)
        recs = recommend(item_id, num)
        return recs


api.add_resource(findfood, '/findfood/<item_id>') # Route_2

if __name__ == '__main__':
     app.run(port=5002)
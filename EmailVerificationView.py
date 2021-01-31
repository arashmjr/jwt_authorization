import pymongo
from flask import Flask, request, jsonify
from flask_classy import FlaskView, route
import random
import datetime
from CoreRepository import CoreRepository
import jwt
from flask_jwt import JWT, jwt_required
from config import api_secret
from bson.objectid import ObjectId
from bson import ObjectId




class EmailVerificationView(FlaskView):

    @route('/sendCode', methods=['POST'])
    def send_email(self):

        email_json = request.get_json()
        number = random.randint(1000, 9999)
        time = datetime.datetime.now()
        myDict = {"token": number, "time": time, "email": email_json['email']}
        data_base = CoreRepository('Verification')
        table_verify = data_base.create_collection('Email_Verification_Collection')
        # x = table_verify.delete_many({})
        # # print(x.deleted_count, " documents deleted.")
        table_verify.insert_one(myDict)
        myquery = {"email": email_json['email']}
        mydoc = table_verify.find_one(myquery)
        result = mydoc['token']
        return jsonify({'code': result})

    @route('/verifyCode', methods=['POST'])
    def send_code(self):
        json = request.get_json()
        data_base = CoreRepository('Verification')
        table_verify = data_base.create_collection('Email_Verification_Collection')
        my_query = {"email": json['email']}
        my_dict = table_verify.find_one(my_query)

        table_profile = data_base.create_collection('Profile')
        time = datetime.datetime.now()
        if my_dict is not None:
            if my_dict['token'] == json['code']:
                record_dict = {'email': json['email'], 'time_register': time}
                table_profile.insert_one(record_dict)
                encoded_jwt = str(jwt.encode({"_id": str(record_dict['_id'])}, api_secret, algorithm="HS256"),'utf-8')
                # print(encoded_jwt)
                # print(record_dict)
                # print(record_dict['_id'])

                # x = table_profile.delete_many({})
                # print(x.deleted_count, " documents deleted.")
                table_verify.delete_one(my_dict)
                return jsonify({'success': True, 'accessToken': encoded_jwt})

        return jsonify({'success': False})


    @route('/register', methods=['POST'])
    def send_token(self):
        if request.headers.get('authorization') is None:
            return {'success': False}, 401
        else:
            encode_token = request.headers['authorization']
            decoded_jwt = jwt.decode(encode_token, api_secret, algorithms="HS256")
            # print(decoded_jwt)
            data_base = CoreRepository('Verification')
            table_profile = data_base.create_collection('Profile')
            query_find_user = {"_id": ObjectId(decoded_jwt['_id'])}
            find_user = table_profile.find_one(query_find_user)

            time = datetime.datetime.now()
            data = request.get_json()
            dict_register = {
                                "first_name": data['firstname'],
                                "last_name": data['lastname'],
                                "country": data['country'],
                                "age": data['age'],
                                "email": find_user['email'],
                                "creation_date": time
                                }
            # prevent from store duplicate record
            user_profile = data_base.create_collection('user_profile')
            items = []
            for item in user_profile.find():
                items.append(item)

            for item in items:
                if dict_register['email'] == item['email']:
                    return {'success': False}

            user_profile.insert_one(dict_register)
            find_dict_user = user_profile.find_one({'email': dict_register['email']})
            find_dict_user['_id'] = str(find_dict_user['_id'])  # value of '_id' convert to str without objectId
            return jsonify(find_dict_user)


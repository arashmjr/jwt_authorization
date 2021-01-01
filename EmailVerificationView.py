import pymongo
from flask import Flask, request,jsonify
from flask_classy import FlaskView, route
import random
import datetime
from CoreRepository import CoreRepository
import jwt
from config import api_secret

class EmailVerificationView(FlaskView):

    @route('/sendCode', methods=['POST'])
    def send_email(self):

        email_json = request.get_json()
        number = random.randint(1000, 9999)
        time = datetime.datetime.now()
        myDict = {"token": number, "time": time, "email": email_json['email']}
        data_base = CoreRepository('Verification')
        table_verify = data_base.create_collection('Email_Verification_Collection')
        # x = table.delete_many({})
        # print(x.deleted_count, " documents deleted.")
        table_verify.insert_one(myDict)
        myquery = {"email": email_json['email']}
        mydoc = table_verify.find_one(myquery)
        result = mydoc['token']
        # mydoc_list = list(mydoc)
        # for x in mydoc_list:
        #     result = x['token']
        #     print(f"code: {x['token']}")
        return jsonify({'code': result})

    @route('/verifyCode', methods=['POST'])
    def send_json(self):
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
                encoded_jwt = jwt.encode({"id": str(record_dict['_id'])}, api_secret, algorithm="HS256")
                # print(encoded_jwt)
                # print(record_dict)
                # x = table_profile.delete_many({})
                # print(x.deleted_count, " documents deleted.")
                table_verify.delete_one(my_dict)
                return jsonify({'success': True, 'accessToken': encoded_jwt})

        return jsonify({'success': False})

from  flask import Flask,jsonify,request,json
from framework import *
app = Flask(__name__)

@app.route('/',methods = ['GET'])
def get_login_page():
    return 'Wiliot Login Page'

@app.route('/generate_access_token',methods = ['GET'])
def generate_access_token():
    try:
        token = generate_token()
        if token.status_code == 200:
            return jsonify ({
                        'status_code':200,"access_token":json.loads(token.text)['access_token'] ,
                        "token_type": "Bearer","expires_in": 21600})
        else:
            return jsonify({
                    'status_code':token.status_code,'message':token.text})
    except Exception as err:
        return err
    
@app.route('/register_gatway/<owner_id>/<gateway_id>',methods=['POST']) 
def register_gateway(owner_id,gateway_id):
    try:
        if owner_id and gateway_id and request.method == 'POST':
            user_input = request.json
            status = registration_gatway(owner_id,gateway_id,user_input)
            if status.status_code == 400 or 403:
                return jsonify ({
                    'message':'Gateway registred successfully',
                    'status_code':200,'status':json.loads(status.text)})
            else:
                return jsonify({
                    'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err

@app.route('/push_data_to_williot_cloud/<gateway_id>/<owner_id>',methods=['POST'])
def push_data_to_williot_cloud(gateway_id,owner_id):
    try:
        if owner_id and gateway_id and request.method == 'POST':
            status = push_data_mqqt_broker(gateway_id,owner_id)
            if status == 'published_data_successfully':
                return jsonify({
                    'staus_code':200,
                    'message':'pushed wiliot packets sucessfully'})
            else:
                return jsonify({
                    'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err

@app.route('/add_new_location/<owner_id>',methods=['POST'])
def add_new_location(owner_id):
    try:
        if owner_id and request.method == 'POST':
            user_input = request.json
            status = add_location(owner_id,user_input)
            if status.status_code == 200:
                return jsonify({'status_code':200,'message':'Location added successfully'})
            else:
                return jsonify({
                    'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err
    
@app.route('/get_all_location_data/<owner_id>/<location_id>')
def get_locations(owner_id,location_id):
    try:
        status = get_all_locations(owner_id,location_id)
        if status.status_code == 200:
            data = status.text
            return jsonify({'status_code':200,'message':'Location data fetched successfully','data':data})
        else:
            return jsonify({
                    'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err

@app.route('/add_zone/<location_id>/<owner_id>',methods = ['POST'])
def add_zone(location_id,owner_id):
    try:
        user_input = request.json
        status = add_zone_location(location_id,owner_id,user_input)
        if status.status_code == 200:
            return jsonify({'status_code':200,'message':'zone added successfully'})
        else:
            return jsonify({
                    'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err
    
@app.route('/get_zones/<location_id>/<owner_id>/<zone_id>')
def get_zones(location_id,owner_id,zone_id):
    try:
        status = get_all_zones(location_id,owner_id,zone_id)
        if status.status_code == 200:
            data = status.text
            return jsonify({'status_code':200,'message':'zone data fetched successfully',data:data})
        else:
           return jsonify({
                    'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err
    
@app.route('/add_new_asset/<owner_id>',methods=['POST'])
def add_new_asset(owner_id):
    try:
        user_input = request.json
        status = add_newasset(owner_id,user_input)
        if status.status_code == 200:
            return jsonify({'status_code':200,'messgae':'asset added successfully'})
        else:
            return jsonify({'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err
    
@app.route('/add_new_category/<owner_id>',methods=['POST'])
def add_new_category(owner_id):
    try:
        user_input = request.json
        status = add_newcategory(owner_id,user_input)
        if status.status_code == 200:
            return jsonify({'status_code':200,'message':'added category successfully'})
        else:
            return jsonify({'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err

@app.route('/new_association/<owner_id>/<location_id>/<zone_id>',methods = ['POST'])
def add_association(owner_id,location_id,zone_id):
    try:
        user_input = request.json
        status = add_new_association(owner_id,location_id,zone_id,user_input)
        if status.status_code == 200:
            return jsonify({'status_code':200,'message':'association added successfully'})
        elif status.status_code == 400:
            return jsonify({'status_code':400,'message':status.text})
        else:
            return jsonify({
                    'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err
    
# @app.route('/new_association/<owner_id>/<location_id>/<zone_id>',methods = ['POST'])
# def add_association(owner_id,location_id,zone_id):
#     try:
#         user_input = request.json
#         status = add_new_association(owner_id,location_id,zone_id,user_input)
#         if status.status_code == 200:
#             return jsonify({'status_code':200,'message':'association added successfully'})
#         elif status.status_code == 400:
#             return jsonify({'status_code':400,'message':status.text})
#         else:
#             return jsonify({
#                     'status_code':status.status_code,'message':status.text})
#     except Exception as err:
#         return err
    
@app.route('/get_listof_gateways/<owner_id>',methods = ['GET'])
def get_gateway_list(owner_id):
    try:
        status = get_all_gatways(owner_id)
        if status.status_code == 200:
            data = status.text
            return jsonify({'status_code':200, 'data' :data ,'message':'Fetched list of gateways successfully'})
        else:
            return jsonify({'status_code':status.status_code,'message':status.text})
    except Exception as err:
        return err
    
# @app.route('/add_bridge/<owner_id>')
# def add_bridge(owner_id):
#     try:
#         # status = add_new_bridege(owner_id)
#     except Exception as err:
#         return err

if __name__ == "__main__":
    app.run()
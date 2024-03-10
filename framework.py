import requests,json
import paho.mqtt.client as mqtt
from endpoints import *
from wiliot_api.platform.platform import *

def create_connection(owner_id):
    try:
        my_api_key = "ODRiNDhjM2QtZGFhNy00ODY0LTg1YmQtZTc1YTQzNzFkOWY1Ok5NSDN1SFVqOFlVbHg1VzByZXN1Y05nYzhmZ2c1djZuUHZFT0VrS3lrM2M="
        owner = owner_id
        platform = PlatformClient(api_key=my_api_key, owner_id=owner)
        return platform
    except Exception as err:
        return err
    
def registration_gatway(owner_id,gateway_id,user_input):
    try:
        user_input = user_input
        get_gatwayid = user_input.get("gatewayType")
        get_getwayname = user_input.get("gatewayName")
        api_body = {
            "gatewayType":get_gatwayid,
            "gatewayName":get_getwayname
        }
        generate_api_json = json.dumps(api_body)
        wiliot_registration_endpoint = gatway_registration_endpoint(owner_id,gateway_id)
        token = generate_token()
        token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImd0eSI6WyJhdXRob3JpemF0aW9uX2NvZGUiXSwia2lkIjoibzk3Mlhkd0hGZEw5WllWdzZid0FtdkF3VHM0In0.eyJhdWQiOiIyMWZmZDQ0NC03NmUyLTRjM2YtOTMxNy0zOGM1ZmRkYjE2OWQiLCJleHAiOjE2OTM5MzcwMTIsImlhdCI6MTY5Mzg5MzgxMiwiaXNzIjoiYWNtZS5jb20iLCJzdWIiOiI1YWQxYzlkMi00MjY1LTQ0YmItYjBkZi1lZGE3OTRjMzUyNzkiLCJqdGkiOiIyYTk5ZGQ0My02MjZlLTQzYWYtYTUzYi01MzQ2ZGU5N2MyYmEiLCJhdXRoZW50aWNhdGlvblR5cGUiOiJQQVNTV09SRCIsImVtYWlsIjoidGh1bmRsYXZAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInByZWZlcnJlZF91c2VybmFtZSI6InRodW5kbGF2QGdtYWlsLmNvbSIsImFwcGxpY2F0aW9uSWQiOiIyMWZmZDQ0NC03NmUyLTRjM2YtOTMxNy0zOGM1ZmRkYjE2OWQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG9mZmxpbmVfYWNjZXNzIiwicm9sZXMiOlsiY29uc3VtZXIiLCJwcm9mZXNzaW9uYWwtc2VydmljZXMiLCJnYXRld2F5Il0sImF1dGhfdGltZSI6MTY5Mzg5MzgxMiwidGlkIjoiMzg2MjM1NjItMzQzNS0zNjMyLTY1MzgtNjUzNTYzMzUzNTY0IiwibGFzdE5hbWUiOiJzYWkiLCJmdWxsTmFtZSI6IlZpdmVrIHNhaSIsIm93bmVycyI6eyI2MDM1NDAyOTE0ODgiOnsicm9sZXMiOlsiYWRtaW4iXX19LCJmaXJzdE5hbWUiOiJWaXZlayIsInVzZXJuYW1lIjoidGh1bmRsYXZAZ21haWwuY29tIn0.YQeKtSNLhflQAaIKGUJUI4R1Bbdyr8e2a0ENUdlSOUIuelb26l1m3APsOPh2_oO_w1v3gNBO_PHEPsQvxO6NKX7Vv1kmg86HetZLh2f2hHDlstvVJaAaEbWsC1s0U5D5dTr7fzfb8y50wvnxmbxqrWgeiWCmLc2gDSAVT8uBl5MtbdmNAC9EVuc4kXJK-2DG1Plvfv1wcyGqRWBE6mhW80PHLvs47n1ks1s26EtYRzbQv9-c1A6xlgibLtnHdKLio7NDDmz9ew4IwsFMZv7HYN3abQOi5OXP9gpUd5gk6jEuonb2jo3pF6jxzjc6TMlml-YrXRW4qwIkDI97TSb15A'
        headers = generate_headers(token)
        make_api_request = requests.request("POST", wiliot_registration_endpoint, headers=headers, data=generate_api_json)
        return make_api_request
    except Exception as err:
        return err
    
def push_data_mqqt_broker():
    try:
        password = generate_token()
        mqqt_connection_details = create_mqqt_broker(password)
        client = mqtt.Client(client_id=mqqt_connection_details.get('client_id'))
        client.username_pw_set(mqqt_connection_details.get('username'), mqqt_connection_details.get('password'))
        client.connect(mqqt_connection_details.get('host'), mqqt_connection_details.get('port'), keepalive=60)
        get_upstream_data = publish_gateway_managemanet_upstream(mqqt_connection_details.get('client_id'),mqqt_connection_details.get('gateway_name'),mqqt_connection_details.get('gateway_type'))
        client.publish(f"https://api.wiliot.com/v1/status-prod/{mqqt_connection_details.get('username')}/{mqqt_connection_details.get('gateway_id')}", json.dumps(get_upstream_data))
        client.on_message = on_message
        client.subscribe(f"update-prod/{mqqt_connection_details.get('username')}/{mqqt_connection_details.get('username')}")
        get_wiliot_packets = wiliot_packets_data(mqqt_connection_details.get('gateway_id'),mqqt_connection_details.get('gateway_name'))
        client.publish(f"https://api.wiliot.com/v1/data-prod/{mqqt_connection_details.get('username')}/{mqqt_connection_details.get('gateway_id')}", json.dumps(get_wiliot_packets))
        return 'published_data_successfully'
    except Exception as err:
        return err

def generate_token():
    try:
        data = wiliot_auth_endpoint()
        auth_url, api_key = data[0],data[1]
        headers = generate_headers(api_key)
        make_api_request = requests.request("POST", auth_url, headers=headers)
        return make_api_request
    except Exception as err:
        return err
    
def get_all_gatways(owner_id):
    try:
        list_of_gatways_endpoint = add_list_gatway_endpoint(owner_id)
        token = generate_token()
        token = json.loads(token.text).get('access_token')
        headers = generate_headers(token)
        make_api_call = requests.request("GET",list_of_gatways_endpoint,headers=headers)
        return make_api_call
    except Exception as err:
        return err

def add_location(owner_id,user_input):
    try:
        add_location_api = add_location_endpoint(owner_id)
        token = generate_token()
        token = json.loads(token.text).get('access_token')
        headers = generate_headers(token)
        api_body = json.dumps(user_input)
        make_api_call = requests.request("POST",add_location_api,headers=headers,data=api_body)
        return make_api_call
    except Exception as err:
        return err
    
def add_zone_location(location_id,owner_id,user_input):
    try:
        add_zone_api = add_zone_endpoint(owner_id,location_id)
        token = generate_token()
        token = json.loads(token.text).get('access_token')
        headers = generate_headers(token)
        api_body = json.dumps(user_input)
        make_api_call = requests.request("POST",add_zone_api,headers=headers,data=api_body)
        return make_api_call
    except Exception as err:
        return err
    
def add_new_association(owner_id,location_id,zone_id,user_input):
    try:
        add_association_api = add_new_association_endpoint(owner_id,location_id,zone_id)
        token = generate_token()
        token = json.loads(token.text).get('access_token')
        headers = generate_headers(token)
        api_body = json.dumps(user_input)
        make_api_call = requests.request("POST",add_association_api,headers=headers,data=api_body)
        return make_api_call
    except Exception as err:
        return err
    
def add_newasset(owner_id,user_input):
    try:
        assest_endpoint = get_assest_endpoint(owner_id)
        token = generate_token()
        token = json.loads(token.text).get('access_token')
        headers = generate_headers(token)
        api_body = json.dumps(user_input)
        make_api_call = requests.request("POST",assest_endpoint,headers=headers,data = api_body)
        return make_api_call
    except Exception as err:
        return err
    
def get_all_locations(owner_id,location_id):
    try:
        get_locations = get_location_endpoint(owner_id,location_id)
        token = generate_token()
        token = json.loads(token.text).get('access_token')
        headers = generate_headers(token)
        make_api_call = requests.request("GET",get_locations,headers=headers)
        return make_api_call
    except Exception as err:
        return err
    
def get_all_zones(location_id,owner_id,zone_id):
    try:
        get_locations = get_zone_endpoint(location_id,owner_id,zone_id)
        token = generate_token()
        token = json.loads(token.text).get('access_token')
        headers = generate_headers(token)
        make_api_call = requests.request("GET",get_locations,headers=headers)
        return make_api_call
    except Exception as err:
        return err
    
def add_newcategory(owner_id,user_input):
    try:
        endpoint = get_category_endpoint(owner_id)
        token = generate_token()
        token = json.loads(token.text).get('access_token')
        headers = generate_headers(token)
        api_body = json.dumps(user_input)
        make_api_call = requests.request("POST",endpoint,headers=headers,data = api_body)
        return make_api_call
    except Exception as err:
        return err
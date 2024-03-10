import json 

def gatway_registration_endpoint(owner_id=None,gateway_id=None):
    try:
        gatway_registration_endpoint = f"https://api.wiliot.com/v1/owner/{owner_id}/gateway/{gateway_id}/mobile"
        return gatway_registration_endpoint
    except Exception as err:
        return err

def generate_headers(token):
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{token}"
        }
        return headers
    except Exception as err:
        return err
    
def create_mqqt_broker(gateway_id,owner_id):
    try:
        host = 'ssl://mqtt.us-east-2.prod.wiliot.cloud'
        port = 1883
        client_id = gateway_id
        username = owner_id
        password = password
        return {'host':host,'port':port,'client_id':client_id,'username':username,'password':password}
    except Exception as err:
        return err
    
def add_list_gatway_endpoint(owner_id):
    try:
        listof_gatways_endpoint = f"https://api.wiliot.com/v1/owner/{owner_id}/gateway"
        return listof_gatways_endpoint
    except Exception as err:
        return err
    
def wiliot_auth_endpoint():
    try:
        api_key = 'ODRiNDhjM2QtZGFhNy00ODY0LTg1YmQtZTc1YTQzNzFkOWY1Ok5NSDN1SFVqOFlVbHg1VzByZXN1Y05nYzhmZ2c1djZuUHZFT0VrS3lrM2M='
        auth_endpoint = "https://api.wiliot.com/v1/auth/token/api"
        return (auth_endpoint,api_key)
    except Exception as err:
        return err
    

def publish_gateway_managemanet_upstream(gateway_id,gateway_name,gateway_type):
    try:
        status_message = {
            "gatewayId":f"{gateway_id}",
            "gatewayName": f"{gateway_name}",
            "gatewayType": f"{gateway_type}",
            "gatewayConf": {
                "interfaceChipSwVersion": "3.14.0",
                "bleChipSwVersion": "3.14.0",
                "apiVersion": "200",
                "additional": {
                    "dataCoupling": False,
                    "txAggregationInterval": 1000
                }
            },
            "tagMetadataCouplingSupported": False,
            "downlinkSupported": True,
            "bridgeOtaUpgradeSupported": False,
            "fwUpgradeSupported": False
        }
        return status_message
    except Exception as err:
        return err
    
def on_message(client, userdata, msg):
    # Handle received messages
    payload = json.loads(msg.payload)
    if "configuration" in payload:
        # Handle configuration message
        print("Received Configuration:", payload)
    elif "action" in payload:
        # Handle action message
        print("Received Action:", payload)

def wiliot_packets_data(gateway_id,gateway_type):
    try:
        data_packet = {
        "gatewayId": f"{gateway_id}",
        "gatewayType": f"{gateway_type}",
        "location": {
            "lat": 32.175853729248047,
            "lng": 34.838546752929688
        },
        "timestamp": 1611674606704,
        "packets": [
            {
                "timestamp": 1611674601701,
                "sequenceId": 0,
                "rssi": 64,
                "payload": "1e16c6fc0000ec010261a009e000000042f6c14839870307190f051202000f"
            },
            # Add more packets as needed
        ]
        }
        return data_packet
    except Exception as err:
        return err
    
def add_location_endpoint(owner_id):
    try:
        location_endpoint = f"https://api.wiliot.com/v1/traceability/owner/{owner_id}/location"
        return location_endpoint
    except Exception as err:
        return err
    
def get_location_endpoint(owner_id,location_id):
    try:
        location_endpoint = f"https://api.wiliot.com/v1/traceability/owner/{owner_id}/location/{location_id}"
        return location_endpoint
    except Exception as err:
        return err
    
def get_assest_endpoint(owner_id):
    try:
        assest_endpoint = f"https://api.wiliot.com/v2/traceability/owner/{owner_id}/asset"
        return assest_endpoint
    except Exception as err:
        return err
    
def get_zone_endpoint(location_id,owner_id,zone_id):
    try:
        location_endpoint = f"https://api.wiliot.com/v1/traceability/owner/{owner_id}/location/{location_id}/zone/{zone_id}"
        return location_endpoint
    except Exception as err:
        return err
    
def add_zone_endpoint(owner_id,location_id):
    try:
        zone_endpoint = f"https://api.wiliot.com/v1/traceability/owner/{owner_id}/location/{location_id}/zone"
        return zone_endpoint
    except Exception as err:
        return err
    
def add_new_association_endpoint(owner_id,location_id,zone_id):
    try:
        assosiation_endpoint = f"https://api.wiliot.com/v1/traceability/owner/{owner_id}/location/{location_id}/zone/{zone_id}/association"
        return assosiation_endpoint
    except Exception as err:
        return err
    
def add_new_bridge():
    try:
        pass
    except Exception as err:
        return err
    
def get_category_endpoint(owner_id):
    try:
        category_endpoint = f"https://api.wiliot.com//v1/traceability/owner/{owner_id}/category"
        return category_endpoint
    except Exception as err:
        return err
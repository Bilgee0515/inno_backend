# import websocket
# import json
# # from xypClient.XypClient import Service
# # from cryptography import x509
# # from cryptography.hazmat.backends import default_backend
# import base64
# import time
# from env import KEY_PATH, REGNUM, WEBSOCKETURL

# # # Helper function to parse the certificate
# # def parse_certificate(cert_base64):
# #     cert_bytes = base64.b64decode(cert_base64)
# #     cert = x509.load_der_x509_certificate(cert_bytes, default_backend())
# #     return cert

# # # Helper function to extract serial number
# # def get_serial_number(cert_base64):
# #     cert = parse_certificate(cert_base64)
# #     serial_number = cert.serial_number
# #     return serial_number.to_bytes((serial_number.bit_length() + 7) // 8, 'big').hex()

# # Function to determine vehicle type ID based on type
# def map_vehicle_type(vehicle_type_str, weight, mancount):
#     if vehicle_type_str == "C" :
#         if weight >= 3.5 :
#             vehicle_type = 4
#         elif weight >= 18:
#             vehicle_type = 6
#         else :
#             vehicle_type = 3

#     if vehicle_type_str == "A" :
#         vehicle_type = 1

#     if vehicle_type_str == "B" :
#         vehicle_type = 2

#     if vehicle_type_str == "D" :
#         if 8 <= mancount <=12 :
#             vehicle_type = 8
#         elif 13 <= mancount <=24 :
#             vehicle_type = 9
#         else: 
#             vehicle_type = 10
    
#     if vehicle_type_str == "M" :
#         vehicle_type = 11


#     return vehicle_type  # Default to 0 if type not found

# # # WebSocket implementation for XYP Service
# # def get_vehicle_type(lic_plate):
# #     def on_message(ws, message):
# #         try:
# #             sign = json.loads(message)
# #             params = {
# #                 'auth': {
# #                     'citizen': {
# #                         'certFingerprint': get_serial_number(sign['certificate']),
# #                         'regnum': REGNUM,
# #                         'signature': sign['signature'],
# #                     }
# #                 },
# #                 'plateNumber': lic_plate
# #             }

# #             # Call XYP Service
# #             citizen = Service(
# #                 'https://xyp.gov.mn/citizen-1.5.0/ws?WSDL', 
# #                 str(int(time.time())), 
# #                 pkey_path=KEY_PATH
# #             )
# #             response = citizen.call('WS100401_getVehicleInfo', params)

# #             # Extract vehicle type from the response
# #             vehicle_type = response.get('className', '')
# #             weight = response.get('weight', '')
# #             mancount = response.get('manCount', '')
# #             vehicle_type_id = map_vehicle_type(vehicle_type, weight, mancount)
# #             ws.close()
# #             return vehicle_type_id

# #         except Exception as e:
# #             print(f"Error processing WebSocket message: {e}")
# #             ws.close()
# #             return 0

# #     def on_error(ws, error):
# #         print(f"WebSocket error: {error}")
# #         ws.close()

# #     def on_close(ws):
# #         print("### WebSocket closed ###")

# #     def on_open(ws):
# #         def run(*args):
# #             timestamp = str(int(time.time()))
# #             dataSign = REGNUM + "." + timestamp
# #             ws.send(json.dumps({"type": "e457cb50ed64bde0", "data": dataSign}))
# #         thread.start_new_thread(run, ())

# #     websocket.enableTrace(False)
# #     ws = websocket.WebSocketApp(
# #         WEBSOCKETURL,
# #         on_message=on_message,
# #         on_error=on_error,
# #         on_close=on_close,
# #     )
# #     ws.on_open = on_open
# #     ws.run_forever()

# # # Example usage:
# # plate_number = "1234ABC"
# # vehicle_type_id = get_vehicle_type(plate_number)
# # print(f"Vehicle Type ID: {vehicle_type_id}")

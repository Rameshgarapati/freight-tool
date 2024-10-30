# # import http.client
# # import json

# # conn = http.client.HTTPSConnection("www.mtdirect.ca")
# # payload = json.dumps({
# #   "contact": {
# #     "name": "Example User",
# #     "company": "MY COMPANY NAME",
# #     "contact_method": "E",
# #     "contact_method_value": "example.user@mycompany.com",
# #     "shipment_type": "ROAD",
# #     "shipment_terms": "PPD"
# #   },
# #   "origin": {
# #     "city": "TORONTO",
# #     "province": "ON",
# #     "postal_zip": "M1B",
# #     "residential_pickup": False,
# #     "tailgate_pickup": True,
# #     "flat_deck_pickup": False,
# #     "inside_pickup": False,
# #     "drop_off_at_terminal": False,
# #     "warehouse_pickup": False
# #   },
# #   "destination": {
# #     "city": "CALGARY",
# #     "province": "AB",
# #     "postal_zip": "T2A1A1",
# #     "residential_delivery": False,
# #     "tailgate_delivery": True,
# #     "flat_deck_delivery": False,
# #     "inside_delivery": False,
# #     "dock_pickup": False
# #   },
# #   "items": [
# #     {
# #       "class_value": "70",
# #       "pieces": 1,
# #       "package_code_value": "SK",
# #       "description": "A description of my skid",
# #       "total_weight": 200,
# #       "weight_unit_value": "LBS",
# #       "length": 48,
# #       "width": 40,
# #       "height": 40,
# #       "unit_value": "I"
# #     },
# #     {
# #       "class_value": "70",
# #       "pieces": 2,
# #       "package_code_value": "PK",
# #       "description": "A description of my pallets",
# #       "total_weight": 500,
# #       "weight_unit_value": "LBS",
# #       "length": 50,
# #       "width": 60,
# #       "height": 20,
# #       "unit_value": "I"
# #     }
# #   ],
# #   "other": {
# #     "declared_value": 0,
# #     "currency_type": "C",
# #     "dangerous_goods": False,
# #     "protective_services_heat": False,
# #     "protective_services_reefer": False,
# #     "rock_solid_service_guarantee": False,
# #     "rock_solid_service_value": "",
# #     "call_prior_to_delivery": False,
# #     "off_hour_pickup": False,
# #     "off_hour_delivery": False,
# #     "delivery_by_appointment": False,
# #     "rural_route": False
# #   }
# # })
# # headers = {
# #   'Authorization': 'Token ', 
# #   'Content-Type': 'application/json'
# # }
# # conn.request("POST", "/api/online_quoting/quote", payload, headers)
# # res = conn.getresponse()
# # data = res.read()
# # print(data.decode("utf-8"))

# import http.client
# import json
# from pypostalcode import PostalCodeDatabase
# import pandas as pd
# from datetime import datetime
# from error_mail import send_error_email


# pcdb = PostalCodeDatabase()
# def manitulin_test(fromcode,tocode,noitems,mcweight,length,width,height):
#   # fromcode="L6T3X4"
#   # tocode="E3B4C3"
#   conn = http.client.HTTPSConnection("www.mtdirect.ca")
#   payload = json.dumps({
#     "contact": {
#       "name": "Arul",
#       "company": "Source Atlantic",
#       "contact_method": "E",
#       "contact_method_value": "kannana@sourceatlantic.ca",
#       "shipment_type": "ROAD",
#       "shipment_terms": "PPD"
#     },
#     "origin": {

#       "postal_zip": fromcode,
#       "residential_pickup": False,
#       "tailgate_pickup": True,
#       "flat_deck_pickup": False,
#       "inside_pickup": False,
#       "drop_off_at_terminal": False,
#       "warehouse_pickup": False
#     },
#     "destination": {

#       "postal_zip": tocode,
#       "residential_delivery": False,
#       "tailgate_delivery": True,
#       "flat_deck_delivery": False,
#       "inside_delivery": False,
#       "dock_pickup": False
#     },
#     "items": [
#       {
#         "class_value": "70",
#         "pieces": noitems,
#         "package_code_value": "SK",
#         "description": "A description of my skid",
#         "total_weight": mcweight,
#         "weight_unit_value": "LBS",
#         "length": length,
#         "width": width,
#         "height": height,
#         "unit_value": "I"
#       }
#     ],
#     "other": {
#       "declared_value": 0,
#       "currency_type": "C",
#       "dangerous_goods": False,
#       "protective_services_heat": False,
#       "protective_services_reefer": False,
#       "rock_solid_service_guarantee": False,
#       "rock_solid_service_value": "",
#       "call_prior_to_delivery": False,
#       "off_hour_pickup": False,
#       "off_hour_delivery": False,
#       "delivery_by_appointment": False,
#       "rural_route": False
#     }
#   })
#   token = '6802f6dfb6b086eb9ff2f4ca89c2d21fa6f3fef4' #Change this token in May 2025
#   headers = {
#     'Authorization': 'Access-Token c291cmNlc3Rqb2huOk1BTklUT1VMSU46NjgwMmY2ZGZiNmIwODZlYjlmZjJmNGNhODljMmQyMWZhNmYzZmVmNA==', # Expires on May 2025 , Change token into base64
#     'Content-Type': 'application/json'
#   }
#   charges_df=pd.DataFrame()
#   quote_records=pd.DataFrame()
#   print(pcdb[((fromcode[0:3]).upper())].city)
#   try:
#     print("started Manitaulin")
#     conn.request("POST", "/api/online_quoting/quote", payload, headers)
#     res = conn.getresponse()
#     data = res.read()

#     json_data = data.decode("utf-8")
#     json_data = json.loads(json_data)
#     print(json_data)

    



#     # Create a DataFrame for quote records
#     quote_records = pd.DataFrame({
#         "Provider":"Manitoulin",
#         "Service Type": "Manitoulin courier",
#         'ShipDate': datetime.today().strftime('%Y-%m-%d'),
#         "From":pcdb[((fromcode[0:3]).upper())].city,
#         "To":pcdb[((tocode[0:3]).upper())].city,
#         "QuoteTotal":[json_data['freight_charge']],
#         "No of items":noitems,
#         "weight":mcweight
#     })

#     # Create a DataFrame for charges
    

#     temp=[
#       {
#         "Provider":"Manitoulin",
#         "Service Type": "Manitoulin courier",
#         "Description":"Federal Tax",
#         "Amount":[json_data['federal_tax']]
#       },
#       {

#         "Provider":"Manitoulin",
#         "Service Type": "Manitoulin courier",
#         "Description":"Fuel Charge",
#         "Amount":[json_data['fuel_charge']]
#       },
#       {
#         "Provider":"Manitoulin",
#         "Service Type": "Manitoulin courier",
#         "Description":"Total Accessorial Charge",
#         "Amount":[json_data['total_accessorial_charge']]
#       }
#     ]
#     charges_df = pd.DataFrame(temp)
    

#     # Print the resulting DataFrames
#     print(quote_records, charges_df)
#     return quote_records, charges_df
#   except Exception as e:
#     send_error_email(str(e),"Manitulin")
#     print("no data",e)
#     return quote_records,charges_df

# def manitulin_test_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2):
#   # fromcode="L6T3X4"
#   # tocode="E3B4C3"
#   conn = http.client.HTTPSConnection("www.mtdirect.ca")
#   payload = json.dumps({
#     "contact": {
#       "name": "Arul",
#       "company": "Source Atlantic",
#       "contact_method": "E",
#       "contact_method_value": "kannana@sourceatlantic.ca",
#       "shipment_type": "ROAD",
#       "shipment_terms": "PPD"
#     },
#     "origin": {

#       "postal_zip": fromcode,
#       "residential_pickup": False,
#       "tailgate_pickup": True,
#       "flat_deck_pickup": False,
#       "inside_pickup": False,
#       "drop_off_at_terminal": False,
#       "warehouse_pickup": False
#     },
#     "destination": {

#       "postal_zip": tocode,
#       "residential_delivery": False,
#       "tailgate_delivery": True,
#       "flat_deck_delivery": False,
#       "inside_delivery": False,
#       "dock_pickup": False
#     },
#     "items": [
#       {
#         "class_value": "70",
#         "pieces": noitems,
#         "package_code_value": "SK",
#         "description": "A description of my skid",
#         "total_weight": mcweight,
#         "weight_unit_value": "LBS",
#         "length": length,
#         "width": width,
#         "height": height,
#         "unit_value": "I"
#       },
#       {
#         "class_value": "70",
#         "pieces": noitems2,
#         "package_code_value": "PK",
#         "description": "A description of my pallets",
#         "total_weight": mcweight2,
#         "weight_unit_value": "LBS",
#         "length": length2,
#         "width": width2,
#         "height": height2,
#         "unit_value": "I"
#       }
#     ],
#     "other": {
#       "declared_value": 0,
#       "currency_type": "C",
#       "dangerous_goods": False,
#       "protective_services_heat": False,
#       "protective_services_reefer": False,
#       "rock_solid_service_guarantee": False,
#       "rock_solid_service_value": "",
#       "call_prior_to_delivery": False,
#       "off_hour_pickup": False,
#       "off_hour_delivery": False,
#       "delivery_by_appointment": False,
#       "rural_route": False
#     }
#   })
#   token = '6802f6dfb6b086eb9ff2f4ca89c2d21fa6f3fef4' #Change this token in May 2025
#   headers = {
#     'Authorization': 'Access-Token c291cmNlc3Rqb2huOk1BTklUT1VMSU46NjgwMmY2ZGZiNmIwODZlYjlmZjJmNGNhODljMmQyMWZhNmYzZmVmNA==', # Expires on May 2025 , Change token into base64
#     'Content-Type': 'application/json'
#   }
#   charges_df=pd.DataFrame()
#   quote_records=pd.DataFrame()
#   print(pcdb[((fromcode[0:3]).upper())].city)
#   try:
#     print("started Manitaulin")
#     conn.request("POST", "/api/online_quoting/quote", payload, headers)
#     res = conn.getresponse()
#     data = res.read()

#     json_data = data.decode("utf-8")
#     json_data = json.loads(json_data)
#     print(json_data)

    



#     # Create a DataFrame for quote records
#     quote_records = pd.DataFrame({
#         "Provider":"Manitoulin",
#         "Service Type": "Manitoulin courier",
#         'ShipDate': datetime.today().strftime('%Y-%m-%d'),
#         "From":pcdb[((fromcode[0:3]).upper())].city,
#         "To":pcdb[((tocode[0:3]).upper())].city,
#         "QuoteTotal":[json_data['freight_charge']],
#         "No of items":int(noitems)+int(noitems2),
#         "weight":int(mcweight)+int(mcweight2)
#     })

#     # Create a DataFrame for charges
    

#     temp=[
#       {
#         "Provider":"Manitoulin",
#         "Service Type": "Manitoulin courier",
#         "Description":"Federal Tax",
#         "Amount":[json_data['federal_tax']]
#       },
#       {

#         "Provider":"Manitoulin",
#         "Service Type": "Manitoulin courier",
#         "Description":"Fuel Charge",
#         "Amount":[json_data['fuel_charge']]
#       },
#       {
#         "Provider":"Manitoulin",
#         "Service Type": "Manitoulin courier",
#         "Description":"Total Accessorial Charge",
#         "Amount":[json_data['total_accessorial_charge']]
#       }
#     ]
#     charges_df = pd.DataFrame(temp)
    

#     # Print the resulting DataFrames
#     print(quote_records, charges_df)
#     return quote_records, charges_df
#   except Exception as e:
#     send_error_email(str(e),"Manitulin")
#     print("no data",e)
#     return quote_records,charges_df


# # test1=manitulin_test_multiple("E3B3V5","M5V3L9","10","300","30", "40", "20", "2", "400", "40", "30", "25")
# # test2=manitulin_test("E3B3V5","M5V3L9","10","300","30", "40", "20")

# # print(test1)
# # print(test2)



import http.client
import json
from pypostalcode import PostalCodeDatabase
import pandas as pd


pcdb = PostalCodeDatabase()
def manitulin_test(fromcode,tocode,noitems,mcweight,length,width,height):
  # fromcode="L6T3X4"
  # tocode="E3B4C3"
  conn = http.client.HTTPSConnection("www.mtdirect.ca")
  payload = json.dumps({
    "contact": {
      "name": "Arul",
      "company": "Source Atlantic",
      "contact_method": "E",
      "contact_method_value": "kannana@sourceatlantic.ca",
      "shipment_type": "ROAD",
      "shipment_terms": "PPD"
    },
    "origin": {

      "postal_zip": fromcode,
      "residential_pickup": False,
      "tailgate_pickup": True,
      "flat_deck_pickup": False,
      "inside_pickup": False,
      "drop_off_at_terminal": False,
      "warehouse_pickup": False
    },
    "destination": {

      "postal_zip": tocode,
      "residential_delivery": False,
      "tailgate_delivery": True,
      "flat_deck_delivery": False,
      "inside_delivery": False,
      "dock_pickup": False
    },
    "items": [
      {
        "class_value": "70",
        "pieces": noitems,
        "package_code_value": "SK",
        "description": "A description of my skid",
        "total_weight": mcweight,
        "weight_unit_value": "LBS",
        "length": length,
        "width": width,
        "height": height,
        "unit_value": "I"
      }
    ],
    "other": {
      "declared_value": 0,
      "currency_type": "C",
      "dangerous_goods": False,
      "protective_services_heat": False,
      "protective_services_reefer": False,
      "rock_solid_service_guarantee": False,
      "rock_solid_service_value": "",
      "call_prior_to_delivery": False,
      "off_hour_pickup": False,
      "off_hour_delivery": False,
      "delivery_by_appointment": False,
      "rural_route": False
    }
  })
  #print(payload)
  token = '6802f6dfb6b086eb9ff2f4ca89c2d21fa6f3fef4' #Change this token in May 2025
  headers = {
    'Authorization': 'Access-Token c291cmNlc3Rqb2huOk1BTklUT1VMSU46NjgwMmY2ZGZiNmIwODZlYjlmZjJmNGNhODljMmQyMWZhNmYzZmVmNA==', # Expires on May 2025 , Change token into base64
    'Content-Type': 'application/json'
  }




  payload1 = json.dumps({
    "contact": {
      "name": "Arul",
      "company": "Source Atlantic",
      "contact_method": "E",
      "contact_method_value": "kannana@sourceatlantic.ca",
      "shipment_type": "RAIL",
      "shipment_terms": "PPD"
    },
    "origin": {

      "postal_zip": fromcode,
      "residential_pickup": False,
      "tailgate_pickup": True,
      "flat_deck_pickup": False,
      "inside_pickup": False,
      "drop_off_at_terminal": False,
      "warehouse_pickup": False
    },
    "destination": {

      "postal_zip": tocode,
      "residential_delivery": False,
      "tailgate_delivery": True,
      "flat_deck_delivery": False,
      "inside_delivery": False,
      "dock_pickup": False
    },
    "items": [
      {
        "class_value": "70",
        "pieces": noitems,
        "package_code_value": "SK",
        "description": "A description of my skid",
        "total_weight": mcweight,
        "weight_unit_value": "LBS",
        "length": length,
        "width": width,
        "height": height,
        "unit_value": "I"
      }
    ],
    "other": {
      "declared_value": 0,
      "currency_type": "C",
      "dangerous_goods": False,
      "protective_services_heat": False,
      "protective_services_reefer": False,
      "rock_solid_service_guarantee": False,
      "rock_solid_service_value": "",
      "call_prior_to_delivery": False,
      "off_hour_pickup": False,
      "off_hour_delivery": False,
      "delivery_by_appointment": False,
      "rural_route": False
    }
  })


  try:
    #print("started Manitaulin")
    conn.request("POST", "/api/online_quoting/quote", payload, headers)


    res = conn.getresponse()


    data = res.read()

    json_data = data.decode("utf-8")
    json_data = json.loads(json_data)
    #print(json_data)
    conn.close()
    conn.request("POST", "/api/online_quoting/quote", payload1, headers)

    res1 = conn.getresponse()
    data1 = res1.read()

    json_data1 = data1.decode("utf-8")
    json_data1 = json.loads(json_data1)
    #print(json_data1)


    quote_records = pd.DataFrame()
    charges_df = pd.DataFrame()
    
    if 'freight_charge' in json_data:
      temp=[
      {
        "Provider":"Manitoulin",
        "Service Type": "Road",
        "Description":"Federal Tax",
        "Amount":[json_data['federal_tax']]
      },
      {

        "Provider":"Manitoulin",
        "Service Type": "Road",
        "Description":"Fuel Charge",
        "Amount":[json_data['fuel_charge']]
      },
      {
        "Provider":"Manitoulin",
        "Service Type": "Road",
        "Description":"Total Accessorial Charge",
        "Amount":[json_data['total_accessorial_charge']]
      }]
      road_df = pd.DataFrame(temp)
      charges_df = pd.concat([charges_df, road_df], ignore_index=True)



    



    # Create a DataFrame for quote records

    
      df_road  =pd.DataFrame( [{
        "Provider":"Manitoulin",
        "Service Type": "Road",
        "From":pcdb[((fromcode[0:3]).upper())].city,
        "To":pcdb[((tocode[0:3]).upper())].city,
        "QuoteTotal":[json_data['freight_charge']],
        "No of items":noitems,
        "weight":mcweight
    }])
      quote_records = pd.concat([quote_records, df_road], ignore_index=True)

    if 'freight_charge' in json_data1:


      temp1=[
      {
        "Provider":"Manitoulin",
        "Service Type": "Rail",
        "Description":"Federal Tax",
        "Amount":[json_data1['federal_tax']]
      },
      {

        "Provider":"Manitoulin",
        "Service Type": "Rail",
        "Description":"Fuel Charge",
        "Amount":[json_data1['fuel_charge']]
      },
      {
        "Provider":"Manitoulin",
        "Service Type": "Rail",
        "Description":"Total Accessorial Charge",
        "Amount":[json_data1['total_accessorial_charge']]
      }]
      rail_df = pd.DataFrame(temp1)
      charges_df = pd.concat([charges_df, rail_df], ignore_index=True)


      
      
      df_rail=  pd.DataFrame( [
    {
        "Provider":"Manitoulin",
        "Service Type": "Rail",
        "From":pcdb[((fromcode[0:3]).upper())].city,
        "To":pcdb[((tocode[0:3]).upper())].city,
        "QuoteTotal":[json_data1['freight_charge']],
        "No of items":noitems,
        "weight":mcweight
    }])
    


    
    
      quote_records = pd.concat([quote_records, df_rail], ignore_index=True)
    #print(quote_records)

  
    # Print the resulting DataFrames
    #print(quote_records, charges_df)
    return quote_records, charges_df
  except Exception as e:
    #print("no data",e)
    return quote_records,charges_df


#charges_df,quote_records = manitulin_test("E2M4W9","L6T3X4",10,12,12,12,12)



def manitulin_test_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2):

  # fromcode="L6T3X4"
  # tocode="E3B4C3"
  conn = http.client.HTTPSConnection("www.mtdirect.ca")
  payload = json.dumps({
    "contact": {
      "name": "Arul",
      "company": "Source Atlantic",
      "contact_method": "E",
      "contact_method_value": "kannana@sourceatlantic.ca",
      "shipment_type": "ROAD",
      "shipment_terms": "PPD"
    },
    "origin": {

      "postal_zip": fromcode,
      "residential_pickup": False,
      "tailgate_pickup": True,
      "flat_deck_pickup": False,
      "inside_pickup": False,
      "drop_off_at_terminal": False,
      "warehouse_pickup": False
    },
    "destination": {

      "postal_zip": tocode,
      "residential_delivery": False,
      "tailgate_delivery": True,
      "flat_deck_delivery": False,
      "inside_delivery": False,
      "dock_pickup": False
    },
    "items": [
      {
        "class_value": "70",
        "pieces": noitems,
        "package_code_value": "SK",
        "description": "A description of my skid",
        "total_weight": mcweight,
        "weight_unit_value": "LBS",
        "length": length,
        "width": width,
        "height": height,
        "unit_value": "I"
      },

      {
        "class_value": "70",
        "pieces": noitems2,
        "package_code_value": "PK",
        "description": "A description of my pallets",
        "total_weight": mcweight2,
        "weight_unit_value": "LBS",
        "length": length2,
        "width": width2,
        "height": height2,
        "unit_value": "I"
      }
    ],
    "other": {
      "declared_value": 0,
      "currency_type": "C",
      "dangerous_goods": False,
      "protective_services_heat": False,
      "protective_services_reefer": False,
      "rock_solid_service_guarantee": False,
      "rock_solid_service_value": "",
      "call_prior_to_delivery": False,
      "off_hour_pickup": False,
      "off_hour_delivery": False,
      "delivery_by_appointment": False,
      "rural_route": False
    }
  })
  #print(payload)
  token = '6802f6dfb6b086eb9ff2f4ca89c2d21fa6f3fef4' #Change this token in May 2025
  headers = {
    'Authorization': 'Access-Token c291cmNlc3Rqb2huOk1BTklUT1VMSU46NjgwMmY2ZGZiNmIwODZlYjlmZjJmNGNhODljMmQyMWZhNmYzZmVmNA==', # Expires on May 2025 , Change token into base64
    'Content-Type': 'application/json'
  }




  payload1 = json.dumps({
    "contact": {
      "name": "Arul",
      "company": "Source Atlantic",
      "contact_method": "E",
      "contact_method_value": "kannana@sourceatlantic.ca",
      "shipment_type": "RAIL",
      "shipment_terms": "PPD"
    },
    "origin": {

      "postal_zip": fromcode,
      "residential_pickup": False,
      "tailgate_pickup": True,
      "flat_deck_pickup": False,
      "inside_pickup": False,
      "drop_off_at_terminal": False,
      "warehouse_pickup": False
    },
    "destination": {

      "postal_zip": tocode,
      "residential_delivery": False,
      "tailgate_delivery": True,
      "flat_deck_delivery": False,
      "inside_delivery": False,
      "dock_pickup": False
    },
    "items": [
      {
        "class_value": "70",
        "pieces": noitems,
        "package_code_value": "SK",
        "description": "A description of my skid",
        "total_weight": mcweight,
        "weight_unit_value": "LBS",
        "length": length,
        "width": width,
        "height": height,
        "unit_value": "I"
      },
      {
        "class_value": "70",
        "pieces": noitems2,
        "package_code_value": "PK",
        "description": "A description of my pallets",
        "total_weight": mcweight2,
        "weight_unit_value": "LBS",
        "length": length2,
        "width": width2,
        "height": height2,
        "unit_value": "I"
      }
    ],
    "other": {
      "declared_value": 0,
      "currency_type": "C",
      "dangerous_goods": False,
      "protective_services_heat": False,
      "protective_services_reefer": False,
      "rock_solid_service_guarantee": False,
      "rock_solid_service_value": "",
      "call_prior_to_delivery": False,
      "off_hour_pickup": False,
      "off_hour_delivery": False,
      "delivery_by_appointment": False,
      "rural_route": False
    }
  })


  try:
    #print("started Manitaulin")
    conn.request("POST", "/api/online_quoting/quote", payload, headers)


    res = conn.getresponse()


    data = res.read()

    json_data = data.decode("utf-8")
    json_data = json.loads(json_data)
    #print(json_data)
    conn.close()
    conn.request("POST", "/api/online_quoting/quote", payload1, headers)

    res1 = conn.getresponse()
    data1 = res1.read()

    json_data1 = data1.decode("utf-8")
    json_data1 = json.loads(json_data1)
    #print(json_data1)


    quote_records = pd.DataFrame()
    charges_df = pd.DataFrame()
    
    if 'freight_charge' in json_data:
      temp=[
      {
        "Provider":"Manitoulin",
        "Service Type": "Road",
        "Description":"Federal Tax",
        "Amount":[json_data['federal_tax']]
      },
      {

        "Provider":"Manitoulin",
        "Service Type": "Road",
        "Description":"Fuel Charge",
        "Amount":[json_data['fuel_charge']]
      },
      {
        "Provider":"Manitoulin",
        "Service Type": "Road",
        "Description":"Total Accessorial Charge",
        "Amount":[json_data['total_accessorial_charge']]
      }]
      road_df = pd.DataFrame(temp)
      charges_df = pd.concat([charges_df, road_df], ignore_index=True)



    



    # Create a DataFrame for quote records

    
      df_road  =pd.DataFrame( [{
        "Provider":"Manitoulin",
        "Service Type": "Road",
        "From":pcdb[((fromcode[0:3]).upper())].city,
        "To":pcdb[((tocode[0:3]).upper())].city,
        "QuoteTotal":[json_data['freight_charge']],
        "No of items":noitems,
        "weight":mcweight
    }])
      quote_records = pd.concat([quote_records, df_road], ignore_index=True)

    if 'freight_charge' in json_data1:


      temp1=[
      {
        "Provider":"Manitoulin",
        "Service Type": "Rail",
        "Description":"Federal Tax",
        "Amount":[json_data1['federal_tax']]
      },
      {

        "Provider":"Manitoulin",
        "Service Type": "Rail",
        "Description":"Fuel Charge",
        "Amount":[json_data1['fuel_charge']]
      },
      {
        "Provider":"Manitoulin",
        "Service Type": "Rail",
        "Description":"Total Accessorial Charge",
        "Amount":[json_data1['total_accessorial_charge']]
      }]
      rail_df = pd.DataFrame(temp1)
      charges_df = pd.concat([charges_df, rail_df], ignore_index=True)


      
      
      df_rail=  pd.DataFrame( [
    {
        "Provider":"Manitoulin",
        "Service Type": "Rail",
        "From":pcdb[((fromcode[0:3]).upper())].city,
        "To":pcdb[((tocode[0:3]).upper())].city,
        "QuoteTotal":[json_data1['freight_charge']],
        "No of items":noitems,
        "weight":mcweight
    }])
    


    
    
      quote_records = pd.concat([quote_records, df_rail], ignore_index=True)
    #print(quote_records)

  
    # Print the resulting DataFrames
    #print(quote_records, charges_df)
    return quote_records, charges_df
  except Exception as e:
    #print("no data",e)
    return quote_records,charges_df


#charges_df,quote_records = manitulin_test("E2M4W9","L6T3X4",10,12,12,12,12)


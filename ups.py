
# import requests
# from requests.auth import HTTPBasicAuth

# # UPS API credentials
# client_id = 'Pvk3qZRn0RwlTUUhqOv6Z3CyUArYA780PBt5mvEWPWYVT6gs'
# client_secret = 'o9mL4n79OENWEaPImTR8sVGmWzCtTrprJ5WBGexfdUH6sN6ciFkzpJNSwc2rCsus'
# redirect_uri = 'https://www.sourceatlantic.ca/'

# def ups_rates():
#     url = "https://wwwcie.ups.com/security/v1/oauth/token"

#     payload = {
#     "grant_type": "client_credentials"
#     }

#     headers = {
#     "Content-Type": "application/x-www-form-urlencoded",
#     "x-merchant-id": "string"
#     }

#     response = requests.post(url, data=payload, headers=headers, auth=('Pvk3qZRn0RwlTUUhqOv6Z3CyUArYA780PBt5mvEWPWYVT6gs','o9mL4n79OENWEaPImTR8sVGmWzCtTrprJ5WBGexfdUH6sN6ciFkzpJNSwc2rCsus'))

#     data = response.json()
#     access_token=data["access_token"]
#     print(access_token)
#     print(data["access_token"])

#     version = "v2403"
#     url = "https://wwwcie.ups.com/api/shipments/" + version + "/ship"

#     query = {
#     "additionaladdressvalidation": "string"
#     }

#     payload = {
#         "ShipmentRequest": {
#             "Request": {
#                 "SubVersion": "1801",
#                 "RequestOption": "nonvalidate",
#                 "TransactionReference": {
#                     "CustomerContext": "testing"
#                 }
#             },
#             "Shipment": {
#                 "Description": "Ship WS test",
#                 "Shipper": {
#                     "Name": "ShipperName",
#                     "AttentionName": "ShipperZs Attn Name",
#                     "TaxIdentificationNumber": "123456",
#                     "Phone": {
#                         "Number": "1115554758",
#                         "Extension": " "
#                     },
#                     "ShipperNumber": "1R3900",
#                     "FaxNumber": "8002222222",
#                     "Address": {
#                         "AddressLine": ["123 Main St"],
#                         'City': 'Toronto',
#                         'StateProvinceCode': 'ON',
#                         'PostalCode': 'M5H 2N2',
#                         'CountryCode': 'CA'
#                     }
#                 },
#                 "ShipTo": {
#                     "Name": "Happy Dog Pet Supply",
#                     "AttentionName": "1160b_74",
#                     "Phone": {
#                         "Number": "9225377171"
#                     },
#                     "Address": {
#                         "AddressLine": ["602 Graham Ave"],
#                         'City': 'Vancouver',
#                         'StateProvinceCode': 'BC',
#                         'PostalCode': 'V5K 0A1',
#                         'CountryCode': 'CA'
#                     },
#                     "Residential": " "
#                 },
#                 "ShipFrom": {
#                     "Name": "T and T Designs",
#                     "AttentionName": "1160b_74",
#                     "Phone": {
#                         "Number": "1234567890"
#                     },
#                     "FaxNumber": "1234567890",
#                     "Address": {
#                         "AddressLine": ["610 Reid street"],
#                         'City': 'Toronto',
#                         'StateProvinceCode': 'ON',
#                         'PostalCode': 'M5H 2N2',
#                         'CountryCode': 'CA'
#                     }
#                 },
#                 "PaymentInformation": {
#                     "ShipmentCharge": {
#                         "Type": "01",
#                         "BillShipper": {
#                             "AccountNumber": "1R3900"
#                         }
#                     }
#                 },
#                 "Service": {
#                     "Code": ['01' , '02' , '03' , '12'],
#                     "Description": "Express"
#                 },
#                 "Package": {
#                     "Description": " ",
#                     "Packaging": {
#                         "Code": "02",
#                         "Description": "Nails"
#                     },
#                     "Dimensions": {
#                         "UnitOfMeasurement": {
#                             "Code": "IN",
#                             "Description": "Inches"
#                         },
#                         "Length": "10",
#                         "Width": "30",
#                         "Height": "45"
#                     },
#                     "PackageWeight": {
#                         "UnitOfMeasurement": {
#                             "Code": "LBS",
#                             "Description": "Pounds"
#                         },
#                         "Weight": "5"
#                     }
#                 },
#                 "TaxInformationIndicator": "1"
#             },
#             "LabelSpecification": {
#                 "LabelImageFormat": {
#                     "Code": "GIF",
#                     "Description": "GIF"
#                 },
#                 "HTTPUserAgent": "Mozilla/4.5"
#             }
#         }
#     }

#     headers = {
#     "Content-Type": "application/json",
#     "transId": "string",
#     "transactionSrc": "testing",
#     "Authorization": "Bearer "+access_token
#     }
#     print("Bearer "+access_token)

#     response = requests.post(url, json=payload, headers=headers, params=query)

#     data = response.json()
#     print("next")
#     print(data)

#     shipment_results = data['ShipmentResponse']['ShipmentResults']
#     shipment_charges = shipment_results['ShipmentCharges']
#     package_results = shipment_results['PackageResults'][0]

#     service_name = "Xpresspost"  # Assuming the service name is known
#     base_price = float(shipment_charges['BaseServiceCharge']['MonetaryValue'])
#     gst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "GST"), "0.00")
#     pst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "PST"), "0.00")
#     hst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "HST"), "0.00")
#     due = float(shipment_charges['TotalCharges']['MonetaryValue'])
#     fuel_surcharge = next((item['MonetaryValue'] for item in package_results['ItemizedCharges'] if item['Code'] == "432"), "0.00")
#     expected_delivery_date = "2024-10-28"  # Assuming the expected delivery date is known

#     # Printing the extracted values
#     print(f"Service Name: {service_name}")
#     print(f"Base Price: {base_price}")
#     print(f"GST: {gst}")
#     print(f"PST: {pst}")
#     print(f"HST: {hst}")
#     print(f"Due: {due}")
#     print(f"Fuel Surcharge: {fuel_surcharge}")
#     print(f"Expected Delivery Date: {expected_delivery_date}")

# print(ups_rates())

# # service_codes = ['01' , '02' , '03' , '12']



import requests
import pandas as pd
from datetime import datetime
from error_mail import send_error_email

def ups_rates(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc):
    final_rates=[]
    final_tax=[]
    final_from=from_loc.split(",")[0]
    final_province1=from_loc.split(",")[1][1:3]
    final_to=to_loc.split(",")[0]
    final_province2=to_loc.split(",")[1][1:3]
    service_codes = ['01' , '02' , '03' , '12']

    servicename = {"01": "UPS Next Day Air", "02": "UPS 2nd Day Air", "03": "UPS Ground", "12": "UPS 3 Day Select12"}

    for i in service_codes:
        try:
            url = "https://wwwcie.ups.com/security/v1/oauth/token"

            payload = {
                "grant_type": "client_credentials"
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "x-merchant-id": "string"
            }

            response = requests.post(url, data=payload, headers=headers, auth=('Pvk3qZRn0RwlTUUhqOv6Z3CyUArYA780PBt5mvEWPWYVT6gs','o9mL4n79OENWEaPImTR8sVGmWzCtTrprJ5WBGexfdUH6sN6ciFkzpJNSwc2rCsus'))

            data = response.json()
            access_token = data["access_token"]

            version = "v2403"
            url = "https://wwwcie.ups.com/api/shipments/" + version + "/ship"

            query = {
                "additionaladdressvalidation": "string"
            }

            payload = {
                "ShipmentRequest": {
                    "Request": {
                        "SubVersion": "1801",
                        "RequestOption": "nonvalidate",
                        "TransactionReference": {
                            "CustomerContext": "testing"
                        }
                    },
                    "Shipment": {
                        
                        "Shipper": {
                            "Name": "test",
                            "ShipperNumber": "1R3900",
                            
                            "Address": {
                                "AddressLine": ["test"],
                                'City': 'Saint John',
                                'StateProvinceCode': 'NB',
                                'PostalCode': 'M5H 2N2',
                                'CountryCode': 'CA'
                            }
                        },
                        "ShipTo": {
                            "Name": "test",
                            "Address": {
                                "AddressLine": ["test"],
                                'City': final_to,
                                'StateProvinceCode': final_province2,
                                'PostalCode': tocode,
                                'CountryCode': 'CA'
                            },
                            "Residential": " "
                        },
                        "ShipFrom": {
                            "Name": "test",
                            "Address": {
                                "AddressLine": ["testr"],
                                'City': final_from,
                                'StateProvinceCode': final_province1,
                                'PostalCode': fromcode,
                                'CountryCode': 'CA'
                            }
                        },
                        "PaymentInformation": {
                            "ShipmentCharge": {
                                "Type": "01",
                                "BillShipper": {
                                    "AccountNumber": "1R3900"
                                }
                            }
                        },
                        "Service": {
                            "Code": i
                            
                        },
                        "Package": {
                            "Description": " ",
                            "Packaging": {
                                "Code": "02",
                                "Description": "Nails"
                            },
                            "Dimensions": {
                                "UnitOfMeasurement": {
                                    "Code": "IN",
                                    "Description": "Inches"
                                },
                                "Length": length,
                                "Width": width,
                                "Height": height
                            },
                            "PackageWeight": {
                                "UnitOfMeasurement": {
                                    "Code": "LBS",
                                    "Description": "Pounds"
                                },
                                "Weight": mcweight
                            },
                            "ItemCount": noitems
                        },
                        "TaxInformationIndicator": "1"
                    },
                    "LabelSpecification": {
                        "LabelImageFormat": {
                            "Code": "GIF",
                            "Description": "GIF"
                        },
                        "HTTPUserAgent": "Mozilla/4.5"
                    }
                }
            }

            headers = {
                "Content-Type": "application/json",
                "transId": "string",
                "transactionSrc": "testing",
                "Authorization": "Bearer " + access_token
            }

            response = requests.post(url, json=payload, headers=headers, params=query)

            data = response.json()
            print(data)

            if 'ShipmentResponse' in data and 'ShipmentResults' in data['ShipmentResponse']:
                shipment_results = data['ShipmentResponse']['ShipmentResults']
                shipment_charges = shipment_results['ShipmentCharges']
                package_results = shipment_results['PackageResults'][0]

                service_name = "Xpresspost"  # Assuming the service name is known
                base_price = float(shipment_charges['BaseServiceCharge']['MonetaryValue'])
                gst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "GST"), "0.00")
                pst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "PST"), "0.00")
                hst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "HST"), "0.00")
                due = float(shipment_charges['TotalCharges']['MonetaryValue'])
                fuel_surcharge = shipment_charges['ItemizedCharges'][0]['MonetaryValue']
                expected_delivery_date = "2024-10-28"  # Assuming the expected delivery date is known
                temp_rate={
                    "Provider":"UPS",
                    "Service Type": servicename[i],
                    'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                    "From":from_loc,
                    "To":to_loc,
                    "QuoteTotal":due,
                    "No of days for delivery (Estimated)":"2",
                    "No of items":noitems,
                    "weight":mcweight
                }
                if float(gst)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"GST",
                        "Amount":gst
                    }
                    final_tax.append(temp_tax)
                    
                if float(hst)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"HST",
                        "Amount":hst
                    }
                    final_tax.append(temp_tax)

                if float(pst)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"PST",
                        "Amount":pst
                    }
                    final_tax.append(temp_tax)
                if float(fuel_surcharge)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"Fuel Surcharge",
                        "Amount":fuel_surcharge
                    }
                    final_tax.append(temp_tax)

                
                final_rates.append(temp_rate)
                

                
            
                

        except Exception as e:
            send_error_email(str(e),"UPS")
            print(f"An error occurred: {e}")
            return pd.DataFrame(),pd.DataFrame()
    final_rates=pd.DataFrame(final_rates)
    final_tax=pd.DataFrame(final_tax)

    return final_tax,final_rates


def ups_rates_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2,from_loc,to_loc):
    final_rates=[]
    final_tax=[]
    final_from=from_loc.split(",")[0]
    final_province1=from_loc.split(",")[1][1:3]
    final_to=to_loc.split(",")[0]
    final_province2=to_loc.split(",")[1][1:3]
    service_codes = ['01' , '02' , '03' , '12']
    servicename = {"01": "UPS Next Day Air", "02": "UPS 2nd Day Air", "03": "UPS Ground", "12": "UPS 3 Day Select12"}

    

 
    for i in service_codes:
        try:
            url = "https://wwwcie.ups.com/security/v1/oauth/token"

            payload = {
                "grant_type": "client_credentials"
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "x-merchant-id": "string"
            }

            response = requests.post(url, data=payload, headers=headers, auth=('Pvk3qZRn0RwlTUUhqOv6Z3CyUArYA780PBt5mvEWPWYVT6gs','o9mL4n79OENWEaPImTR8sVGmWzCtTrprJ5WBGexfdUH6sN6ciFkzpJNSwc2rCsus'))

            data = response.json()
            access_token = data["access_token"]

            version = "v2403"
            url = "https://wwwcie.ups.com/api/shipments/" + version + "/ship"

            query = {
                "additionaladdressvalidation": "string"
            }

            payload = {
                "ShipmentRequest": {
                    "Request": {
                        "SubVersion": "1801",
                        "RequestOption": "nonvalidate",
                        "TransactionReference": {
                            "CustomerContext": "testing"
                        }
                    },
                    "Shipment": {
                        
                        "Shipper": {
                            "Name": "test",
                            "ShipperNumber": "1R3900",
                            
                            "Address": {
                                "AddressLine": ["test"],
                                'City': 'Saint John',
                                'StateProvinceCode': 'NB',
                                'PostalCode': 'M5H 2N2',
                                'CountryCode': 'CA'
                            }
                        },
                        "ShipTo": {
                            "Name": "test",
                            "Address": {
                                "AddressLine": ["test"],
                                'City': final_to,
                                'StateProvinceCode': final_province2,
                                'PostalCode': tocode,
                                'CountryCode': 'CA'
                            },
                            "Residential": " "
                        },
                        "ShipFrom": {
                            "Name": "test",
                            "Address": {
                                "AddressLine": ["testr"],
                                'City': final_from,
                                'StateProvinceCode': final_province1,
                                'PostalCode': fromcode,
                                'CountryCode': 'CA'
                            }
                        },
                        "PaymentInformation": {
                            "ShipmentCharge": {
                                "Type": "01",
                                "BillShipper": {
                                    "AccountNumber": "1R3900"
                                }
                            }
                        },
                        "Service": {
                            "Code": i
                            
                        },
                        "Package": [{
                            "Description": " ",
                            "Packaging": {
                                "Code": "02",
                                "Description": "test"
                            },
                            "Dimensions": {
                                "UnitOfMeasurement": {
                                    "Code": "IN",
                                    "Description": "Inches"
                                },
                                "Length": length,
                                "Width": width,
                                "Height": height
                            },
                            "PackageWeight": {
                                "UnitOfMeasurement": {
                                    "Code": "LBS",
                                    "Description": "Pounds"
                                },
                                "Weight": mcweight
                            },
                            "ItemCount": noitems
                        },{
                            "Description": "test",
                            "Packaging": {
                                "Code": "02",
                                "Description": "test"
                            },
                            "Dimensions": {
                                "UnitOfMeasurement": {
                                    "Code": "IN",
                                    "Description": "Inches"
                                },
                                "Length": length2,
                                "Width": width2,
                                "Height": height2
                            },
                            "PackageWeight": {
                                "UnitOfMeasurement": {
                                    "Code": "LBS",
                                    "Description": "Pounds"
                                },
                                "Weight": mcweight2
                            },
                            "ItemCount": noitems2
                        }

                        ],
                        "TaxInformationIndicator": "1"
                    },
                    "LabelSpecification": {
                        "LabelImageFormat": {
                            "Code": "GIF",
                            "Description": "GIF"
                        },
                        "HTTPUserAgent": "Mozilla/4.5"
                    }
                }
            }

            headers = {
                "Content-Type": "application/json",
                "transId": "string",
                "transactionSrc": "testing",
                "Authorization": "Bearer " + access_token
            }

            response = requests.post(url, json=payload, headers=headers, params=query)

            data = response.json()
            print(data)

            if 'ShipmentResponse' in data and 'ShipmentResults' in data['ShipmentResponse']:
                shipment_results = data['ShipmentResponse']['ShipmentResults']
                shipment_charges = shipment_results['ShipmentCharges']
                package_results = shipment_results['PackageResults'][0]

                service_name = "Xpresspost"  # Assuming the service name is known
                base_price = float(shipment_charges['BaseServiceCharge']['MonetaryValue'])
                gst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "GST"), "0.00")
                pst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "PST"), "0.00")
                hst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "HST"), "0.00")
                due = float(shipment_charges['TotalCharges']['MonetaryValue'])
                fuel_surcharge = shipment_charges['ItemizedCharges'][0]['MonetaryValue']
                expected_delivery_date = "2024-10-28"  # Assuming the expected delivery date is known
                temp_rate={
                    "Provider":"UPS",
                    "Service Type": servicename[i],
                    'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                    "From":from_loc,
                    "To":to_loc,
                    "QuoteTotal":due,
                    "No of days for delivery (Estimated)":"2",
                    "No of items":int(noitems)+int(noitems2),
                    "weight":int(mcweight)+int(mcweight2)
                }
                if float(gst)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"GST",
                        "Amount":gst
                    }
                    final_tax.append(temp_tax)
                    
                if float(hst)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"HST",
                        "Amount":hst
                    }
                    final_tax.append(temp_tax)

                if float(pst)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"PST",
                        "Amount":pst
                    }
                    final_tax.append(temp_tax)
                if float(fuel_surcharge)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"Fuel Surcharge",
                        "Amount":fuel_surcharge
                    }
                    final_tax.append(temp_tax)

                
                final_rates.append(temp_rate)
                

                
            
                

        except Exception as e:
            send_error_email(str(e),"UPS")
            print(f"An error occurred: {e}")
            return pd.DataFrame(),pd.DataFrame()
    final_rates=pd.DataFrame(final_rates)
    final_tax=pd.DataFrame(final_tax)

    return final_tax,final_rates





def ups_rates_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc):
    final_rates=[]
    final_tax=[]
    final_from=from_loc.split(",")[0]
    final_province1=from_loc.split(",")[1][1:3]
    final_to=to_loc.split(",")[0]
    final_province2=to_loc.split(",")[1][1:3]
    service_codes = ['01' , '02' , '03' , '12']

    servicename = {"01": "Next Day Air", "02" : "2nd Day Air", "03" : "Ground",  "07" : "Express", "08" : "Expedited", "11" : "UPS Standard", "12" : "3 Day Select", "13" : "Next Day Air Saver", "14" : "UPS Next Day Air® Early","17" : "UPS Worldwide Economy DDU","54" : "Express Plus","59" : "2nd Day Air A.M.","65" : "UPS Saver","M2" : "First Class Mail","M3" : "Priority Mail","M4" : "Expedited MaiI Innovations","M5" : "Priority Mail Innovations","M6" : "Economy Mail Innovations","M7" : "MaiI Innovations (MI) Returns","70" : "UPS Access Point™ Economy","71" : "UPS Worldwide Express Freight Midday","72" : "UPS Worldwide Economy DDP","74" : "UPS Express®12:00","75" : "UPS Heavy Goods","82" : "UPS Today Standard","83" : "UPS Today Dedicated Courier","84" : "UPS Today Intercity","85" : "UPS Today Express","86" : "UPS Today Express Saver","96" : "UPS Worldwide Express Freight."}


    item=[]
    totalweight=0
    totalitem=0
    for i in range(len(length)):
        temp={
                            "Description": " ",
                            "Packaging": {
                                "Code": "02",
                                "Description": "test"
                            },
                            "Dimensions": {
                                "UnitOfMeasurement": {
                                    "Code": "IN",
                                    "Description": "Inches"
                                },
                                "Length": length[i],
                                "Width": width[i],
                                "Height": height[i]
                            },
                            "PackageWeight": {
                                "UnitOfMeasurement": {
                                    "Code": "LBS",
                                    "Description": "Pounds"
                                },
                                "Weight": mcweight[i]
                            },
                            "ItemCount": noitems[i]
                        }
        totalweight += float(mcweight[i])
        totalitem += int(noitems[i])
        item.append(temp)

    for i in servicename:
        try:
            url = "https://wwwcie.ups.com/security/v1/oauth/token"

            payload = {
                "grant_type": "client_credentials"
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "x-merchant-id": "string"
            }

            response = requests.post(url, data=payload, headers=headers, auth=('Pvk3qZRn0RwlTUUhqOv6Z3CyUArYA780PBt5mvEWPWYVT6gs','o9mL4n79OENWEaPImTR8sVGmWzCtTrprJ5WBGexfdUH6sN6ciFkzpJNSwc2rCsus'))

            data = response.json()
            access_token = data["access_token"]

            version = "v2403"
            url = "https://wwwcie.ups.com/api/shipments/" + version + "/ship"

            query = {
                "additionaladdressvalidation": "string"
            }

            payload = {
                "ShipmentRequest": {
                    "Request": {
                        "SubVersion": "1801",
                        "RequestOption": "nonvalidate",
                        "TransactionReference": {
                            "CustomerContext": "testing"
                        }
                    },
                    "Shipment": {
                        
                        "Shipper": {
                            "Name": "test",
                            "ShipperNumber": "1R3900",
                            
                            "Address": {
                                "AddressLine": ["test"],
                                'City': 'Saint John',
                                'StateProvinceCode': 'NB',
                                'PostalCode': 'M5H 2N2',
                                'CountryCode': 'CA'
                            }
                        },
                        "ShipTo": {
                            "Name": "test",
                            "Address": {
                                "AddressLine": ["test"],
                                'City': final_to,
                                'StateProvinceCode': final_province2,
                                'PostalCode': tocode,
                                'CountryCode': 'CA'
                            },
                            "Residential": " "
                        },
                        "ShipFrom": {
                            "Name": "test",
                            "Address": {
                                "AddressLine": ["testr"],
                                'City': final_from,
                                'StateProvinceCode': final_province1,
                                'PostalCode': fromcode,
                                'CountryCode': 'CA'
                            }
                        },
                        "PaymentInformation": {
                            "ShipmentCharge": {
                                "Type": "01",
                                "BillShipper": {
                                    "AccountNumber": "1R3900"
                                }
                            }
                        },
                        "Service": {
                            "Code": i
                            
                        },
                        "Package": item,
                        "TaxInformationIndicator": "1"
                    },
                    "LabelSpecification": {
                        "LabelImageFormat": {
                            "Code": "GIF",
                            "Description": "GIF"
                        },
                        "HTTPUserAgent": "Mozilla/4.5"
                    }
                }
            }

            headers = {
                "Content-Type": "application/json",
                "transId": "string",
                "transactionSrc": "testing",
                "Authorization": "Bearer " + access_token
            }

            response = requests.post(url, json=payload, headers=headers, params=query)

            data = response.json()
            print(data)

            if 'ShipmentResponse' in data and 'ShipmentResults' in data['ShipmentResponse']:
                shipment_results = data['ShipmentResponse']['ShipmentResults']
                shipment_charges = shipment_results['ShipmentCharges']
                package_results = shipment_results['PackageResults'][0]

                service_name = "Xpresspost"  # Assuming the service name is known
                base_price = float(shipment_charges['BaseServiceCharge']['MonetaryValue'])
                gst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "GST"), "0.00")
                pst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "PST"), "0.00")
                hst = next((item['MonetaryValue'] for item in shipment_charges['TaxCharges'] if item['Type'] == "HST"), "0.00")
                due = float(shipment_charges['TotalCharges']['MonetaryValue'])
                fuel_surcharge = shipment_charges['ItemizedCharges'][0]['MonetaryValue']
                expected_delivery_date = "2024-10-28"  # Assuming the expected delivery date is known
                temp_rate={
                    "Provider":"UPS",
                    "Service Type": servicename[i],
                    'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                    "From":from_loc,
                    "To":to_loc,
                    "QuoteTotal":due,
                    "No of days for delivery (Estimated)":"2",
                    "No of items":totalitem,
                    "weight":totalweight
                }
                if float(gst)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"GST",
                        "Amount":gst
                    }
                    final_tax.append(temp_tax)
                    
                if float(hst)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"HST",
                        "Amount":hst
                    }
                    final_tax.append(temp_tax)

                if float(pst)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"PST",
                        "Amount":pst
                    }
                    final_tax.append(temp_tax)
                if float(fuel_surcharge)>0.00:
                    temp_tax={
                        "Provider":"UPS",
                        "Service Type": "UPS",
                        "Description":"Fuel Surcharge",
                        "Amount":fuel_surcharge
                    }
                    final_tax.append(temp_tax)

                
                final_rates.append(temp_rate)
                

                
            
                

        except Exception as e:
            send_error_email(str(e),"UPS")
            print(f"An error occurred: {e}")
            return pd.DataFrame(),pd.DataFrame()
    final_rates=pd.DataFrame(final_rates)
    final_tax=pd.DataFrame(final_tax)

    return final_tax,final_rates



# from_loc="FREDERICTON, NB (E3B3V5)"
# to_loc="TORONTO, ON (M5V3L9)"
# fromcode = 'E3B3V5'
# tocode = 'M5V3L9'
# noitems = ["2","3"]
# mcweight = ["10","20"]
# length = ["20","30"]
# width = ["15","20"]
# height = ["10","15"]


# data,tax=ups_rates_list(fromcode, tocode, noitems, mcweight, length, width, height,from_loc,to_loc)
# print(data,tax)
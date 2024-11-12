from typing import Counter
from zipfile import ZIP_FILECOUNT_LIMIT
from flask import Flask, render_template, request
import pandas as pd
import json
from pandas.core.dtypes.missing import notnull
import requests
import os
import numpy as np
# from suds.client import Client
# from pypostalcode import PostalCodeDatabase
# import xmltodict
# from uszipcode import SearchEngine, SimpleZipcode
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from threading import Timer
from fedex_token import check_folder_and_set_variable
from fedex_token import check_folder_and_run_code
# from counter import read_counter
# from counter import update_counter
from pypostalcode import PostalCodeDatabase


from datetime import datetime
from datetime import date
from xml.etree.ElementTree import XML, fromstring

import requests
from requests.structures import CaseInsensitiveDict
import json
# from suds.client import Client
# import xmltodict
# from pypostalcode import PostalCodeDatabase

from xml.etree.ElementTree import XML, fromstring
import xml
import pandas as pd
# from suds.sax.text import Raw
import threading  
import time
from error_mail import send_error_email
# from log import log_terminal_activities

folder_path = os.getcwd()


def fedex_test(fromcode,tocode,noitems,mcweight,country,length, width, height):

    fedex_data=[]
    fedex_tax=[]


    
    # fromcode="E3B3V5"
    # tocode="E3B4C3"
    # country ="CA"
    # mcweight=8

    
    tkn = "token"
    pcdb = PostalCodeDatabase()


    file_check = check_folder_and_set_variable()
    print (file_check)

    token = check_folder_and_run_code(file_check)


	
    #response1 = requests.request("POST", url1, data=payload1, headers=headers1)
    #token = json.loads(response1.text)['access_token']
    print(token)
    url = "https://apis.fedex.com/rate/v1/rates/quotes"
    headers = {
        'Content-Type': "application/json",
        'X-locale': "en_CA",
        'Authorization': 'Bearer '+ token
    }

    query1= {
        "accountNumber": {"value": "458975000"},
        "rateRequestControlParameters": {"returnTransitTimes": "true"},
        "requestedShipment": {
            "preferredCurrency": "CAD",
            "rateRequestType": ["PREFERRED"],
            "shipper": {
                "address": {
                    "postalCode": fromcode,
                    "countryCode": country
                }
            },
            "recipient": {
                "address": {
                    "postalCode": tocode,
                    "countryCode": country
                }
            },
            "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
            "packagingType": "YOUR_PACKAGING",
            "requestedPackageLineItems": [
                {
                    "subPackagingType": "BAG",
                    "groupPackageCount": 1,
    
                    "weight": {
                        "units": "LB",
                        "value": mcweight
                    },
                    "dimensions": {
                        "length": length,
                        "width": width,
                        "height": height,
                        "units": "IN"
                    }
                },
                
                # Add more packages as needed
            ]
        }
    }
    # query1 = {"accountNumber": {"value": "458975000"},"rateRequestControlParameters": {"returnTransitTimes": "true",},"requestedShipment": {"preferredCurrency": "CAD","rateRequestType": ["PREFERRED"],"shipper": {"address": {"postalCode": fromcode,"countryCode": "CA"}},"recipient": {"address": {"postalCode": tocode,"countryCode": country}},"pickupType": "DROPOFF_AT_FEDEX_LOCATION","packagingType": "YOUR_PACKAGING","requestedPackageLineItems": [{ "weight": {"units": "LB","value": mcweight},}]}}
   
    query1 = json.dumps(query1)
    try:
        response2 = requests.request("POST", url, data=query1, headers=headers)
        response3 = response2.json()
        print(response3)
        # print(response3['output']['rateReplyDetails'][1])
        
        for i in response3['output']['rateReplyDetails']:
            if "transitDays" in i["commit"]:
                temp={
                    "Provider":"Fedex",
                    "Service Type": i['serviceName'],
                    'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                    "From":pcdb[(i["commit"]['derivedOriginDetail']['postalCode'])[0:3].upper()].city,
                    "To":pcdb[(i["commit"]['derivedDestinationDetail']['postalCode'])[0:3].upper()].city,
                    "QuoteTotal":i['ratedShipmentDetails'][0]['totalNetFedExCharge'],
                    "No of days for delivery (Estimated)":i["commit"]["transitDays"]['description'],
                    "No of items":noitems,
                    "weight":mcweight
                }
            else:
                temp={
                    "Provider":"Fedex",
                    "Service Type": i['serviceName'],
                    'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                    "From":pcdb[(i["commit"]['derivedOriginDetail']['postalCode'])[0:3].upper()].city,
                    "To":pcdb[(i["commit"]['derivedDestinationDetail']['postalCode'])[0:3].upper()].city,
                    "QuoteTotal":i['ratedShipmentDetails'][0]['totalNetFedExCharge'],
                    "No of days for delivery (Estimated)":"1",
                    "No of items":noitems,
                    "weight":mcweight
                }
            temp_tax={
                "Provider":"Fedex",
                "Service Type": i['serviceName'],
                "Description":i['ratedShipmentDetails'][0]['shipmentRateDetail']['surCharges'][0]['description'],
                "Amount":i['ratedShipmentDetails'][0]['shipmentRateDetail']['surCharges'][0]['amount']
            }
            temp_tax_2={
                "Provider":"Fedex",
                "Service Type": i['serviceName'],
                "Description":i['ratedShipmentDetails'][0]['shipmentRateDetail']['taxes'][0]['description'],
                "Amount":i['ratedShipmentDetails'][0]['shipmentRateDetail']['taxes'][0]['amount']
            }
            fedex_tax.append(temp_tax)
            fedex_tax.append(temp_tax_2)
            fedex_data.append(temp)
    except Exception as e:
        send_error_email(str(e),"Fedex")
        print(e)

    print(fedex_data)
    print("tax")
    print(fedex_tax)
    fedex_data=pd.DataFrame(fedex_data)
    fedex_tax=pd.DataFrame(fedex_tax)
    return fedex_data,fedex_tax
    # return render_template('home.html',tables=[fedex_tax.to_html(classes='data', header="true",index = False)],tables1=[fedex_data.to_html(classes='data', header="true",index = False)])

def fedex_test_multiple(fromcode,tocode,noitems,mcweight,country,length, width, height, noitems2, mcweight2, length2, width2, height2):

    fedex_data=[]
    fedex_tax=[]


    
    # fromcode="E3B3V5"
    # tocode="E3B4C3"
    # country ="CA"
    # mcweight=8

    
    tkn = "token"
    pcdb = PostalCodeDatabase()


    file_check = check_folder_and_set_variable()
    print (file_check)

    token = check_folder_and_run_code(file_check)


	
    #response1 = requests.request("POST", url1, data=payload1, headers=headers1)
    #token = json.loads(response1.text)['access_token']
    print(token)
    url = "https://apis.fedex.com/rate/v1/rates/quotes"
    headers = {
        'Content-Type': "application/json",
        'X-locale': "en_CA",
        'Authorization': 'Bearer '+ token
    }
    query1= {
        "accountNumber": {"value": "458975000"},
        "rateRequestControlParameters": {"returnTransitTimes": "true"},
        "requestedShipment": {
            "preferredCurrency": "CAD",
            "rateRequestType": ["PREFERRED"],
            "shipper": {
                "address": {
                    "postalCode": fromcode,
                    "countryCode": country
                }
            },
            "recipient": {
                "address": {
                    "postalCode": tocode,
                    "countryCode": country
                }
            },
            "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
            "packagingType": "YOUR_PACKAGING",
            "requestedPackageLineItems": [
                {
                    "subPackagingType": "BAG",
                    "groupPackageCount": noitems,
    
                    "weight": {
                        "units": "LB",
                        "value": mcweight
                    },
                    "dimensions": {
                        "length": length,
                        "width": width,
                        "height": height,
                        "units": "IN"
                    }
                },
                {
                    "subPackagingType": "BAG",
                    "groupPackageCount": noitems2,
    
                    "weight": {
                        "units": "LB",
                        "value": mcweight2
                    },
                    "dimensions": {
                        "length": length2,
                        "width": width2,
                        "height": height2,
                        "units": "IN"
                    }
                },
                # Add more packages as needed
            ]
        }
    }
    # query1 = {"accountNumber": {"value": "458975000"},"rateRequestControlParameters": {"returnTransitTimes": "true",},"requestedShipment": {"preferredCurrency": "CAD","rateRequestType": ["PREFERRED"],"shipper": {"address": {"postalCode": fromcode,"countryCode": "CA"}},"recipient": {"address": {"postalCode": tocode,"countryCode": country}},"pickupType": "DROPOFF_AT_FEDEX_LOCATION","packagingType": "YOUR_PACKAGING","requestedPackageLineItems": [{ "weight": {"units": "LB","value": mcweight},}]}}
   
    query1 = json.dumps(query1)
    try:
        response2 = requests.request("POST", url, data=query1, headers=headers)
        response3 = response2.json()
        print(response3)
        # print(response3['output']['rateReplyDetails'][1])
        
        for i in response3['output']['rateReplyDetails']:
            if "transitDays" in i["commit"]:
                temp={
                    "Provider":"Fedex",
                    "Service Type": i['serviceName'],
                    'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                    "From":pcdb[(i["commit"]['derivedOriginDetail']['postalCode'])[0:3].upper()].city,
                    "To":pcdb[(i["commit"]['derivedDestinationDetail']['postalCode'])[0:3].upper()].city,
                    "QuoteTotal":i['ratedShipmentDetails'][0]['totalNetFedExCharge'],
                    "No of days for delivery (Estimated)":i["commit"]["transitDays"]['description'],
                    "No of items":int(noitems)+int(noitems2),
                    "weight":int(mcweight)+int(mcweight2)
                }
            else:
                temp={
                    "Provider":"Fedex",
                    "Service Type": i['serviceName'],
                    'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                    "From":pcdb[(i["commit"]['derivedOriginDetail']['postalCode'])[0:3].upper()].city,
                    "To":pcdb[(i["commit"]['derivedDestinationDetail']['postalCode'])[0:3].upper()].city,
                    "QuoteTotal":i['ratedShipmentDetails'][0]['totalNetFedExCharge'],
                    "No of days for delivery (Estimated)":"1",
                    "No of items":int(noitems)+int(noitems2),
                    "weight":int(mcweight)+int(mcweight2)
                }
            temp_tax={
                "Provider":"Fedex",
                "Service Type": i['serviceName'],
                "Description":i['ratedShipmentDetails'][0]['shipmentRateDetail']['surCharges'][0]['description'],
                "Amount":i['ratedShipmentDetails'][0]['shipmentRateDetail']['surCharges'][0]['amount']
            }
            temp_tax_2={
                "Provider":"Fedex",
                "Service Type": i['serviceName'],
                "Description":i['ratedShipmentDetails'][0]['shipmentRateDetail']['taxes'][0]['description'],
                "Amount":i['ratedShipmentDetails'][0]['shipmentRateDetail']['taxes'][0]['amount']
            }
            fedex_tax.append(temp_tax)
            fedex_tax.append(temp_tax_2)
            fedex_data.append(temp)
    except Exception as e:
        send_error_email(str(e),"Fedex")
        print(e)

    print(fedex_data)
    print("tax")
    print(fedex_tax)
    fedex_data=pd.DataFrame(fedex_data)
    fedex_tax=pd.DataFrame(fedex_tax)
    return fedex_data,fedex_tax


# test1=fedex_test_multiple("E3B3V5","E3B4C3","10","30","CA","30", "40", "20", "2", "40", "40", "30", "25")
# test2=fedex_test("E3B3V5","E3B4C3","10","30","CA","30", "40", "20")

# print(test1)
# print(test2)


def fedex_test_list(fromcode,tocode,noitems,mcweight,country,length, width, height,from_loc,to_loc):

    fedex_data=[]
    fedex_tax=[]


    
    # fromcode="E3B3V5"
    # tocode="E3B4C3"
    # country ="CA"
    # mcweight=8

    
    tkn = "token"
    pcdb = PostalCodeDatabase()


    file_check = check_folder_and_set_variable()
    print (file_check)

    token = check_folder_and_run_code(file_check)

    item=[]
    totalweight=0
    totalitems=0

    for i in range(len(length)):
        temp={
                    "subPackagingType": "BAG",
                    "groupPackageCount": 1,
    
                    "weight": {
                        "units": "LB",
                        "value": mcweight[i]
                    },
                    "dimensions": {
                        "length": length[i],
                        "width": width[i],
                        "height": height[i],
                        "units": "IN"
                    }
                }
        item.append(temp)
        totalweight += float(mcweight[i])
        totalitems += int(noitems[i])





	
    #response1 = requests.request("POST", url1, data=payload1, headers=headers1)
    #token = json.loads(response1.text)['access_token']
    print(token)
    url = "https://apis.fedex.com/rate/v1/rates/quotes"
    headers = {
        'Content-Type': "application/json",
        'X-locale': "en_CA",
        'Authorization': 'Bearer '+ token
    }

    query1= {
        "accountNumber": {"value": "458975000"},
        "rateRequestControlParameters": {"returnTransitTimes": "true"},
        "requestedShipment": {
            "preferredCurrency": "CAD",
            "rateRequestType": ["PREFERRED"],
            "shipper": {
                "address": {
                    "postalCode": fromcode,
                    "countryCode": country
                }
            },
            "recipient": {
                "address": {
                    "postalCode": tocode,
                    "countryCode": country
                }
            },
            "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
            "packagingType": "YOUR_PACKAGING",
            "requestedPackageLineItems": item
        }
    }
    # query1 = {"accountNumber": {"value": "458975000"},"rateRequestControlParameters": {"returnTransitTimes": "true",},"requestedShipment": {"preferredCurrency": "CAD","rateRequestType": ["PREFERRED"],"shipper": {"address": {"postalCode": fromcode,"countryCode": "CA"}},"recipient": {"address": {"postalCode": tocode,"countryCode": country}},"pickupType": "DROPOFF_AT_FEDEX_LOCATION","packagingType": "YOUR_PACKAGING","requestedPackageLineItems": [{ "weight": {"units": "LB","value": mcweight},}]}}
   
    query1 = json.dumps(query1)
    try:
        response2 = requests.request("POST", url, data=query1, headers=headers)
        response3 = response2.json()
        print(response3)
        # print(response3['output']['rateReplyDetails'][1])
        
        for i in response3['output']['rateReplyDetails']:
            if "transitDays" in i["commit"]:
                temp={
                    "Provider":"Fedex",
                    "Service Type": i['serviceName'],
                    'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                    "From":from_loc,
                    "To":to_loc,
                    "QuoteTotal":i['ratedShipmentDetails'][0]['totalNetFedExCharge'],
                    "No of days for delivery (Estimated)":i["commit"]["transitDays"]['description'],
                    "No of items":totalitems,
                    "weight":totalweight
                }
            else:
                temp={
                    "Provider":"Fedex",
                    "Service Type": i['serviceName'],
                    'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                    "From":from_loc,
                    "To":to_loc,
                    "QuoteTotal":i['ratedShipmentDetails'][0]['totalNetFedExCharge'],
                    "No of days for delivery (Estimated)":"1",
                    "No of items":totalitems,
                    "weight": totalweight
                }
            temp_tax={
                "Provider":"Fedex",
                "Service Type": i['serviceName'],
                "Description":i['ratedShipmentDetails'][0]['shipmentRateDetail']['surCharges'][0]['description'],
                "Amount":i['ratedShipmentDetails'][0]['shipmentRateDetail']['surCharges'][0]['amount']
            }
            temp_tax_2={
                "Provider":"Fedex",
                "Service Type": i['serviceName'],
                "Description":i['ratedShipmentDetails'][0]['shipmentRateDetail']['taxes'][0]['description'],
                "Amount":i['ratedShipmentDetails'][0]['shipmentRateDetail']['taxes'][0]['amount']
            }
            fedex_tax.append(temp_tax)
            fedex_tax.append(temp_tax_2)
            fedex_data.append(temp)
    except Exception as e:
        send_error_email(str(e),"Fedex")
        print(e)

    print(fedex_data)
    print("tax")
    print(fedex_tax)
    fedex_data=pd.DataFrame(fedex_data)
    fedex_tax=pd.DataFrame(fedex_tax)
    return fedex_data,fedex_tax


# fromcode = 'K1A0B1'
# tocode = 'V5H2N2'
# noitems = ['7', '8', '5']
# mcweight = ['30', '40', '50']
# length =['20', '15', '30']
# width = ['10', '10', '10']
# height = ['15', '10', '20']
# # from_loc = 'Ottawa'
# # to_loc = 'Vancouver'
# country="CA"

# data,tax = fedex_test_list(fromcode, tocode, noitems, mcweight,country, length, width, height)
# print(data,tax)
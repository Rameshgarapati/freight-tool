from typing import Counter
from zipfile import ZIP_FILECOUNT_LIMIT
from flask import Flask, render_template, request
import pandas as pd
import json
from pandas.core.dtypes.missing import notnull
import requests
import numpy as np
# from suds.client import Client
from pypostalcode import PostalCodeDatabase
# import xmltodict
# from uszipcode import SearchEngine, SimpleZipcode
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from threading import Timer
from fedex_token import check_folder_and_set_variable
from fedex_token import check_folder_and_run_code
from counter import read_counter
from counter import update_counter


from datetime import datetime
from datetime import date
from xml.etree.ElementTree import XML, fromstring

import requests
from requests.structures import CaseInsensitiveDict
import json
# from suds.client import Client
# import xmltodict
from pypostalcode import PostalCodeDatabase

from xml.etree.ElementTree import XML, fromstring
import xml
import pandas as pd
# from suds.sax.text import Raw
import threading  
import time
from log import log_terminal_activities
from general_def import fastest_object_to_dict,zco,zcon,DecimalEncoder
from Midland_test import get_rate_quotes_and_charges,get_rate_quotes_and_charges_multiple,get_rate_quotes_and_charges_list
import os
from fedex_test import fedex_test, fedex_test_multiple,fedex_test_list
from Manitulin_test import manitulin_test,manitulin_test_multiple,manitulin_test_list
from Day_and_Ross import day_and_Ross,day_and_Ross_multiple,day_and_Ross_list
from ups import ups_rates,ups_rates_multiple,ups_rates_list
from canada_post import canada_post_rate,canada_post_rate_list
from pulorator import pulorator,pulorator_list

# Example usage




# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/', methods=['GET', 'POST'])

def home():
    


    counter_filename = "visitor_counter.txt"

# Read the current counter value
    current_counter = read_counter(counter_filename)
    print(f"Current visitor count: {current_counter}")

# Increment the counter (e.g., when a new visitor arrives)
    new_counter = current_counter + 1

# Update the counter value in the file
    update_counter(counter_filename, new_counter)


    accountno = request.form.get("account")
    # mcweight = request.form.get("mcweight")
    # height = request.form.get("height")
    # length = request.form.get("length")
    # width = request.form.get("width")
    noitems = request.form.getlist('noitems[]')
    mcweight = request.form.getlist('mcweight[]')
    length = request.form.getlist('length[]')
    width = request.form.getlist('width[]')
    height = request.form.getlist('height[]')
    country = request.form.get("Country")
    tocode = request.form.get("tocode")
    tocode1 = request.form.get("tocode1")
    city1 = request.form.get("City1")
    # noitems = request.form.get("noitems")
    fromcode = request.form.get("fromcode")
    Date = request.form.get("Date")
    height2 = request.form.get("height2")
    length2 = request.form.get("length2")
    width2 = request.form.get("width2")
    noitems2 = request.form.get("noitems2")
    mcweight2 = request.form.get("mcweight2")


    from_loc=fromcode
    to_loc=tocode


    print(length,height,width,mcweight,noitems,country)
    
    token=""
    quote_records=pd.DataFrame()
    charges_df=pd.DataFrame()
    print(mcweight2,noitems2,length2,width2,height2,mcweight)
    
    try:
        charges_df,quote_records = get_rate_quotes_and_charges_list(fromcode,tocode,noitems,mcweight,length,width,height)
        
        if not charges_df.empty:
            from_loc=charges_df["From"][0]
            to_loc=charges_df["To"][0]
            print(from_loc,to_loc)
        fedex_data,fedex_tax=fedex_test_list(fromcode,tocode,noitems,mcweight,country,length, width, height,from_loc,to_loc)
        print(type(fedex_data))
        charges_df = pd.concat([charges_df, fedex_data], ignore_index=True, sort=False)
            # charges_df=charges_df.append(fedex_data,ignore_index=True)
        quote_records = pd.concat([quote_records, fedex_tax], ignore_index=True, sort=False)
        
        try:
            manitulin_data,manitulin_tax=manitulin_test_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc)
            charges_df=pd.concat([charges_df,manitulin_data],ignore_index=True, sort=False)
            quote_records=pd.concat([quote_records,manitulin_tax],ignore_index=True, sort=False)
        except Exception as e:
            print("Manitulin error",e)

        
        try:
            DandR_data, DandR_tax=day_and_Ross_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc)
            
            charges_df=pd.concat([charges_df,DandR_tax],ignore_index=True, sort=False)
            quote_records=pd.concat([quote_records,DandR_data],ignore_index=True, sort=False)
        except Exception as e:
            print("Day and Ross error",e)
        

        try:
            print("ups_data")
            ups_data,ups_tax=ups_rates_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc)
            charges_df=pd.concat([charges_df,ups_tax],ignore_index=True, sort=False)
            quote_records=pd.concat([quote_records,ups_data],ignore_index=True, sort=False)

        except Exception as e:
            print("Ups error :",e)

        try:
            print("Canada_post_data")
            canada_post_data,canada_post_tax=canada_post_rate_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc)
            charges_df=pd.concat([charges_df,canada_post_data],ignore_index=True, sort=False)
            quote_records=pd.concat([quote_records,canada_post_tax],ignore_index=True, sort=False)

        except Exception as e:
            print("Canada post error :",e)

        try:
            print("Purolator Data")
            purolator_post_data,purolator_post_tax=pulorator_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc)
            charges_df=pd.concat([charges_df,purolator_post_data],ignore_index=True, sort=False)
            quote_records=pd.concat([quote_records,purolator_post_tax],ignore_index=True, sort=False)

        except Exception as e:
            print("purolator post error :",e)

        file_check = check_folder_and_set_variable()
        print (file_check)

        token = check_folder_and_run_code(file_check)
        

        print(charges_df,quote_records)



        #     # Example usage
        #     print(type(charges_df))
        #     fedex_data,fedex_tax=fedex_test_list(fromcode,tocode,noitems,mcweight,country,length, width, height)
        #     print(type(fedex_data))
        #     charges_df = pd.concat([charges_df, fedex_data], ignore_index=True, sort=False)
        #     # charges_df=charges_df.append(fedex_data,ignore_index=True)
        #     quote_records = pd.concat([quote_records, fedex_tax], ignore_index=True, sort=False)
        #     # quote_records=quote_records.append(fedex_tax,ignore_index=True)
            
        #     if(fromcode!= None):
        #         try:
        #             manitulin_data,manitulin_tax=manitulin_test_list(fromcode,tocode,noitems,mcweight,length,width,height)
        #             charges_df=pd.concat([charges_df,manitulin_data],ignore_index=True, sort=False)
        #             quote_records=pd.concat([quote_records,manitulin_tax],ignore_index=True, sort=False)
        #         except Exception as e:
        #             print("no data",e)
        #         DandR_data, DandR_tax=day_and_Ross_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc)
        #         print("Day and ross",DandR_data,DandR_tax)
        #         charges_df=pd.concat([charges_df,DandR_tax],ignore_index=True, sort=False)
        #         quote_records=pd.concat([quote_records,DandR_data],ignore_index=True, sort=False)

        #         try:
        #             print("ups_data")
        #             ups_data,ups_tax=ups_rates_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc)
        #             charges_df=pd.concat([charges_df,ups_tax],ignore_index=True, sort=False)
        #             quote_records=pd.concat([quote_records,ups_data],ignore_index=True, sort=False)

        #         except Exception as e:
        #             print("Ups error :",e)

        #         try:
        #             print("Canada_post_data")
        #             canada_post_data,canada_post_tax=canada_post_rate_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc)
        #             charges_df=pd.concat([charges_df,canada_post_data],ignore_index=True, sort=False)
        #             quote_records=pd.concat([quote_records,canada_post_tax],ignore_index=True, sort=False)

        #         except Exception as e:
        #             print("Canada post error :",e)


        #         try:
        #             print("Purolator Data")
        #             purolator_post_data,purolator_post_tax=pulorator_list(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc)
        #             charges_df=pd.concat([charges_df,purolator_post_data],ignore_index=True, sort=False)
        #             quote_records=pd.concat([quote_records,purolator_post_tax],ignore_index=True, sort=False)

        #         except Exception as e:
        #             print("purolator post error :",e)



        #     file_check = check_folder_and_set_variable()
        #     print (file_check)

        #     token = check_folder_and_run_code(file_check)
        # else:
        #     charges_df,quote_records = get_rate_quotes_and_charges_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2, mcweight2, length2, width2, height2)
        
        #     if not charges_df.empty:
        #         from_loc=charges_df["From"][0]
        #         to_loc=charges_df["To"][0]
        #         print(from_loc,to_loc)
        #     # Example usage
        #     print(type(charges_df))
        #     fedex_data,fedex_tax=fedex_test_multiple(fromcode,tocode,noitems,mcweight,country,length, width, height,noitems2, mcweight2, length2, width2, height2)
        #     print(type(fedex_data))
        #     charges_df = pd.concat([charges_df, fedex_data], ignore_index=True, sort=False)
        #     # charges_df=charges_df.append(fedex_data,ignore_index=True)
        #     quote_records = pd.concat([quote_records, fedex_tax], ignore_index=True, sort=False)
        #     # quote_records=quote_records.append(fedex_tax,ignore_index=True)
            
        #     if(fromcode!= None):
        #         try:
        #             manitulin_data,manitulin_tax=manitulin_test_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2)
        #             charges_df=pd.concat([charges_df,manitulin_data],ignore_index=True, sort=False)
        #             quote_records=pd.concat([quote_records,manitulin_tax],ignore_index=True, sort=False)
        #         except Exception as e:
        #             print("no data",e)
        #         DandR_data, DandR_tax=day_and_Ross_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2,from_loc,to_loc)
        #         print("Day and ross",DandR_data,DandR_tax)
        #         charges_df=pd.concat([charges_df,DandR_tax],ignore_index=True, sort=False)
        #         quote_records=pd.concat([quote_records,DandR_data],ignore_index=True, sort=False)

        #         try:
        #             print("ups_data")
        #             ups_data,ups_tax=ups_rates_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2,from_loc,to_loc)
        #             charges_df=pd.concat([charges_df,ups_tax],ignore_index=True, sort=False)
        #             quote_records=pd.concat([quote_records,ups_data],ignore_index=True, sort=False)

        #         except Exception as e:
        #             print("Ups error :",e)

        #         try:
        #             print("Purolator Data")
        #             purolator_post_data,purolator_post_tax=pulorator(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2,from_loc,to_loc)
        #             charges_df=pd.concat([charges_df,purolator_post_data],ignore_index=True, sort=False)
        #             quote_records=pd.concat([quote_records,purolator_post_tax],ignore_index=True, sort=False)

        #         except Exception as e:
        #             print("purolator post error :",e)



        #     file_check = check_folder_and_set_variable()
        #     print (file_check)

        #     token = check_folder_and_run_code(file_check)
    except Exception as e:
        print(e)


	
    #response1 = requests.request("POST", url1, data=payload1, headers=headers1)
    #token = json.loads(response1.text)['access_token']
    print(token)
    url = "https://apis.fedex.com/rate/v1/rates/quotes"
    headers = {
    'Content-Type': "application/json",
    'X-locale': "en_CA",
    'Authorization': 'Bearer '+ token}

    return render_template('home.html',tables=[quote_records.to_html(classes='data', header="true",index = False)],tables1=[charges_df.to_html(classes='data', header="true",index = False)])

if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost',4449,debug=True)
    log_filename = "terminal_activities.log"
    log_terminal_activities(log_filename)

    #app.run('10.37.4.40',5800)
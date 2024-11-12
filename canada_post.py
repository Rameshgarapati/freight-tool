# import requests
# from requests.auth import HTTPBasicAuth
# import xml.etree.ElementTree as ET
# from datetime import datetime

# Replace with your own credentials
username = 'ff1a950cfa2a67e7'
password = 'b363d2f61540bfeb013dca'
customer_number = '0007209467'
contract_id = ''

# def days_between_dates(date1, date2):
#     # Convert the string dates to datetime objects
#     date_format = "%Y-%m-%d"
#     d1 = datetime.strptime(date1, date_format)
#     d2 = datetime.strptime(date2, date_format)
    
#     # Calculate the difference in days
#     delta = d2 - d1
#     return delta.days


# def canada_post_rate(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc):
#     # Canada Post API endpoint for rating
#     final_rates=[]
#     final_tax=[]

#     url = 'https://soa-gw.canadapost.ca/rs/ship/price'

#     # Sample payload for rating request

#     parcel_characteristics = ""
#     for _ in range(noitems):
#         parcel_characteristics += f"""
#         <parcel-characteristics>
#             <weight>{mcweight}</weight>
#             <dimensions>
#                 <length>{length}</length>
#                 <width>{width}</width>
#                 <height>{height}</height>
#             </dimensions>
#         </parcel-characteristics>
#         """

#     payload = f"""
#     <mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v4">
#         <customer-number>{customer_number}</customer-number>
#         {parcel_characteristics}
#         <origin-postal-code>{fromcode}</origin-postal-code>
#         <destination>
#             <domestic>
#                 <postal-code>{tocode}</postal-code>
#             </domestic>
#         </destination>
#     </mailing-scenario>
#     """


#     headers = {
#         'Content-Type': 'application/vnd.cpc.ship.rate-v4+xml',
#         'Accept': 'application/vnd.cpc.ship.rate-v4+xml'
#     }

#     response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, data=payload)

#     if response.status_code == 200:
#         print(response.text)
#     else:
#         print(f"Error: {response.status_code}")
#         print(response.text)




#     # Parse the XML data
#     root = ET.fromstring(response.text)

#     # Define the namespace
#     namespace = {'ns': 'http://www.canadapost.ca/ws/ship/rate-v4'}

#     # Extract details
#     for price_quote in root.findall('ns:price-quote', namespace):
#         service_code = price_quote.find('ns:service-code', namespace).text
#         service_name = price_quote.find('ns:service-name', namespace).text
#         base_price = price_quote.find('ns:price-details/ns:base', namespace).text
#         gst = price_quote.find('ns:price-details/ns:taxes/ns:gst', namespace).text
#         pst = price_quote.find('ns:price-details/ns:taxes/ns:pst', namespace).text
#         hst = price_quote.find('ns:price-details/ns:taxes/ns:hst', namespace).text
#         due = price_quote.find('ns:price-details/ns:due', namespace).text
#         fuel_surcharge = price_quote.find('ns:price-details/ns:adjustments/ns:adjustment[ns:adjustment-code="FUELSC"]/ns:adjustment-cost', namespace).text
#         delivery_date = price_quote.find('ns:service-standard/ns:expected-delivery-date', namespace).text

        



#         temp_rate={
#             "Provider":"Canada Post",
#             "Service Type": service_name,
#             'ShipDate': datetime.today().strftime('%Y-%m-%d'),
#             "From":from_loc,
#             "To":to_loc,
#             "QuoteTotal":due,
#             "Delivery Date (Estimated)":delivery_date,
#             "No of days for delivery (Estimated)": days_between_dates(datetime.today().strftime('%Y-%m-%d'),delivery_date),
#             "No of items":noitems,
#             "weight":mcweight
#         }
#         if float(gst)>0.00:
#             temp_tax={
#                 "Provider":"Canada Post",
#                 "Service Type": service_name,
#                 "Description":"GST",
#                 "Amount":gst
#             }
#             final_tax.append(temp_tax)
                    
#         if float(hst)>0.00:
#             temp_tax={
#                 "Provider":"Canada Post",
#                 "Service Type": service_name,
#                 "Description":"HST",
#                 "Amount":hst
#             }
#             final_tax.append(temp_tax)

#         if float(pst)>0.00:
#             temp_tax={
#                 "Provider":"Canada Post",
#                 "Service Type": service_name,
#                 "Description":"PST",
#                 "Amount":pst
#             }
#             final_tax.append(temp_tax)
#         if float(fuel_surcharge)>0.00:
#             temp_tax={
#                 "Provider":"Canada Post",
#                 "Service Type": service_name,
#                 "Description":"Fuel Surcharge",
#                 "Amount":fuel_surcharge
#             }
#             final_tax.append(temp_tax)

                
#         final_rates.append(temp_rate)

import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
from error_mail import send_error_email

def days_between_dates(date1, date2):
    # Convert the string dates to datetime objects
    date_format = "%Y-%m-%d"
    d1 = datetime.strptime(date1, date_format)
    d2 = datetime.strptime(date2, date_format)
    
    # Calculate the difference in days
    delta = d2 - d1
    return delta.days

def canada_post_rate(fromcode, tocode, noitems, mcweight, length, width, height, from_loc, to_loc):
    try:
        # Canada Post API endpoint for rating
        final_rates = []
        final_tax = []
        # mcweight=float(mcweight)*int(noitems)
        # length=float(length)*int(noitems)
        # width=float(width)*int(noitems)
        # height=float(height)*int(noitems)

        url = 'https://soa-gw.canadapost.ca/rs/ship/price'

        # Sample payload for rating request
        parcel_characteristics = ""
        for _ in range(int(noitems)):
            parcel_characteristics += f"""
            <parcel-characteristics>
                <weight>{mcweight}</weight>
                <dimensions>
                    <length>{length}</length>
                    <width>{width}</width>
                    <height>{height}</height>
                </dimensions>
            </parcel-characteristics>
            """

        payload = f"""
        <mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v4">
            <customer-number>{customer_number}</customer-number>
            <parcel-characteristics>
                <weight>{str((mcweight))}</weight>
                <dimensions>
                    <length>{str(length)}</length>
                    <width>{str(width)}</width>
                    <height>{str(height)}</height>
                </dimensions>
                
            </parcel-characteristics>
            <origin-postal-code>{fromcode}</origin-postal-code>
            <destination>
                <domestic>
                    <postal-code>{tocode}</postal-code>
                </domestic>
            </destination>
        </mailing-scenario>
        """

        headers = {
            'Content-Type': 'application/vnd.cpc.ship.rate-v4+xml',
            'Accept': 'application/vnd.cpc.ship.rate-v4+xml'
        }

        response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, data=payload)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return {}

        # Parse the XML data
        root = ET.fromstring(response.text)

        # Define the namespace
        namespace = {'ns': 'http://www.canadapost.ca/ws/ship/rate-v4'}

        # Extract details
        for price_quote in root.findall('ns:price-quote', namespace):
            service_code = price_quote.find('ns:service-code', namespace).text
            service_name = price_quote.find('ns:service-name', namespace).text
            base_price = price_quote.find('ns:price-details/ns:base', namespace).text
            gst = price_quote.find('ns:price-details/ns:taxes/ns:gst', namespace).text
            pst = price_quote.find('ns:price-details/ns:taxes/ns:pst', namespace).text
            hst = price_quote.find('ns:price-details/ns:taxes/ns:hst', namespace).text
            due = price_quote.find('ns:price-details/ns:due', namespace).text
            fuel_surcharge = price_quote.find('ns:price-details/ns:adjustments/ns:adjustment[ns:adjustment-code="FUELSC"]/ns:adjustment-cost', namespace).text
            delivery_date = price_quote.find('ns:service-standard/ns:expected-delivery-date', namespace).text

            temp_rate = {
                "Provider": "Canada Post",
                "Service Type": service_name,
                'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                "From": from_loc,
                "To": to_loc,
                "QuoteTotal": due,
                "Delivery Date (Estimated)": delivery_date,
                "No of days for delivery (Estimated)": days_between_dates(datetime.today().strftime('%Y-%m-%d'), delivery_date),
                "No of items": noitems,
                "weight": mcweight
            }
            
            if float(gst) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "GST",
                    "Amount": gst
                }
                final_tax.append(temp_tax)
                        
            if float(hst) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "HST",
                    "Amount": hst
                }
                final_tax.append(temp_tax)

            if float(pst) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "PST",
                    "Amount": pst
                }
                final_tax.append(temp_tax)
                
            if float(fuel_surcharge) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "Fuel Surcharge",
                    "Amount": fuel_surcharge
                }
                final_tax.append(temp_tax)

            final_rates.append(temp_rate)

        if not final_rates:
            return pd.DataFrame(),pd.DataFrame()
        
        return pd.DataFrame(final_rates), pd.DataFrame(final_tax)

    except Exception as e:
        send_error_email(str(e),"Canada Post")
        print(f"An error occurred: {e}")
        return pd.DataFrame(),pd.DataFrame()
    


def canada_post_rate_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2,from_loc,to_loc):
    try:
        # Canada Post API endpoint for rating
        final_rates = []
        final_tax = []
        mcweight=float(mcweight)*int(noitems)
        length=float(length)*int(noitems)
        width=float(width)*int(noitems)
        height=float(height)*int(noitems)

        mcweight2=float(mcweight2)*int(noitems2)
        length2=float(length2)*int(noitems2)
        width2=float(width2)*int(noitems2)
        height2=float(height2)*int(noitems2)
        mcweight+=mcweight2
        length+=length2
        width+=width2
        height+=height2
        


        url = 'https://soa-gw.canadapost.ca/rs/ship/price'

        # Sample payload for rating request
        parcel_characteristics = ""
        for _ in range(int(noitems)):
            parcel_characteristics += f"""
            <parcel-characteristics>
                <weight>{mcweight}</weight>
                <dimensions>
                    <length>{length}</length>
                    <width>{width}</width>
                    <height>{height}</height>
                </dimensions>
            </parcel-characteristics>
            """

        payload = f"""
        <mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v4">
            <customer-number>{customer_number}</customer-number>
            <parcel-characteristics>
                <weight>{str((mcweight))}</weight>
                <dimensions>
                    <length>{str(length)}</length>
                    <width>{str(width)}</width>
                    <height>{str(height)}</height>
                </dimensions>
                
            </parcel-characteristics>
            <origin-postal-code>{fromcode}</origin-postal-code>
            <destination>
                <domestic>
                    <postal-code>{tocode}</postal-code>
                </domestic>
            </destination>
        </mailing-scenario>
        """

        headers = {
            'Content-Type': 'application/vnd.cpc.ship.rate-v4+xml',
            'Accept': 'application/vnd.cpc.ship.rate-v4+xml'
        }

        response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, data=payload)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return {}

        # Parse the XML data
        root = ET.fromstring(response.text)

        # Define the namespace
        namespace = {'ns': 'http://www.canadapost.ca/ws/ship/rate-v4'}

        # Extract details
        for price_quote in root.findall('ns:price-quote', namespace):
            service_code = price_quote.find('ns:service-code', namespace).text
            service_name = price_quote.find('ns:service-name', namespace).text
            base_price = price_quote.find('ns:price-details/ns:base', namespace).text
            gst = price_quote.find('ns:price-details/ns:taxes/ns:gst', namespace).text
            pst = price_quote.find('ns:price-details/ns:taxes/ns:pst', namespace).text
            hst = price_quote.find('ns:price-details/ns:taxes/ns:hst', namespace).text
            due = price_quote.find('ns:price-details/ns:due', namespace).text
            fuel_surcharge = price_quote.find('ns:price-details/ns:adjustments/ns:adjustment[ns:adjustment-code="FUELSC"]/ns:adjustment-cost', namespace).text
            delivery_date = price_quote.find('ns:service-standard/ns:expected-delivery-date', namespace).text

            temp_rate = {
                "Provider": "Canada Post",
                "Service Type": service_name,
                'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                "From": from_loc,
                "To": to_loc,
                "QuoteTotal": due,
                "Delivery Date (Estimated)": delivery_date,
                "No of days for delivery (Estimated)": days_between_dates(datetime.today().strftime('%Y-%m-%d'), delivery_date),
                "No of items": noitems,
                "weight": mcweight
            }
            
            if float(gst) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "GST",
                    "Amount": gst
                }
                final_tax.append(temp_tax)
                        
            if float(hst) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "HST",
                    "Amount": hst
                }
                final_tax.append(temp_tax)

            if float(pst) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "PST",
                    "Amount": pst
                }
                final_tax.append(temp_tax)
                
            if float(fuel_surcharge) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "Fuel Surcharge",
                    "Amount": fuel_surcharge
                }
                final_tax.append(temp_tax)

            final_rates.append(temp_rate)

        if not final_rates:
            return pd.DataFrame(),pd.DataFrame()
        
        return pd.DataFrame(final_rates), pd.DataFrame(final_tax)

    except Exception as e:
        send_error_email(str(e),"Canada Post")
        print(f"An error occurred: {e}")
        return pd.DataFrame(),pd.DataFrame()
    


def canada_post_rate_list(fromcode, tocode, noitems, mcweight, length, width, height, from_loc, to_loc):
    try:
        # Canada Post API endpoint for rating
        final_rates = []
        final_tax = []

        finallength=0
        finalwidth=0
        finalheight=0
        finalweight=0
        totalitems=0
        totalweight=0

        for i in range(len(length)):
            finalweight += (float(mcweight[i])*int(noitems[i]))
            finallength += (int(length[i])*int(noitems[i]))
            finalwidth  += (int(width[i])*int(noitems[i]))
            finalheight += (int(height[i])*int(noitems[i]))
            totalitems  += int(noitems[i])
            totalweight += float(mcweight[i])



        # mcweight=float(mcweight)*int(noitems)
        # length=float(length)*int(noitems)
        # width=float(width)*int(noitems)
        # height=float(height)*int(noitems)

        url = 'https://soa-gw.canadapost.ca/rs/ship/price'

        # Sample payload for rating request
        # parcel_characteristics = ""
        # for _ in range(int(noitems)):
        #     parcel_characteristics += f"""
        #     <parcel-characteristics>
        #         <weight>{mcweight}</weight>
        #         <dimensions>
        #             <length>{length}</length>
        #             <width>{width}</width>
        #             <height>{height}</height>
        #         </dimensions>
        #     </parcel-characteristics>
        #     """

        payload = f"""
        <mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v4">
            <customer-number>{customer_number}</customer-number>
            <parcel-characteristics>
                <weight>{str((finalweight))}</weight>
                <dimensions>
                    <length>{str(finallength)}</length>
                    <width>{str(finalwidth)}</width>
                    <height>{str(finalheight)}</height>
                </dimensions>
                
            </parcel-characteristics>
            <origin-postal-code>{fromcode}</origin-postal-code>
            <destination>
                <domestic>
                    <postal-code>{tocode}</postal-code>
                </domestic>
            </destination>
        </mailing-scenario>
        """

        headers = {
            'Content-Type': 'application/vnd.cpc.ship.rate-v4+xml',
            'Accept': 'application/vnd.cpc.ship.rate-v4+xml'
        }

        response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, data=payload)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return {}

        # Parse the XML data
        root = ET.fromstring(response.text)

        # Define the namespace
        namespace = {'ns': 'http://www.canadapost.ca/ws/ship/rate-v4'}

        # Extract details
        for price_quote in root.findall('ns:price-quote', namespace):
            service_code = price_quote.find('ns:service-code', namespace).text
            service_name = price_quote.find('ns:service-name', namespace).text
            base_price = price_quote.find('ns:price-details/ns:base', namespace).text
            gst = price_quote.find('ns:price-details/ns:taxes/ns:gst', namespace).text
            pst = price_quote.find('ns:price-details/ns:taxes/ns:pst', namespace).text
            hst = price_quote.find('ns:price-details/ns:taxes/ns:hst', namespace).text
            due = price_quote.find('ns:price-details/ns:due', namespace).text
            fuel_surcharge = price_quote.find('ns:price-details/ns:adjustments/ns:adjustment[ns:adjustment-code="FUELSC"]/ns:adjustment-cost', namespace).text
            delivery_date = price_quote.find('ns:service-standard/ns:expected-delivery-date', namespace).text

            temp_rate = {
                "Provider": "Canada Post",
                "Service Type": service_name,
                'ShipDate': datetime.today().strftime('%Y-%m-%d'),
                "From": from_loc,
                "To": to_loc,
                "QuoteTotal": due,
                "Delivery Date (Estimated)": delivery_date,
                "No of days for delivery (Estimated)": days_between_dates(datetime.today().strftime('%Y-%m-%d'), delivery_date),
                "No of items": totalitems,
                "weight": totalweight
            }
            
            if float(gst) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "GST",
                    "Amount": gst
                }
                final_tax.append(temp_tax)
                        
            if float(hst) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "HST",
                    "Amount": hst
                }
                final_tax.append(temp_tax)

            if float(pst) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "PST",
                    "Amount": pst
                }
                final_tax.append(temp_tax)
                
            if float(fuel_surcharge) > 0.00:
                temp_tax = {
                    "Provider": "Canada Post",
                    "Service Type": service_name,
                    "Description": "Fuel Surcharge",
                    "Amount": fuel_surcharge
                }
                final_tax.append(temp_tax)

            final_rates.append(temp_rate)

        if not final_rates:
            return pd.DataFrame(),pd.DataFrame()
        
        return pd.DataFrame(final_rates), pd.DataFrame(final_tax)

    except Exception as e:
        send_error_email(str(e),"Canada Post")
        print(f"An error occurred: {e}")
        return pd.DataFrame(),pd.DataFrame()


# fromcode = 'K1A0B1'
# tocode = 'V5H2N2'
# noitems = ["2","3"]
# mcweight = ["1.0","2.0"]
# length = ["10","10"]
# width = ["10","10"]
# height = ["10","10"]
# from_loc = 'Ottawa'
# to_loc = 'Vancouver'

# rates_info = canada_post_rate_list(fromcode, tocode, noitems, mcweight, length, width, height, from_loc, to_loc)
# print(rates_info)
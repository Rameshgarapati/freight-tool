import requests
import pandas as pd
from error_mail import send_error_email

def get_rate_quotes_and_charges(fromcode, tocode, noitems, mcweight, length, width, height):
    try:
        if fromcode is not None:
            query = {
                'RateQuoteReq': {
                    'RateQuoteRequest': [{'ShipZip': fromcode, 'ConsZip': tocode}],
                    'RateQuoteReqLine': [{'Weight': mcweight, 'Pieces': noitems, 'Height': height, 'Length': length, 'Width': width}],
                    "RateQuoteReqLineDim": [{"QuoteLineNo": "1","DimLineNo": "1","DimUnits": "in","UnitLength": length,"UnitHeight": height,"UnitWidth": width,"UnitCount": noitems}
                                            ,{"QuoteLineNo": "2","DimLineNo": "2","DimUnits": "in","UnitLength": length,"UnitHeight": height,"UnitWidth": width,"UnitCount": noitems}],
                    'RateQuoteReqAcc': [{'accountno': 245}]
                }
            }

            
            
            response = requests.post('https://apigateway.jdirving.com/gateway/MidlandGetRateQuote/1.0.0/RateQuote?APIkey=52cdcc02-23e7-430c-99a4-8e8fa87583fc', json=query)
            print(response)
            if response.status_code == 200:
            
                response = response.json()

                quote_records = []
                for quote in response['RateQuote']:
                    quote_record = {
                    'Provider': 'Midland Courier',
                    'Service Type': quote['ServTypeDescTranslated'],
                    'ShipDate': quote['ShipDate'],
                    'From': f"{quote['ShipCity']}, {quote['ShipState']} ({quote['ShipZip']})",
                    'To': f"{quote['ConsCity']}, {quote['ConsState']} ({quote['ConsZip']})",
                    'QuoteTotal': quote['QuoteTotal'],
                    'Delivery Date (Estimated)': quote['EstDelDate'],
                    'No of days for delivery (Estimated)': quote['TransitDays'],
                    'No of items': quote['TotalPieces'],
                    'weight':mcweight,
                    'Charges': quote['RateQuoteCharge']
                    }
                    quote_records.append(quote_record)

            # Create a DataFrame from the quote records
                df = pd.DataFrame(quote_records)
                df = df.drop(columns=['Charges'])

            # Extract charges data from the quote records
                charges_records = []
                for quote_record in quote_records:
                    for charge in quote_record['Charges']:
                        charge_record = {
                        'Provider': quote_record['Provider'],
                        'Service Type': quote_record['Service Type'],
                        'ChargeLineNo': charge['ChargeLineNo'],
                        'Description': charge['ChargeDesc'],
                        'Amount': charge['ChargeAmount']
                        }
                        charges_records.append(charge_record)

            # Create a DataFrame for charges
                charges_df = pd.DataFrame(charges_records)

                return df, charges_df
            else:
                response = response.json()
                print(response)
                quote_records = pd.DataFrame()
                charges_df = pd.DataFrame()
                return quote_records , charges_df            
        else:
            quote_records = pd.DataFrame()
            charges_df = pd.DataFrame()
            return quote_records , charges_df
    except Exception as e:
        send_error_email(str(e),"Midland")
        print(e)
    
def get_rate_quotes_and_charges_multiple(fromcode, tocode, noitems, mcweight, length, width, height, noitems2, mcweight2, length2, width2, height2):
    try:
        if fromcode is not None:
            query = {
                'RateQuoteReq': {
                    'RateQuoteRequest': [{'ShipZip': fromcode, 'ConsZip': tocode}],
                    'RateQuoteReqLine': [{'Weight': mcweight, 'Pieces': noitems, 'Height': height, 'Length': length, 'Width': width},{'Weight': mcweight2, 'Pieces': noitems2, 'Height': height2, 'Length': length2, 'Width': width2}],
                    "RateQuoteReqLineDim": [{"QuoteLineNo": "1","DimLineNo": "1","DimUnits": "in","UnitLength": length,"UnitHeight": height,"UnitWidth": width,"UnitCount": noitems}
                                            ,{"QuoteLineNo": "2","DimLineNo": "2","DimUnits": "in","UnitLength": length2,"UnitHeight": height2,"UnitWidth": width2,"UnitCount": noitems2}],
                    'RateQuoteReqAcc': [{'accountno': 245}]
                }
            }

            
            
            response = requests.post('https://apigateway.jdirving.com/gateway/MidlandGetRateQuote/1.0.0/RateQuote?APIkey=52cdcc02-23e7-430c-99a4-8e8fa87583fc', json=query)
            print(response)
            if response.status_code == 200:
            
                response = response.json()

                quote_records = []
                for quote in response['RateQuote']:
                    quote_record = {
                    'Provider': 'Midland Courier',
                    'Service Type': quote['ServTypeDescTranslated'],
                    'ShipDate': quote['ShipDate'],
                    'From': f"{quote['ShipCity']}, {quote['ShipState']} ({quote['ShipZip']})",
                    'To': f"{quote['ConsCity']}, {quote['ConsState']} ({quote['ConsZip']})",
                    'QuoteTotal': quote['QuoteTotal'],
                    'Delivery Date (Estimated)': quote['EstDelDate'],
                    'No of days for delivery (Estimated)': quote['TransitDays'],
                    'No of items': quote['TotalPieces'],
                    'weight':int(mcweight)+int(mcweight2),
                    'Charges': quote['RateQuoteCharge']
                    }
                    quote_records.append(quote_record)

            # Create a DataFrame from the quote records
                df = pd.DataFrame(quote_records)
                df = df.drop(columns=['Charges'])

            # Extract charges data from the quote records
                charges_records = []
                for quote_record in quote_records:
                    for charge in quote_record['Charges']:
                        charge_record = {
                        'Provider': quote_record['Provider'],
                        'Service Type': quote_record['Service Type'],
                        'ChargeLineNo': charge['ChargeLineNo'],
                        'Description': charge['ChargeDesc'],
                        'Amount': charge['ChargeAmount']
                        }
                        charges_records.append(charge_record)

            # Create a DataFrame for charges
                charges_df = pd.DataFrame(charges_records)

                return df, charges_df
            else:
                response = response.json()
                print(response)
                quote_records = pd.DataFrame()
                charges_df = pd.DataFrame()
                return quote_records , charges_df            
        else:
            quote_records = pd.DataFrame()
            charges_df = pd.DataFrame()
            return quote_records , charges_df
    except Exception as e:
        send_error_email(str(e),"Midland")
        print(str(e))



def get_rate_quotes_and_charges_list(fromcode, tocode, noitems, mcweight, length, width, height):

    item=[]
    ratequote=[]
    totalweight=0
    totalitems=0
    for i in range(len(length)):
        temp={'Weight': mcweight[i], 'Pieces': noitems[i], 'Height': height[i], 'Length': length[i], 'Width': width[i]}
        temp2={"QuoteLineNo": "1","DimLineNo": "1","DimUnits": "in","UnitLength": length[i],"UnitHeight": height[i],"UnitWidth": width[i],"UnitCount": noitems[i]}
        item.append(temp)
        ratequote.append(temp2)
        totalweight += float(mcweight[i])
        totalitems += int(noitems[i])
                                            
    try:
        if fromcode is not None:
            query = {
                'RateQuoteReq': {
                    'RateQuoteRequest': [{'ShipZip': fromcode, 'ConsZip': tocode}],
                    'RateQuoteReqLine': item,
                    "RateQuoteReqLineDim": ratequote,
                    'RateQuoteReqAcc': [{'accountno': 245}]
                }
            }

            
            
            response = requests.post('https://apigateway.jdirving.com/gateway/MidlandGetRateQuote/1.0.0/RateQuote?APIkey=52cdcc02-23e7-430c-99a4-8e8fa87583fc', json=query)
            print(response)
            if response.status_code == 200:
            
                response = response.json()

                quote_records = []
                for quote in response['RateQuote']:
                    quote_record = {
                    'Provider': 'Midland Courier',
                    'Service Type': quote['ServTypeDescTranslated'],
                    'ShipDate': quote['ShipDate'],
                    'From': f"{quote['ShipCity']}, {quote['ShipState']} ({quote['ShipZip']})",
                    'To': f"{quote['ConsCity']}, {quote['ConsState']} ({quote['ConsZip']})",
                    'QuoteTotal': quote['QuoteTotal'],
                    'Delivery Date (Estimated)': quote['EstDelDate'],
                    'No of days for delivery (Estimated)': quote['TransitDays'],
                    'No of items': quote['TotalPieces'],
                    'weight':totalweight,
                    'Charges': quote['RateQuoteCharge']
                    }
                    quote_records.append(quote_record)

            # Create a DataFrame from the quote records
                df = pd.DataFrame(quote_records)
                df = df.drop(columns=['Charges'])

            # Extract charges data from the quote records
                charges_records = []
                for quote_record in quote_records:
                    for charge in quote_record['Charges']:
                        charge_record = {
                        'Provider': quote_record['Provider'],
                        'Service Type': quote_record['Service Type'],
                        'ChargeLineNo': charge['ChargeLineNo'],
                        'Description': charge['ChargeDesc'],
                        'Amount': charge['ChargeAmount']
                        }
                        charges_records.append(charge_record)

            # Create a DataFrame for charges
                charges_df = pd.DataFrame(charges_records)

                return df, charges_df
            else:
                response = response.json()
                print(response)
                quote_records = pd.DataFrame()
                charges_df = pd.DataFrame()
                return quote_records , charges_df            
        else:
            quote_records = pd.DataFrame()
            charges_df = pd.DataFrame()
            return quote_records , charges_df
    except Exception as e:
        send_error_email(str(e),"Midland")
        print(e)


# fromcode = 'E3B3V5'
# tocode = 'M5V3L9'
# noitems = ["2","3"]
# mcweight = ["10","20"]
# length = ["20","30"]
# width = ["15","20"]
# height = ["10","15"]

# data,tax=get_rate_quotes_and_charges_list(fromcode, tocode, noitems, mcweight, length, width, height)
# print(data,tax)

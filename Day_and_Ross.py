import requests
from requests.structures import CaseInsensitiveDict
import json
from suds.client import Client
import xmltodict
from pypostalcode import PostalCodeDatabase
from datetime import datetime

from xml.etree.ElementTree import XML, fromstring
import xml
import pandas as pd
from suds.sax.text import Raw
from uszipcode import SearchEngine, SimpleZipcode
from error_mail import send_error_email


pcdb = PostalCodeDatabase()

def fastest_object_to_dict(obj):
    if not hasattr(obj, '__keylist__'):
        return obj
    data = {}
    fields = obj.__keylist__
    for field in fields:
        val = getattr(obj, field)
        if isinstance(val, list):  # tuple not used
            data[field] = []
            for item in val:
                data[field].append(fastest_object_to_dict(item))
        else:
            data[field] = fastest_object_to_dict(val)
    return data

def day_and_Ross(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc):
    final_from=from_loc.split(",")[0]
    final_province1=from_loc.split(",")[1][1:3]
    final_to=to_loc.split(",")[0]
    final_province2=to_loc.split(",")[1][1:3]
    
    print(final_from,"next provr",final_province1)
    
    try:
        url = "https://dayross.dayrossgroup.com/public/ShipmentServices.asmx?wsdl"
        client = Client(url)
        # body1 =  '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://dayrossgroup.com/web/public/webservices/shipmentServices">\n<ns0:Header />\n<ns0:Body>\n    <ns1:GetRate2>\n    <ns1:division>GeneralFreight</ns1:division>\n    <ns1:emailAddress>api@sourceatlantic.ca</ns1:emailAddress>\n    <ns1:password>PWD071225</ns1:password>\n    <ns1:shipment>\n        <ns1:ShipperAddress>\n            <ns1:City>Edmonton</ns1:City>\n            <ns1:Province>AB</ns1:Province>\n            <ns1:PostalCode>T6E5L7</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ShipperAddress>\n        <ns1:ConsigneeAddress>\n            <ns1:City>DOAKTOWN</ns1:City>\n            <ns1:Province>NB</ns1:Province>\n            <ns1:PostalCode>E9C1H4</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ConsigneeAddress>\n        <ns1:BillToAccount>071225</ns1:BillToAccount>\n        <ns1:Items>\n            <ns1:ShipmentItem>\n                <ns1:Pieces>1</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n                    <ns1:Weight>5</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n        </ns1:Items>\n                </ns1:shipment>\n</ns1:GetRate2>\n</ns0:Body>\n</ns0:Envelope>'
        # body =  '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://dayrossgroup.com/web/public/webservices/shipmentServices">\n<ns0:Header />\n<ns0:Body>\n    <ns1:GetRate2>\n    <ns1:division>'+'Sameday'+'</ns1:division>\n    <ns1:emailAddress>api@sourceatlantic.ca</ns1:emailAddress>\n    <ns1:password>PWD071225</ns1:password>\n    <ns1:shipment>\n        <ns1:ShipperAddress>\n            <ns1:City>SAINT JOHN</ns1:City>\n            <ns1:Province>NB</ns1:Province>\n            <ns1:PostalCode>E2K4L9</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ShipperAddress>\n        <ns1:ConsigneeAddress>\n            <ns1:City>BRAMPTON</ns1:City>\n            <ns1:Province>ON</ns1:Province>\n            <ns1:PostalCode>L6T3X4</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ConsigneeAddress>\n        <ns1:BillToAccount>114283</ns1:BillToAccount>\n        <ns1:Items>\n            <ns1:ShipmentItem>\n                <ns1:Pieces>1</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n           <ns1:Weight>100</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n        </ns1:Items>\n                     </ns1:shipment>\n</ns1:GetRate2>\n</ns0:Body>\n</ns0:Envelope>'
        body =  '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://dayrossgroup.com/web/public/webservices/shipmentServices">\n<ns0:Header />\n<ns0:Body>\n    <ns1:GetRate2>\n    <ns1:division>GeneralFreight</ns1:division>\n    <ns1:emailAddress>api@sourceatlantic.ca</ns1:emailAddress>\n    <ns1:password>PWD071225</ns1:password>\n    <ns1:shipment>\n        <ns1:ShipperAddress>\n            <ns1:City>'+final_from+'</ns1:City>\n            <ns1:Province>'+final_province1+'</ns1:Province>\n            <ns1:PostalCode>'+fromcode+'</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ShipperAddress>\n        <ns1:ConsigneeAddress>\n            <ns1:City>'+final_to+'</ns1:City>\n            <ns1:Province>'+final_province2+'</ns1:Province>\n            <ns1:PostalCode>'+tocode+'</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ConsigneeAddress>\n        <ns1:BillToAccount>071225</ns1:BillToAccount>\n        <ns1:Items>\n            <ns1:ShipmentItem>\n                <ns1:Pieces>'+noitems+'</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n       <ns1:Height>'+height+'</ns1:Height>\n   <ns1:Length>'+length+'</ns1:Length>\n  <ns1:Width>'+width+'</ns1:Width>\n  <ns1:LengthUnit>Inches</ns1:LengthUnit>\n         <ns1:Weight>'+mcweight+'</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n        </ns1:Items>\n          </ns1:shipment>\n</ns1:GetRate2>\n</ns0:Body>\n</ns0:Envelope>'
        body1 =  '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://dayrossgroup.com/web/public/webservices/shipmentServices">\n<ns0:Header />\n<ns0:Body>\n    <ns1:GetRate2>\n    <ns1:division>Sameday</ns1:division>\n    <ns1:emailAddress>api@sourceatlantic.ca</ns1:emailAddress>\n    <ns1:password>PWD071225</ns1:password>\n    <ns1:shipment>\n        <ns1:ShipperAddress>\n            <ns1:City>'+final_from+'</ns1:City>\n            <ns1:Province>'+final_province1+'</ns1:Province>\n            <ns1:PostalCode>'+fromcode+'</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ShipperAddress>\n        <ns1:ConsigneeAddress>\n            <ns1:City>'+final_to+'</ns1:City>\n            <ns1:Province>'+final_province2+'</ns1:Province>\n            <ns1:PostalCode>'+tocode+'</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ConsigneeAddress>\n        <ns1:BillToAccount>114283</ns1:BillToAccount>\n        <ns1:Items>\n            <ns1:ShipmentItem>\n                <ns1:Pieces>'+noitems+'</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n      <ns1:Height>'+height+'</ns1:Height>\n   <ns1:Length>'+length+'</ns1:Length>\n  <ns1:Width>'+width+'</ns1:Width>\n  <ns1:LengthUnit>Inches</ns1:LengthUnit>\n          <ns1:Weight>'+mcweight+'</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n        </ns1:Items>\n          </ns1:shipment>\n</ns1:GetRate2>\n</ns0:Body>\n</ns0:Envelope>'
        print(body)
        xml_str = xml.etree.ElementTree.tostring(fromstring(body), encoding='utf-8')
        xml_str1 = xml.etree.ElementTree.tostring(fromstring(body1), encoding='utf-8')
        print(xml_str)
    
        result = client.service.GetRate2(__inject={'msg':xml_str})
        result1 = client.service.GetRate2(__inject={'msg':xml_str1})
    
        y1 = pd.json_normalize(json.loads((pd.json_normalize(fastest_object_to_dict(result)))['ServiceLevels'].to_json(orient="index",date_format='iso'))['0'])
        y11 = pd.json_normalize(json.loads((pd.json_normalize(fastest_object_to_dict(result1)))['ServiceLevels'].to_json(orient="index",date_format='iso'))['0'])
        y1 = pd.concat([y1, y11], ignore_index=True)
        print("start day and ross",y1)
        y1['Provider'] = 'Day&Ross'
        y1['From'] = pcdb[((fromcode[0:3]).upper())].city
        y1['To'] = pcdb[((tocode[0:3]).upper())].city
        y1['TotalPieces'] = noitems
        y1['TotalWeightPounds'] = mcweight
        y1['ShipmentDate'] = datetime.today().strftime('%Y-%m-%d')
        yl = y1[["Provider","Description","ShipmentDate","From","To","TotalAmount","ExpectedDeliveryDate","TransitTime","TotalPieces","TotalWeightPounds"]]
        yl.rename(columns={'Provider': 'Provider','Description': 'Service Type','TotalAmount':'QuoteTotal', 'ShipCity': 'From','ConsCity':'To','ExpectedDeliveryDate':'Delivery Date (Estimated)','TotalPieces':'No of items','TotalWeightPounds':'weight','ShipmentDate':'ShipDate','TransitTime':'No of days for delivery (Estimated)'}, inplace=True)
        count_row1 = yl.shape[0]
        yn = yl['Service Type'].to_list()
        N = 0
        d = pd.DataFrame(columns=["Provider","Service Type","ChargeLineNo","Description","Amount"])
                
        for X in yn:
            y2 = pd.json_normalize(pd.json_normalize(json.loads(y1['ShipmentCharges.ShipmentCharge'].to_json(orient="index")))[str(N)])
            coun = len(y2.columns)
            print(coun)
            e = pd.DataFrame(columns=["Provider","Service Type","ChargeLineNo","Description","Amount"])
            temp_df = pd.DataFrame(columns=["Description", "Amount"])
    
            for Y in range(coun):
                y5 = pd.json_normalize(y2[Y])
                temp_df = pd.concat([temp_df, y5[['Description', 'Amount']]], ignore_index=True)
                print(temp_df)
    
                        
            temp_df['Service Type'] = X
            temp_df['Provider'] = 'Day&Ross'
            temp_df['ChargeLineNo'] = temp_df.index + 1
    
            print(temp_df)
            d = pd.concat([d, temp_df], ignore_index=True)
            print(d)
    
            N += 1
        
        print(yl)
        print(d)
        return d,yl
    except Exception as e:
        send_error_email(str(e),"Day and Ross")
        print("no data for day and ross",e)


def day_and_Ross_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2,from_loc,to_loc):
    final_from=from_loc.split(",")[0]
    final_province1=from_loc.split(",")[1][1:3]
    final_to=to_loc.split(",")[0]
    final_province2=to_loc.split(",")[1][1:3]
    
    print(final_from,"next provr",final_province1)
    
    try:
        url = "https://dayross.dayrossgroup.com/public/ShipmentServices.asmx?wsdl"
        client = Client(url)
        # body1 =  '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://dayrossgroup.com/web/public/webservices/shipmentServices">\n<ns0:Header />\n<ns0:Body>\n    <ns1:GetRate2>\n    <ns1:division>GeneralFreight</ns1:division>\n    <ns1:emailAddress>api@sourceatlantic.ca</ns1:emailAddress>\n    <ns1:password>PWD071225</ns1:password>\n    <ns1:shipment>\n        <ns1:ShipperAddress>\n            <ns1:City>Edmonton</ns1:City>\n            <ns1:Province>AB</ns1:Province>\n            <ns1:PostalCode>T6E5L7</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ShipperAddress>\n        <ns1:ConsigneeAddress>\n            <ns1:City>DOAKTOWN</ns1:City>\n            <ns1:Province>NB</ns1:Province>\n            <ns1:PostalCode>E9C1H4</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ConsigneeAddress>\n        <ns1:BillToAccount>071225</ns1:BillToAccount>\n        <ns1:Items>\n            <ns1:ShipmentItem>\n                <ns1:Pieces>1</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n                    <ns1:Weight>5</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n        </ns1:Items>\n                </ns1:shipment>\n</ns1:GetRate2>\n</ns0:Body>\n</ns0:Envelope>'
        # body =  '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://dayrossgroup.com/web/public/webservices/shipmentServices">\n<ns0:Header />\n<ns0:Body>\n    <ns1:GetRate2>\n    <ns1:division>'+'Sameday'+'</ns1:division>\n    <ns1:emailAddress>api@sourceatlantic.ca</ns1:emailAddress>\n    <ns1:password>PWD071225</ns1:password>\n    <ns1:shipment>\n        <ns1:ShipperAddress>\n            <ns1:City>SAINT JOHN</ns1:City>\n            <ns1:Province>NB</ns1:Province>\n            <ns1:PostalCode>E2K4L9</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ShipperAddress>\n        <ns1:ConsigneeAddress>\n            <ns1:City>BRAMPTON</ns1:City>\n            <ns1:Province>ON</ns1:Province>\n            <ns1:PostalCode>L6T3X4</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ConsigneeAddress>\n        <ns1:BillToAccount>114283</ns1:BillToAccount>\n        <ns1:Items>\n            <ns1:ShipmentItem>\n                <ns1:Pieces>1</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n           <ns1:Weight>100</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n        </ns1:Items>\n                     </ns1:shipment>\n</ns1:GetRate2>\n</ns0:Body>\n</ns0:Envelope>'
        body =  '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://dayrossgroup.com/web/public/webservices/shipmentServices">\n<ns0:Header />\n<ns0:Body>\n    <ns1:GetRate2>\n    <ns1:division>GeneralFreight</ns1:division>\n    <ns1:emailAddress>api@sourceatlantic.ca</ns1:emailAddress>\n    <ns1:password>PWD071225</ns1:password>\n    <ns1:shipment>\n        <ns1:ShipperAddress>\n            <ns1:City>'+final_from+'</ns1:City>\n            <ns1:Province>'+final_province1+'</ns1:Province>\n            <ns1:PostalCode>'+fromcode+'</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ShipperAddress>\n        <ns1:ConsigneeAddress>\n            <ns1:City>'+final_to+'</ns1:City>\n            <ns1:Province>'+final_province2+'</ns1:Province>\n            <ns1:PostalCode>'+tocode+'</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ConsigneeAddress>\n        <ns1:BillToAccount>071225</ns1:BillToAccount>\n        <ns1:Items>\n            <ns1:ShipmentItem>\n                <ns1:Pieces>'+noitems+'</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n       <ns1:Height>'+height+'</ns1:Height>\n   <ns1:Length>'+length+'</ns1:Length>\n  <ns1:Width>'+width+'</ns1:Width>\n  <ns1:LengthUnit>Inches</ns1:LengthUnit>\n         <ns1:Weight>'+mcweight+'</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n     <ns1:ShipmentItem>\n                <ns1:Pieces>'+noitems2+'</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n       <ns1:Height>'+height2+'</ns1:Height>\n   <ns1:Length>'+length2+'</ns1:Length>\n  <ns1:Width>'+width2+'</ns1:Width>\n  <ns1:LengthUnit>Inches</ns1:LengthUnit>\n         <ns1:Weight>'+mcweight2+'</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n   </ns1:Items>\n          </ns1:shipment>\n</ns1:GetRate2>\n</ns0:Body>\n</ns0:Envelope>'
        body1 =  '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://dayrossgroup.com/web/public/webservices/shipmentServices">\n<ns0:Header />\n<ns0:Body>\n    <ns1:GetRate2>\n    <ns1:division>Sameday</ns1:division>\n    <ns1:emailAddress>api@sourceatlantic.ca</ns1:emailAddress>\n    <ns1:password>PWD071225</ns1:password>\n    <ns1:shipment>\n        <ns1:ShipperAddress>\n            <ns1:City>'+final_from+'</ns1:City>\n            <ns1:Province>'+final_province1+'</ns1:Province>\n            <ns1:PostalCode>'+fromcode+'</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ShipperAddress>\n        <ns1:ConsigneeAddress>\n            <ns1:City>'+final_to+'</ns1:City>\n            <ns1:Province>'+final_province2+'</ns1:Province>\n            <ns1:PostalCode>'+tocode+'</ns1:PostalCode>\n            <ns1:Country>CA</ns1:Country>\n        </ns1:ConsigneeAddress>\n        <ns1:BillToAccount>114283</ns1:BillToAccount>\n        <ns1:Items>\n            <ns1:ShipmentItem>\n                <ns1:Pieces>'+noitems+'</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n      <ns1:Height>'+height+'</ns1:Height>\n   <ns1:Length>'+length+'</ns1:Length>\n  <ns1:Width>'+width+'</ns1:Width>\n  <ns1:LengthUnit>Inches</ns1:LengthUnit>\n          <ns1:Weight>'+mcweight+'</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n    <ns1:ShipmentItem>\n                <ns1:Pieces>'+noitems2+'</ns1:Pieces>\n                <ns1:Description>desc</ns1:Description>\n       <ns1:Height>'+height2+'</ns1:Height>\n   <ns1:Length>'+length2+'</ns1:Length>\n  <ns1:Width>'+width2+'</ns1:Width>\n  <ns1:LengthUnit>Inches</ns1:LengthUnit>\n         <ns1:Weight>'+mcweight2+'</ns1:Weight>\n                <ns1:WeightUnit>Pounds</ns1:WeightUnit>\n           </ns1:ShipmentItem>\n    </ns1:Items>\n          </ns1:shipment>\n</ns1:GetRate2>\n</ns0:Body>\n</ns0:Envelope>'
        print(body)
        xml_str = xml.etree.ElementTree.tostring(fromstring(body), encoding='utf-8')
        xml_str1 = xml.etree.ElementTree.tostring(fromstring(body1), encoding='utf-8')
        print(xml_str)
    
        result = client.service.GetRate2(__inject={'msg':xml_str})
        result1 = client.service.GetRate2(__inject={'msg':xml_str1})
    
        y1 = pd.json_normalize(json.loads((pd.json_normalize(fastest_object_to_dict(result)))['ServiceLevels'].to_json(orient="index",date_format='iso'))['0'])
        y11 = pd.json_normalize(json.loads((pd.json_normalize(fastest_object_to_dict(result1)))['ServiceLevels'].to_json(orient="index",date_format='iso'))['0'])
        y1 = pd.concat([y1, y11], ignore_index=True)
        print("start day and ross",y1)
        y1['Provider'] = 'Day&Ross'
        y1['From'] = pcdb[((fromcode[0:3]).upper())].city
        y1['To'] = pcdb[((tocode[0:3]).upper())].city
        y1['TotalPieces'] = int(noitems)+int(noitems2)
        y1['TotalWeightPounds'] = int(mcweight)+int(mcweight2)
        y1['ShipmentDate'] = datetime.today().strftime('%Y-%m-%d')
        yl = y1[["Provider","Description","ShipmentDate","From","To","TotalAmount","ExpectedDeliveryDate","TransitTime","TotalPieces","TotalWeightPounds"]]
        yl.rename(columns={'Provider': 'Provider','Description': 'Service Type','TotalAmount':'QuoteTotal', 'ShipCity': 'From','ConsCity':'To','ExpectedDeliveryDate':'Delivery Date (Estimated)','TotalPieces':'No of items','TotalWeightPounds':'weight','ShipmentDate':'ShipDate','TransitTime':'No of days for delivery (Estimated)'}, inplace=True)
        count_row1 = yl.shape[0]
        yn = yl['Service Type'].to_list()
        N = 0
        d = pd.DataFrame(columns=["Provider","Service Type","ChargeLineNo","Description","Amount"])
                
        for X in yn:
            y2 = pd.json_normalize(pd.json_normalize(json.loads(y1['ShipmentCharges.ShipmentCharge'].to_json(orient="index")))[str(N)])
            coun = len(y2.columns)
            print(coun)
            e = pd.DataFrame(columns=["Provider","Service Type","ChargeLineNo","Description","Amount"])
            temp_df = pd.DataFrame(columns=["Description", "Amount"])
    
            for Y in range(coun):
                y5 = pd.json_normalize(y2[Y])
                temp_df = pd.concat([temp_df, y5[['Description', 'Amount']]], ignore_index=True)
                print(temp_df)
    
                        
            temp_df['Service Type'] = X
            temp_df['Provider'] = 'Day&Ross'
            temp_df['ChargeLineNo'] = temp_df.index + 1
    
            print(temp_df)
            d = pd.concat([d, temp_df], ignore_index=True)
            print(d)
    
            N += 1
        
        print(yl)
        print(d)
        return d,yl
    except Exception as e:
        send_error_email(str(e),"Day and Ross")
        print("no data for day and ross",e)

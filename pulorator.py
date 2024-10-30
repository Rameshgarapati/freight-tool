from suds.client import Client
import json
import pandas as pd
from suds import WebFault
from datetime import datetime
from error_mail import send_error_email


# def pulorator(fromcode,tocode,noitems,mcweight,length,width,height):

#     pulorator_data=[]
#     pulorator_tax=[]

#     url = "https://webservices.purolator.com/PWS/V2/Estimating/EstimatingService.asmx?wsdl"
#     client = Client(url,username='90403ceda9a84bfaaa85ef9c57a495e8',password='ukT5})SB')
#     Language = client.factory.create('ns0:Language')
#     RequestContext = client.factory.create('ns0:RequestContext')
#     RequestContext.Version = '2.0'
#     RequestContext.GroupID = 'xxx'
#     RequestContext.RequestReference = 'Rating Example'
#     RequestContext.Language = Language.en

#     client.set_options(soapheaders=RequestContext)

#     country="CA"
#     BillingAccountNumber = '4192710'
#     ReceiverAddress = client.factory.create('ns0:ShortAddress')
#     ReceiverAddress.Country = "CA"
#     PackageType = 'CustomerPackaging'
#     TotalWeight = client.factory.create('ns0:TotalWeight')
#     TotalWeight.Value = mcweight
#     WeightUnit = client.factory.create('ns0:WeightUnit')
#     TotalWeight.WeightUnit.value = WeightUnit.lb
   
#     SenderPostalCode = fromcode
    

    

        
#     if country == 'CA':
#         ReceiverAddress.PostalCode = tocode

    
#     response1 = client.service.GetQuickEstimate(BillingAccountNumber,SenderPostalCode,ReceiverAddress,PackageType,TotalWeight)
    
#     for i in response1["ShipmentEstimates"]["ShipmentEstimate"]:
#         print("line")
#         print(i["ServiceID"])
#         temp_rate = {
#                 "Provider": "Purolator",
#                 "Service Type": i["ServiceID"],
#                 'ShipDate': i["ShipmentDate"],
#                 "From": fromcode,
#                 "To": tocode,
#                 "QuoteTotal": i["TotalPrice"],
#                 "Delivery Date (Estimated)": i["ExpectedDeliveryDate"],
#                 "No of days for delivery (Estimated)": i["EstimatedTransitDays"],
#                 "No of items": noitems,
#                 "weight": mcweight
#             }
#         pulorator_data.append(temp_rate)

#         for j in i["Surcharges"][0]:
#             print(j)
#             if j["Amount"] > 0:
#                 temp_tax = {
#                         "Provider": "Purolator",
#                         "Service Type": i["ServiceID"],
#                         "Description": j["Type"],
#                         "Amount": j["Amount"]
#                     }
#                 pulorator_tax.append(temp_tax)
#         for j in i["Taxes"][0]:
#             print(j)
#             if j["Amount"] > 0:
#                 temp_tax = {
#                         "Provider": "Purolator",
#                         "Service Type": i["ServiceID"],
#                         "Description": j["Type"],
#                         "Amount": j["Amount"]
#                     }
#                 pulorator_tax.append(temp_tax)
    
#     return pd.DataFrame(pulorator_data),pd.DataFrame(pulorator_tax)



# def pulorator(fromcode, tocode, noitems, mcweight, length, width, height):
#     import pandas as pd
#     from suds.client import Client
#     from suds import WebFault

#     pulorator_data = []
#     pulorator_tax = []

#     try:
#         url = "https://webservices.purolator.com/PWS/V2/Estimating/EstimatingService.asmx?wsdl"
#         client = Client(url, username='90403ceda9a84bfaaa85ef9c57a495e8', password='ukT5})SB')
#         Language = client.factory.create('ns0:Language')
#         RequestContext = client.factory.create('ns0:RequestContext')
#         RequestContext.Version = '2.0'
#         RequestContext.GroupID = 'xxx'
#         RequestContext.RequestReference = 'Rating Example'
#         RequestContext.Language = Language.en

#         client.set_options(soapheaders=RequestContext)

#         country = "CA"
#         BillingAccountNumber = '4192710'
#         ReceiverAddress = client.factory.create('ns0:ShortAddress')
#         ReceiverAddress.Country = "CA"
#         PackageType = 'CustomerPackaging'
#         TotalWeight = client.factory.create('ns0:TotalWeight')
#         TotalWeight.Value = mcweight
#         WeightUnit = client.factory.create('ns0:WeightUnit')
#         TotalWeight.WeightUnit.value = WeightUnit.lb

#         SenderPostalCode = fromcode

#         if country == 'CA':
#             ReceiverAddress.PostalCode = tocode

#         response1 = client.service.GetQuickEstimate(BillingAccountNumber, SenderPostalCode, ReceiverAddress, PackageType, TotalWeight)

#         for i in response1["ShipmentEstimates"]["ShipmentEstimate"]:
#             temp_rate = {
#                 "Provider": "Purolator",
#                 "Service Type": i["ServiceID"],
#                 'ShipDate': i["ShipmentDate"],
#                 "From": fromcode,
#                 "To": tocode,
#                 "QuoteTotal": i["TotalPrice"],
#                 "Delivery Date (Estimated)": i["ExpectedDeliveryDate"],
#                 "No of days for delivery (Estimated)": i["EstimatedTransitDays"],
#                 "No of items": noitems,
#                 "weight": mcweight
#             }
#             pulorator_data.append(temp_rate)

#             for j in i["Surcharges"][0]:
#                 if j["Amount"] > 0:
#                     temp_tax = {
#                         "Provider": "Purolator",
#                         "Service Type": i["ServiceID"],
#                         "Description": j["Type"],
#                         "Amount": j["Amount"]
#                     }
#                     pulorator_tax.append(temp_tax)
#             for j in i["Taxes"][0]:
#                 if j["Amount"] > 0:
#                     temp_tax = {
#                         "Provider": "Purolator",
#                         "Service Type": i["ServiceID"],
#                         "Description": j["Type"],
#                         "Amount": j["Amount"]
#                     }
#                     pulorator_tax.append(temp_tax)

#         return pd.DataFrame(pulorator_data), pd.DataFrame(pulorator_tax)

#     except WebFault as e:
#         print(f"SOAP error: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     return pd.DataFrame(), pd.DataFrame()



def pulorator(fromcode,tocode,noitems,mcweight,length,width,height,from_loc,to_loc):

    pulorator_data = []
    pulorator_tax = []
    final_from=from_loc.split(",")[0]
    final_province1=from_loc.split(",")[1][1:3]
    final_to=to_loc.split(",")[0]
    final_province2=to_loc.split(",")[1][1:3]
    

    try:
        url = "https://webservices.purolator.com/PWS/V2/Estimating/EstimatingService.asmx?wsdl"
        username = '90403ceda9a84bfaaa85ef9c57a495e8'
        password = 'ukT5})SB'

        # Create a client with username and password
        client = Client(url, username=username, password=password)

        # Create the necessary factory objects
        RequestContext = client.factory.create('ns0:RequestContext')
        RequestContext.Version = '2.0'
        RequestContext.GroupID = 'xxx'
        RequestContext.RequestReference = 'Rating Example'
        RequestContext.Language = 'en'

        # Set the SOAP headers
        client.set_options(soapheaders=RequestContext)

        # Define the Shipment object
        Shipment = client.factory.create('ns0:Shipment')
        Shipment.SenderInformation = client.factory.create('ns0:SenderInformation')
        Shipment.SenderInformation.Address = client.factory.create('ns0:Address')
        Shipment.SenderInformation.Address.Name = 'Arul Kannan'
        Shipment.SenderInformation.Address.StreetNumber = '1234'
        Shipment.SenderInformation.Address.StreetName = 'Main Street'
        Shipment.SenderInformation.Address.City = 'Saint John'
        Shipment.SenderInformation.Address.Province = final_province1
        Shipment.SenderInformation.Address.Country = 'CA'
        Shipment.SenderInformation.Address.PostalCode = fromcode
        Shipment.SenderInformation.Address.PhoneNumber = client.factory.create('ns0:PhoneNumber')
        Shipment.SenderInformation.Address.PhoneNumber.CountryCode = '1'
        Shipment.SenderInformation.Address.PhoneNumber.AreaCode = '905'
        Shipment.SenderInformation.Address.PhoneNumber.Phone = '5555555'

        Shipment.ReceiverInformation = client.factory.create('ns0:ReceiverInformation')
        Shipment.ReceiverInformation.Address = client.factory.create('ns0:Address')
        Shipment.ReceiverInformation.Address.Name = 'Aaron Summer'
        Shipment.ReceiverInformation.Address.StreetNumber = '2245'
        Shipment.ReceiverInformation.Address.StreetName = 'Douglas Road'
        Shipment.ReceiverInformation.Address.City = 'Burnaby'
        Shipment.ReceiverInformation.Address.Province = final_province2
        Shipment.ReceiverInformation.Address.Country = 'CA'
        Shipment.ReceiverInformation.Address.PostalCode = tocode
        Shipment.ReceiverInformation.Address.PhoneNumber = client.factory.create('ns0:PhoneNumber')
        Shipment.ReceiverInformation.Address.PhoneNumber.CountryCode = '1'
        Shipment.ReceiverInformation.Address.PhoneNumber.AreaCode = '604'
        Shipment.ReceiverInformation.Address.PhoneNumber.Phone = '2982181'

        # Function to set dimension
        def set_dimension(value):
            dim = client.factory.create('ns0:Dimension')
            dim.Value = value
            dim.DimensionUnit = 'in'
            return dim

        # Define two different Piece objects with dimensions
        pieces_information = client.factory.create('ns0:ArrayOfPiece')

        # First piece
        piece1 = client.factory.create('ns0:Piece')
        piece1.Weight = client.factory.create('ns0:Weight')
        piece1.Weight.Value = float(mcweight)
        piece1.Weight.WeightUnit = 'lb'
        piece1.Length = set_dimension(int(length))
        piece1.Width = set_dimension(int(width))
        piece1.Height = set_dimension(int(height))
        pieces_information.Piece.append(piece1)

        # # Second piece
        # piece2 = client.factory.create('ns0:Piece')
        # piece2.Weight = client.factory.create('ns0:Weight')
        # piece2.Weight.Value = 15
        # piece2.Weight.WeightUnit = 'lb'
        # piece2.Length = set_dimension(15)
        # piece2.Width = set_dimension(15)
        # piece2.Height = set_dimension(15)
        # pieces_information.Piece.append(piece2)

        # Define the Package Information
        Shipment.PackageInformation = client.factory.create('ns0:PackageInformation')
        Shipment.PackageInformation.ServiceID = 'PurolatorExpress'
        Shipment.PackageInformation.TotalWeight = client.factory.create('ns0:TotalWeight')
        Shipment.PackageInformation.TotalWeight.Value = sum(float(mcweight) for i in range(int(noitems)))
        Shipment.PackageInformation.TotalWeight.WeightUnit = 'lb'
        Shipment.PackageInformation.TotalPieces = int(noitems)
        Shipment.PackageInformation.PiecesInformation = pieces_information

        # Define the Payment Information
        Shipment.PaymentInformation = client.factory.create('ns0:PaymentInformation')
        Shipment.PaymentInformation.PaymentType = 'Sender'
        Shipment.PaymentInformation.BillingAccountNumber = '4192710'
        Shipment.PaymentInformation.RegisteredAccountNumber = '4192710'

        # Define the Pickup Information
        Shipment.PickupInformation = client.factory.create('ns0:PickupInformation')
        Shipment.PickupInformation.PickupType = 'DropOff'

        # Add the current date as the shipment date
        current_date_str = datetime.now().strftime("%Y-%m-%d")
        Shipment.ShipmentDate = current_date_str

        # Define the ShowAlternativeServicesIndicator
        ShowAlternativeServicesIndicator = True

        # Make the request
        response = client.service.GetFullEstimate(Shipment, ShowAlternativeServicesIndicator)

        for i in response["ShipmentEstimates"]["ShipmentEstimate"]:
            temp_rate = {
                "Provider": "Purolator",
                "Service Type": i["ServiceID"],
                'ShipDate': i["ShipmentDate"],
                "From": from_loc,
                "To": to_loc,
                "QuoteTotal": i["TotalPrice"],
                "Delivery Date (Estimated)": i["ExpectedDeliveryDate"],
                "No of days for delivery (Estimated)": i["EstimatedTransitDays"],
                "No of items": noitems,
                "weight": mcweight
            }
            pulorator_data.append(temp_rate)

            for j in i["Surcharges"][0]:
                if j["Amount"] > 0:
                    temp_tax = {
                        "Provider": "Purolator",
                        "Service Type": i["ServiceID"],
                        "Description": j["Type"],
                        "Amount": j["Amount"]
                    }
                    pulorator_tax.append(temp_tax)
            for j in i["Taxes"][0]:
                if j["Amount"] > 0:
                    temp_tax = {
                        "Provider": "Purolator",
                        "Service Type": i["ServiceID"],
                        "Description": j["Type"],
                        "Amount": j["Amount"]
                    }
                    pulorator_tax.append(temp_tax)

        return pd.DataFrame(pulorator_data), pd.DataFrame(pulorator_tax)

    
    except Exception as e:
        send_error_email(str(e),"Purolator")
        print(f"An error occurred: {e}")

    return pd.DataFrame(), pd.DataFrame()



def pulorator_multiple(fromcode,tocode,noitems,mcweight,length,width,height,noitems2,mcweight2,length2,width2,height2,from_loc,to_loc):

    pulorator_data = []
    pulorator_tax = []

    final_from=from_loc.split(",")[0]
    final_province1=from_loc.split(",")[1][1:3]
    final_to=to_loc.split(",")[0]
    final_province2=to_loc.split(",")[1][1:3]

    try:
        url = "https://webservices.purolator.com/PWS/V2/Estimating/EstimatingService.asmx?wsdl"
        username = '90403ceda9a84bfaaa85ef9c57a495e8'
        password = 'ukT5})SB'

        # Create a client with username and password
        client = Client(url, username=username, password=password)

        # Create the necessary factory objects
        RequestContext = client.factory.create('ns0:RequestContext')
        RequestContext.Version = '2.0'
        RequestContext.GroupID = 'xxx'
        RequestContext.RequestReference = 'Rating Example'
        RequestContext.Language = 'en'

        # Set the SOAP headers
        client.set_options(soapheaders=RequestContext)

        # Define the Shipment object
        Shipment = client.factory.create('ns0:Shipment')
        Shipment.SenderInformation = client.factory.create('ns0:SenderInformation')
        Shipment.SenderInformation.Address = client.factory.create('ns0:Address')
        Shipment.SenderInformation.Address.Name = 'Arul Kannan'
        Shipment.SenderInformation.Address.StreetNumber = '1234'
        Shipment.SenderInformation.Address.StreetName = 'Main Street'
        Shipment.SenderInformation.Address.City = 'Saint John'
        Shipment.SenderInformation.Address.Province = final_province1
        Shipment.SenderInformation.Address.Country = 'CA'
        Shipment.SenderInformation.Address.PostalCode = fromcode
        Shipment.SenderInformation.Address.PhoneNumber = client.factory.create('ns0:PhoneNumber')
        Shipment.SenderInformation.Address.PhoneNumber.CountryCode = '1'
        Shipment.SenderInformation.Address.PhoneNumber.AreaCode = '905'
        Shipment.SenderInformation.Address.PhoneNumber.Phone = '5555555'

        Shipment.ReceiverInformation = client.factory.create('ns0:ReceiverInformation')
        Shipment.ReceiverInformation.Address = client.factory.create('ns0:Address')
        Shipment.ReceiverInformation.Address.Name = 'Aaron Summer'
        Shipment.ReceiverInformation.Address.StreetNumber = '2245'
        Shipment.ReceiverInformation.Address.StreetName = 'Douglas Road'
        Shipment.ReceiverInformation.Address.City = 'Burnaby'
        Shipment.ReceiverInformation.Address.Province = final_province2
        Shipment.ReceiverInformation.Address.Country = 'CA'
        Shipment.ReceiverInformation.Address.PostalCode = tocode
        Shipment.ReceiverInformation.Address.PhoneNumber = client.factory.create('ns0:PhoneNumber')
        Shipment.ReceiverInformation.Address.PhoneNumber.CountryCode = '1'
        Shipment.ReceiverInformation.Address.PhoneNumber.AreaCode = '604'
        Shipment.ReceiverInformation.Address.PhoneNumber.Phone = '2982181'

        # Function to set dimension
        def set_dimension(value):
            dim = client.factory.create('ns0:Dimension')
            dim.Value = value
            dim.DimensionUnit = 'in'
            return dim

        # Define two different Piece objects with dimensions
        pieces_information = client.factory.create('ns0:ArrayOfPiece')

        # First piece
        piece1 = client.factory.create('ns0:Piece')
        piece1.Weight = client.factory.create('ns0:Weight')
        piece1.Weight.Value = float(mcweight)
        piece1.Weight.WeightUnit = 'lb'
        piece1.Length = set_dimension(int(length))
        piece1.Width = set_dimension(int(width))
        piece1.Height = set_dimension(int(height))
        pieces_information.Piece.append(piece1)

        
        piece2 = client.factory.create('ns0:Piece')
        piece2.Weight = client.factory.create('ns0:Weight')
        piece2.Weight.Value = float(mcweight2)
        piece2.Weight.WeightUnit = 'lb'
        piece2.Length = set_dimension(int(length2))
        piece2.Width = set_dimension(int(width2))
        piece2.Height = set_dimension(int(height2))
        pieces_information.Piece.append(piece2)

        totalweight=0
        for i in range(int(noitems)):
            totalweight +=float(mcweight)
        for i in range(int(noitems2)):
            totalweight+=float(mcweight2)

        # Define the Package Information
        Shipment.PackageInformation = client.factory.create('ns0:PackageInformation')
        Shipment.PackageInformation.ServiceID = 'PurolatorExpress'
        Shipment.PackageInformation.TotalWeight = client.factory.create('ns0:TotalWeight')
        Shipment.PackageInformation.TotalWeight.Value = sum(float(mcweight) for i in range(int(noitems)))
        Shipment.PackageInformation.TotalWeight.WeightUnit = 'lb'
        Shipment.PackageInformation.TotalPieces = int(noitems)+int(noitems2)
        Shipment.PackageInformation.PiecesInformation = pieces_information

        # Define the Payment Information
        Shipment.PaymentInformation = client.factory.create('ns0:PaymentInformation')
        Shipment.PaymentInformation.PaymentType = 'Sender'
        Shipment.PaymentInformation.BillingAccountNumber = '4192710'
        Shipment.PaymentInformation.RegisteredAccountNumber = '4192710'

        # Define the Pickup Information
        Shipment.PickupInformation = client.factory.create('ns0:PickupInformation')
        Shipment.PickupInformation.PickupType = 'DropOff'

        # Add the current date as the shipment date
        current_date_str = datetime.now().strftime("%Y-%m-%d")
        Shipment.ShipmentDate = current_date_str

        # Define the ShowAlternativeServicesIndicator
        ShowAlternativeServicesIndicator = True

        # Make the request
        response = client.service.GetFullEstimate(Shipment, ShowAlternativeServicesIndicator)

        for i in response["ShipmentEstimates"]["ShipmentEstimate"]:
            temp_rate = {
                "Provider": "Purolator",
                "Service Type": i["ServiceID"],
                'ShipDate': i["ShipmentDate"],
                "From": from_loc,
                "To": to_loc,
                "QuoteTotal": i["TotalPrice"],
                "Delivery Date (Estimated)": i["ExpectedDeliveryDate"],
                "No of days for delivery (Estimated)": i["EstimatedTransitDays"],
                "No of items": int(noitems)+int(noitems2),
                "weight": float(mcweight)+float(mcweight2)
            }
            pulorator_data.append(temp_rate)

            for j in i["Surcharges"][0]:
                if j["Amount"] > 0:
                    temp_tax = {
                        "Provider": "Purolator",
                        "Service Type": i["ServiceID"],
                        "Description": j["Type"],
                        "Amount": j["Amount"]
                    }
                    pulorator_tax.append(temp_tax)
            for j in i["Taxes"][0]:
                if j["Amount"] > 0:
                    temp_tax = {
                        "Provider": "Purolator",
                        "Service Type": i["ServiceID"],
                        "Description": j["Type"],
                        "Amount": j["Amount"]
                    }
                    pulorator_tax.append(temp_tax)

        return pd.DataFrame(pulorator_data), pd.DataFrame(pulorator_tax)

    
    except Exception as e:
        send_error_email(str(e),"Purolator")
        print(f"An error occurred: {e}")

    return pd.DataFrame(), pd.DataFrame() 


# fromcode = 'E2K5P2'
# tocode = 'V5C5A9'
# noitems = "2"
# mcweight = "1.0"
# length = "20"
# width = "15"
# height = "10"


# data,tax=pulorator(fromcode, tocode, noitems, mcweight, length, width, height)
# print(data,tax)


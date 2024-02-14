# import blpapi
import pandas as pd
import time 
import datetime
from itertools import islice
import numpy as np


# def chunks(data, SIZE=10000):
#     it = iter(data)
#     for i in range(0, len(data), SIZE):
#         yield {k:data[k] for k in islice(it, SIZE)}


# def is_market_open():
#     current_time = datetime.datetime.now().time()
#     market_close_time = datetime.time(16, 0)  # 16:00 hours

#     return current_time < market_close_time

# def sendRequest(session, tickers):
#     # Obtain the reference data service
#     refDataService = session.getService("//blp/refdata")

#     # Create a request for bond data
#     request = refDataService.createRequest("ReferenceDataRequest")

#     # Add securities to the request
#     for ticker in tickers:
#         request.getElement("securities").appendValue(f'{ticker}')

#     # Add fields to the request
#     request.getElement("fields").appendValue("BID")
#     request.getElement("fields").appendValue("ASK")
#     request.getElement("fields").appendValue("YLD_YTM_BID")
#     request.getElement("fields").appendValue("YLD_YTM_ASK")
#     request.getElement("fields").appendValue("CPN")
#     request.getElement("fields").appendValue("AMT_OUTSTANDING")
#     request.getElement("fields").appendValue("CPN_FREQ")
#     request.getElement("fields").appendValue("DUR_MID")
#     request.getElement("fields").appendValue("DAYS_TO_NEXT_COUPON")
#     request.getElement("fields").appendValue("FINAL_MATURITY")
    

#     # Send the request
#     session.sendRequest(request)


# def processResponse(event):
#     returndict = {}
#     tickerlist = {
#                 'RIKB 25 0612': 'EH856574@EXCH     Corp', 'RIKB 24 0415': 'BP415428@EXCH     Corp',
#                 'RIKB 26 1015': 'ZM550820@EXCH     Corp', 'RIKB 28 1115': 'AM216492@EXCH     Corp',
#                 'RIKB 31 0124': 'EI543139@EXCH     Corp', 'RIKB 42 0217': 'BU935789@EXCH     Corp',
#                 'RIKS 26 0216': 'AV822915@EXCH     Corp', 'RIKS 30 0701': 'EI719451@EXCH     Corp',
#                 'RIKS 33 0321': 'EJ106481@EXCH     Corp', 'RIKS 37 0115': 'BT641009@EXCH     Corp',
#                 'RVKN 35 1': 'LW833191@EXCH     Corp', 'RVK 32 1': 'BO948965@EXCH     Corp',
#                 'RVK 53 1': 'EJ965736@EXCH     Corp', 'RVKN24 1': 'BR416346@EXCH Corp',
#                 'RVKNG 40 1': 'BO992153@EXCH Corp', 'RVKG 48 1': 'BO720110@EXCH Corp',
#                 'OR090546': 'BO924765@EXCH Corp', 'OR180255 GB': 'ZP725965@EXCH Corp',
#                 'OR020934 GB': 'ZP725685@EXCH Corp', 'OR180242 GB': 'BR384814@EXCH Corp',
#                 'HFF150224': None, 'HFF150434': None,
#                 'HFF150644': None, 'LSS150224': None,
#                 'LSS150434': None, 'LSS151155': None,
#                 'LSS 39 0303': None, 'ARION CBI 25': None,
#                 'ARION CBI 29': None, 'ARION CBI 30': None,
#                 'ARION CBI 48': None, 'LBANK CBI 24': None,
#                 'LBANK CBI 26': None, 'LBANK CBI 28': None,
#                 'ISB CBI 24': None, 'ISB CBI 26': None,
#                 'ISB CBI 28': None, 'ISB CBI 29': None,
#                 'ISB CBI 30': None, 'REGINN181037 GB': None,
#                 'REGINN27 GB': None, 'REGINN50 GB': None,
#                 'ARBO 31 GSB': None, 'FB100366 SB': None,
#                 'GROSKA 29 GB': None, 'IS Kredit 61 SB': None,
#                 'LL 010641 GB': None, 'LSS40440 GB': None

#                     }
#     inv_map = {v: k for k, v in tickerlist.items()}
#     for msg in event:
#         if event.eventType() == blpapi.Event.RESPONSE:
#             securities = msg.getElement("securityData")

#             for i in range(securities.numValues()):
#                 securityData = securities.getValueAsElement(i)
#                 ticker = securityData.getElementAsString("security")
            
#                 for field in securityData.getElement("fieldData").elements():
#                     field_name = field.name()
#                     field_value = field.getValueAsString()
#                     if inv_map[str(ticker)] not in returndict.keys():
#                         returndict[inv_map[str(ticker)]] = {} 
#                     returndict[inv_map[str(ticker)]][str(field_name)] = field_value
    
    # return returndict


def main():
    # Input Bloomberg server details
    # host = "localhost"
    # port = 8194

    # # Establish a connection to the Bloomberg Terminal
    # sessionOptions = blpapi.SessionOptions()
    # sessionOptions.setServerHost(host)
    # sessionOptions.setServerPort(port)

    # session = blpapi.Session(sessionOptions)
    # if not session.start():
    #     print("Failed to start session.")
    #     return

    # try:
    #     if not session.openService("//blp/refdata"):
    #         print("Failed to open //blp/refdata service")
    #         return
    #     uppls = {}
    #     tickerlist = {'RIKB 24 0415': 'BP415428@EXCH     Corp', 'RIKB 25 0612': 'EH856574@EXCH     Corp', 'RIKB 26 1015': 'ZM550820@EXCH     Corp',
    #                    'RIKB 28 1115': 'AM216492@EXCH     Corp', 'RIKB 31 0124': 'EI543139@EXCH     Corp', 'RIKB 42 0217': 'BU935789@EXCH     Corp', 
    #                    'RIKS 26 0216': 'AV822915@EXCH     Corp', 'RIKS 30 0701': 'EI719451@EXCH     Corp', 'RIKS 33 0321': 'EJ106481@EXCH     Corp', 
    #                    'RIKS 37 0115': 'BT641009@EXCH     Corp', 'RVKN 35 1': 'LW833191@EXCH     Corp', 'RVK 32 1': 'BO948965@EXCH     Corp', 
    #                    'RVK 53 1': 'EJ965736@EXCH     Corp', 'RVKN24 1': 'BR416346@EXCH Corp', 'RVKNG 40 1': 'BO992153@EXCH Corp', 
    #                    'RVKG 48 1': 'BO720110@EXCH Corp','OR090546': 'BO924765@EXCH Corp', 'OR180255 GB': 'ZP725965@EXCH Corp', 'OR020934 GB': 'ZP725685@EXCH Corp', 
    #                    'OR180242 GB': 'BR384814@EXCH Corp'}
    #     for item in chunks(tickerlist, 10):
    #         tickerlist = item
    #         sendRequest(session, tickerlist.values())
    #         # Process received events
    #         while True:
    #             event = session.nextEvent()
    #             retdict = processResponse(event)
    #             uppls.update(retdict)
    #             if event.eventType() == blpapi.Event.RESPONSE:
    #                 break
    

    # finally:
    data = [
        ["RIKB 24 0415", 98.625000, 98.710000, 10.121832, 1, 0.174775, 69, "2024-04-15"],
        ["RIKB 25 0612", 98.950000, 99.070000, 8.797499, 1, 1.272446, 127, "2025-06-12"],
        ["RIKB 26 1015", 97.000000, 97.190000, 8.010518, 1, 2.499648, 252, "2026-10-15"],
        ["RIKB 28 1115", 91.350000, 91.585000, 7.197403, 1, 4.294504, 283, "2028-11-15"],
        ["RIKB 31 0124", 98.225000, 98.600000, 6.827343, 1, 5.794940, 353, "2031-01-24"],
        ["RIKB 42 0217", 79.700000, 80.450000, 6.434300, 1, 11.404116, 11, "2042-02-17"],
        ["RIKS 26 0216", 95.950000, 96.185000, 3.606995, 1, 1.968860, 10, "2026-02-16"],
        ["RIKS 30 0701", 102.485000, 102.900000, 2.818276, 1, 5.560478, 146, "2030-07-01"],
        ["RIKS 33 0321", 102.775000, 103.305000, 2.652919, 1, 7.530562, 44, "2033-03-21"],
        ["RIKS 37 0115", 85.200000, 85.770000, 2.338693, 1, 12.024966, 344, "2037-01-15"],
        ["RVKN 35 1", 92.665000, 93.350000, 7.860138, 2, 7.686296, 49, "2035-03-26"],
        ["RVK 32 1", 93.100000, 93.935000, 3.419470, 4, 7.806886, 75, "2032-10-21"],
        ["RVK 53 1", 111.800000, 113.350000, 3.775122, 2, 13.796831, 125, "2053-12-10"],
        ["RVKG 48 1", 87.000000, 88.070000, 3.145621, 2, 18.182083, 75, "2048-10-21"],
        ["OR180255 GB", 92.200000, 92.990000, 2.989111, 1, 20.692547, 12, "2055-02-18"],
        ["OR020934 GB", 89.600000, 90.350000, 2.852709, 1, 9.636367, 129, "2034-09-02"],
        ["OR180242 GB", 82.200000, 83.400000, 6.146622, 2, 6.369581, 12, "2042-02-18"],
        ["RVKN24 1", np.nan, np.nan, 10.271807, 2, 0.270120, 95, "2024-05-11"],
        ["RVKNG 40 1", np.nan, np.nan, 7.228395, 1, 10.892690, 197, "2040-08-21"],
        ["OR090546", np.nan, np.nan, 3.618318, 2, 15.819347, 93, "2046-05-09"]
    ]

    columns = ["Nafn", "BID", "ASK", "YLD_YTM_BID", "CPN_FREQ", "DUR_MID", "DAYS_TO_NEXT_COUPON", "FINAL_MATURITY"]


# Create the DataFrame
    tafla = pd.DataFrame(data, columns=columns)
    #     tafla = pd.DataFrame.from_dict(uppls, orient='index')
    #     tafla.reset_index(inplace=True)
    #     tafla.rename(columns={'index':"Nafn"}, inplace=True)

    # return [tafla, uppls]
    return [tafla, data]


if __name__ == "__main__":
    # while is_market_open:
    main()

# search_transactions_limit.py
import json
# requires Python SDK version 1.3 or higher
from algosdk.v2client import indexer
from datetime import datetime, timedelta
import base64
import pytz

# USER CONFIGURABLE SETTINGS
#  Set your local time zone. 
local = pytz.timezone("America/New_York")

myindexer = indexer.IndexerClient(indexer_token="", indexer_address="https://algoindexer.algoexplorerapi.io", headers={'User-Agent': 'DoYouLoveMe?'})

# Set start and end time of the vote in your local time
check_time = datetime.now() - timedelta(days=1)
utc_dt = check_time.astimezone(pytz.utc)
check_time_start_utc = utc_dt.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

# Get transactions to the designated wallet between the start and end dates
response = myindexer.search_transactions_by_address(
    address="C3DUWF4E4WHD4NQ52S3QEWB6EOFAEVZ55UBYFJNBJSI2LYFTUSO3IABT34", 
    asset_id=435335235, 
    start_time=check_time_start_utc,  
    min_amount=100000,
    limit=15
    #max_amount=0
)

totaltransactions = len(response['transactions'])

message = 'Buy/sells in the last 24 hours > 200K CRSD(showing last 15)'
for x in range(totaltransactions):
    try: 
        if response['transactions'][x]['asset-transfer-transaction']['receiver'] == 'C3DUWF4E4WHD4NQ52S3QEWB6EOFAEVZ55UBYFJNBJSI2LYFTUSO3IABT34':
            amount_sold = (response['transactions'][x]['asset-transfer-transaction']['amount'])
            amount_sold_format = "{:,}".format(amount_sold)
            crsd_seller_address = response['transactions'][x]['sender']
            tx_sold_time = response['transactions'][x]['round-time']
            tx_sold_time_local = datetime_time = datetime.fromtimestamp(tx_sold_time)

            response_output = str(crsd_seller_address[0:10]) + '; ' + str(tx_sold_time_local) + '; sold; ' +  str(amount_sold_format) + ' CRSD' + '\n'
            message = message + '\n' + str(crsd_seller_address) + ' sold ' + str(amount_sold_format) + ' CRSD on ' + str(tx_sold_time_local) + ' EST'
    except KeyError:
        pass

    try: 
        if response['transactions'][x]['sender'] == 'C3DUWF4E4WHD4NQ52S3QEWB6EOFAEVZ55UBYFJNBJSI2LYFTUSO3IABT34':
            amount_bought = (response['transactions'][x]['asset-transfer-transaction']['amount'])
            amount_bought_format = "{:,}".format(amount_bought)
            crsd_buyer_address = response['transactions'][x]['asset-transfer-transaction']['receiver']
            tx_bought_time = response['transactions'][x]['round-time']
            tx_bought_time_local = datetime_time = datetime.fromtimestamp(tx_bought_time)

            response_output = str(crsd_buyer_address[0:10]) + '; ' + str(tx_bought_time_local) + '; bought; ' + str(amount_bought_format) + ' CRSD' +'\n'
            message = message + '\n' + str(crsd_buyer_address) + ' bought ' + str(amount_bought_format) + ' CRSD on ' + str(tx_bought_time_local) + ' EST'
            
    except KeyError:
        pass
print(message)


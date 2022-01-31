from algosdk.v2client import indexer
from datetime import datetime   
import base64
import pytz

# USER CONFIGURABLE SETTINGS
#  Set your local time zone. 
local = pytz.timezone("America/New_York")

# Set start and end time of the vote in your local time
vote_start_date = "2022-1-25 14:47"
vote_end_date = "2022-2-01 14:47"

static_file_locatin = 'CHANGEME'

f = open(static_file_locatin + "crescendo_vote.txt", "w")

# DO NOT MAKE ANY CHANGES BELOW #
#######################################

# instantiate indexer client
myindexer = indexer.IndexerClient(indexer_token="", indexer_address="https://algoindexer.algoexplorerapi.io", headers={'User-Agent': 'DoYouLoveMe?'})

#Convert start date/time to UTC
naive = datetime.strptime(vote_start_date, "%Y-%m-%d %H:%M")
local_dt = local.localize(naive, is_dst=None)
utc_dt = local_dt.astimezone(pytz.utc)
vote_start_date_utc = utc_dt.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

#Convert end date/time to UTC
naive = datetime.strptime(vote_end_date, "%Y-%m-%d %H:%M")
local_dt = local.localize(naive, is_dst=None)
utc_dt = local_dt.astimezone(pytz.utc)
vote_end_data_utc = utc_dt.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

# Get transactions to the designated wallet between the start and end dates
response = myindexer.search_transactions_by_address(
    address="34IOOGFLLWPB43R3LSHTZE5AG33TFEKHCM4UELGGXUCZQ6DR7ETGMG7TCA", 
    #asset_id=435335235, 
    start_time=vote_start_date_utc,  
    end_time=vote_end_data_utc,
    #min_amount=0,
    #max_amount=0
)

totaltransactions = len(response['transactions'])

# A list containing multiple characters, that needs to be deleted from the string.
list_of_chars = ['\n', '[', ']', '(', ')', ';', '\\', '/',',']
translation_table = str.maketrans('', '', ''.join(list_of_chars))

today = datetime.now()

f.write(str("Wallet Address,Block Voted,CRSD Balance,Vote,Last Updated:" + str(today) + " Eastern US Time" + '\n'))
for x in range(totaltransactions):
    try: 
        if response['transactions'][x]['asset-transfer-transaction']['receiver'] == '34IOOGFLLWPB43R3LSHTZE5AG33TFEKHCM4UELGGXUCZQ6DR7ETGMG7TCA':
            #decode note field and strip new line
            note_string = response['transactions'][x]['note']
            note_string_bytes = note_string.encode("ascii")
            note_decode_bytes = base64.b64decode(note_string_bytes)
            note_decode_string = note_decode_bytes.decode("ascii")
            note_stripped = note_decode_string.translate(translation_table)

            #Check CRSD balance
            account_balance = myindexer.account_info(address=response['transactions'][x]['sender'])
            totalasa = len(account_balance['account']['assets'])
            for y in range(totalasa):
                if account_balance['account']['assets'][y]['asset-id'] == 435335235:
                    crescendo_balance = account_balance['account']['assets'][y]['amount']

            response_output = response['transactions'][x]['sender'] + ',' +  str(response['transactions'][x]['confirmed-round']) + ',' + str(crescendo_balance) + ',' + note_stripped + '\n'
            f.write(str(response_output))
    except KeyError:
        pass
    
     #Check if they voted by sending Algo instead of CRSD
    try: 
        if response['transactions'][x]['payment-transaction']['receiver'] == '34IOOGFLLWPB43R3LSHTZE5AG33TFEKHCM4UELGGXUCZQ6DR7ETGMG7TCA' :
            #decode note field and strip new line
            note_string_alg = response['transactions'][x]['note']
            note_string_bytes_alg = note_string_alg.encode("ascii")
            note_decode_bytes_alg = base64.b64decode(note_string_bytes_alg)
            note_decode_string_alg = note_decode_bytes_alg.decode("ascii")
            note_stripped_alg = note_decode_string_alg.translate(translation_table)

            #Check CRSD balance
            account_balance_alg = myindexer.account_info(address=response['transactions'][x]['sender'])
            totalasa_alg = len(account_balance_alg['account']['assets'])
            for y in range(totalasa_alg):
                if account_balance_alg['account']['assets'][y]['asset-id'] == 435335235:
                    crescendo_balance_alg = account_balance_alg['account']['assets'][y]['amount']

            f.write(response['transactions'][x]['sender'] + ',' +  str(response['transactions'][x]['confirmed-round']) + ',' + str(crescendo_balance_alg) + ',' + note_stripped_alg + '\n')
    except KeyError:
        pass


f.close()
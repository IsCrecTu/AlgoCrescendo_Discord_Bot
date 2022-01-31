from algosdk.v2client import indexer
import sqlite3

myindexer = indexer.IndexerClient(indexer_token="", indexer_address="https://algoindexer.algoexplorerapi.io", headers={'User-Agent': 'DoYouLoveMe?'})

static_file_locatin = 'CHANGEME'

con = sqlite3.connect(static_file_locatin + 'crsd_holders.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS holders")
cur.execute("DROP TABLE IF EXISTS lp_holders")
cur.execute("CREATE TABLE holders (wallet text NOT NULL, crsd_balance integer NOT NULL)")
cur.execute("CREATE TABLE lp_holders (wallet text NOT NULL, crsd_lp_balance integer NOT NULL)")

nexttoken = ""
numtx = 1
# loop using next_page to paginate until there are no more transactions in the response
# for the limit (max is 1000  per request)
while (numtx > 0):
    response = myindexer.asset_balances(asset_id=435335235,  next_page=nexttoken) 
    transactions = response['balances']
    numtx = len(transactions)
    if (numtx > 0):
        nexttoken = response['next-token']
       
        for x in range(numtx):
            try:
                wallet_address = response['balances'][x]['address']
                wallet_balance = response['balances'][x]['amount']
            except KeyError:
                pass
            cur.execute("INSERT INTO holders VALUES (?, ?)", (wallet_address, wallet_balance))

#Check LP Token Balance
nexttoken = ""
numtx = 1
# loop using next_page to paginate until there are no more transactions in the response
# for the limit (max is 1000  per request)
while (numtx > 0):
    response = myindexer.asset_balances(asset_id=552660994, max_balance=1000000000, next_page=nexttoken) 
    transactions = response['balances']
    numtx = len(transactions)
    if (numtx > 0):
        nexttoken = response['next-token']
       
        for x in range(numtx):
            try:
                wallet_lp_address = response['balances'][x]['address']
                wallet_lp_balance = (response['balances'][x]['amount'])/1000000
            except KeyError:
                pass
            cur.execute("INSERT INTO lp_holders VALUES (?, ?)", (wallet_lp_address, wallet_lp_balance))

con.commit()

con.close()
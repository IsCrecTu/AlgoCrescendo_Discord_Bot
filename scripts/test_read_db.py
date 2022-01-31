import sqlite3

def readSqliteTable():
    static_file_locatin = 'CHANGEME'
    top10="Top 10 Wallets under 20 Mill CRSD"
    try:
        sqliteConnection = sqlite3.connect(static_file_location + 'crsd_holders.db')
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")

        sqlite_select_query = """SELECT * FROM holders WHERE crsd_balance < 20000000 ORDER BY crsd_balance DESC LIMIT 10"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        #print("Total rows are:  ", len(records))
        #print("Printing each row")
        i = 1
        for row in records:
            wallet_txt_address = row[0]
            wallet_txt_balance = "{:,}".format(row[1])
            top10 = top10 + '\n' + str(i) + ". " + wallet_txt_address[0:10] + "--------Balance: " + str(wallet_txt_balance) + " CRSD"
            #print(str(i) + ". " + wallet_txt_address[0:10] + " Balance: " + str(wallet_txt_balance) + " CRSD" )
            i = i + 1

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection is closed")

    return top10

print(readSqliteTable())
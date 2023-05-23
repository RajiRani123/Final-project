import mysql.connector
from mysql.connector import Error


class Database():
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="banks_portal",
                 user='root',
                 password='1337'):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)

            if self.connection.is_connected():
                return
        except Error as e:
            print("Error while connecting to MySQL", e)

    def getAllAccounts(self):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "select * from accounts"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def getAllTransactions(self):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "select * from transactions"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def deposit(self, accountID, amount):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            result = self.cursor.callproc('deposit', args=[accountID, amount])
            self.connection.commit()
            print(result)

    def withdraw(self, accountID, amount):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            result = self.cursor.callproc('withdraw', args=[accountID, amount])
            self.connection.commit()
            print(result)

    def addAccount(self, ownerName, owner_ssn, balance, status):
        add_account = "INSERT INTO accounts(ownerName, owner_ssn, balance, account_status) VALUES (%s, %s, %s, %s)"
        account_data = (ownerName, owner_ssn, balance, status)
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            self.cursor.execute(add_account, account_data)
            self.connection.commit()
            print(self.cursor.rowcount, "record inserted.")

    def accountTransactions(self, accountID):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            self.cursor.callproc('accountTransactions', args=[accountID])
            results = []
            for result in self.cursor.stored_results():
                rows = result.fetchall()
                if rows:
                    results.extend(rows)
            return results

    def deleteAccount(self, AccountID):
        del_account = "DELETE FROM accounts WHERE accountId = %s"
        del_transactions = "DELETE FROM transactions WHERE accountId = %s"
        account_data = (AccountID,)
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            self.cursor.execute(del_account, account_data)
            self.cursor.execute(del_transactions, account_data)
            self.connection.commit()


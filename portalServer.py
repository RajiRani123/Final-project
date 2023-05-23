from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
from portalDatabase import Database
import cgi


class PortalRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args):
        self.database = Database()
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):

        try:
            if self.path == '/addAccount':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                owner_name = form.getvalue("oname")
                owner_ssn = int(form.getvalue("owner_ssn"))
                balance = float(form.getvalue("balance"))
                acct_status = "active"

                self.database.addAccount(owner_name, owner_ssn, balance, acct_status)

                print("grabbed values", owner_name, owner_ssn, balance)

                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Account have been added</h3>")
                self.wfile.write(b"<div><a href='/addAccount'>Add a New Account</a></div>")
                self.wfile.write(b"</center></body></html>")

            if self.path == '/deposit':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                account_id = int(form.getvalue("acc_id"))
                amount = float(form.getvalue("amount"))

                self.database.deposit(account_id, amount)

                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Deposit has been processed</h3>")
                self.wfile.write(b"<div><a href='/deposit'>Make Another Deposit</a></div>")
                self.wfile.write(b"</center></body></html>")

            if self.path == '/withdraw':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                account_id = int(form.getvalue("acc_id"))
                amount = float(form.getvalue("amount"))

                self.database.withdraw(account_id, amount)

                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Withdrawal has been processed</h3>")
                self.wfile.write(b"<div><a href='/withdraw'>Make Another Withdrawal</a></div>")
                self.wfile.write(b"</center></body></html>")

            if self.path == '/searchTransactions':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                account_id = int(form.getvalue("acc_id"))

                transactions = self.database.accountTransactions(account_id)
                print(transactions)

                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Transactions for Account " + str(account_id).encode() + b"</h3>")
                self.wfile.write(b"<table border=2>")
                self.wfile.write(
                    b"<tr><th>Transaction ID</th><th>Account ID</th><th>Type</th><th>Amount</th></tr>")
                for t in transactions:
                    self.wfile.write(
                        "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                            t[0], t[1], t[2], t[3]
                        ).encode()
                    )
                self.wfile.write(b"</table>")
                self.wfile.write(b"<div><a href='/searchTransactions'>Search for Another Account</a></div>")
                self.wfile.write(b"</center></body></html>")

            if self.path == '/deleteAccount':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                account_id = int(form.getvalue("acc_id"))

                self.database.deleteAccount(account_id)

                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Deletion has been processed</h3>")
                self.wfile.write(b"<div><a href='/deleteAccount'>Make Another Deletion</a></div>")
                self.wfile.write(b"</center></body></html>")

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

        return

    def do_GET(self):
        try:

            if self.path == '/':
                data = []
                records = self.database.getAllAccounts()
                print(records)
                data = records

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>All Accounts</h2>")
                self.wfile.write(b"<table border=2> \
                                    <tr><th> Account ID </th>\
                                        <th> Account Owner</th>\
                                        <th> Balance </th>\
                                        <th> Status </th></tr>")
                for row in data:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b'</td></tr>')

                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/transactions':
                transactions = self.database.getAllTransactions()
                print(transactions)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                <a href='/transactions'>All Transactions</a>|\
                                 <a href='/addAccount'>Add Account</a>|\
                                  <a href='/withdraw'>Withdraw</a>|\
                                  <a href='/deposit'>Deposit </a>|\
                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>All Transactions</h2>")
                self.wfile.write(b"<table border=2> \
                    <tr><th>Transaction ID</th><th>Account ID</th><th>Type</th><th>Amount</th></tr>")
                for t in transactions:
                    self.wfile.write(
                        "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                            t[0], t[1], t[2], t[3]
                        ).encode()
                    )
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/addAccount':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Add New Account</h2>")

                self.wfile.write(b"<form action='/addAccount' method='post'>")
                self.wfile.write(b'<label for="oname">Owner Name:</label>\
                      <input type="text" id="oname" name="oname"><br><br>\
                      <label for="owner_ssn">Owner SSN:</label>\
                      <input type="number" id="owner_ssn" name="owner_ssn"><br><br>\
                      <label for="balance">Balance:</label>\
                      <input type="number" step="0.01" id="balance" name="balance"><br><br>\
                      <input type="submit" value="Submit">\
                      </form>')

                self.wfile.write(b"</center></body></html>")
                return
            if self.path == '/withdraw':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Withdraw from an account</h2>")

                self.wfile.write(b"<form action='/withdraw' method='post'>")
                self.wfile.write(b'<label for="acc_id">Account ID:</label>\
                                                      <input type="number" id="acc_id" name="acc_id"><br><br>\
                                                      <label for="amount">Amount:</label>\
                                                      <input type="text" id="amount" name="amount"><br><br>\
                                                      <input type="submit" value="Submit">\
                                                      </form>')

                self.wfile.write(b"</center></body></html>")
                return

            if self.path == '/deposit':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Deposit into an account</h2>")

                self.wfile.write(b"<form action='/deposit' method='post'>")
                self.wfile.write(b'<label for="acc_id">Account ID:</label>\
                                      <input type="number" id="acc_id" name="acc_id"><br><br>\
                                      <label for="amount">Amount:</label>\
                                      <input type="text" id="amount" name="amount"><br><br>\
                                      <input type="submit" value="Submit">\
                                      </form>')

                self.wfile.write(b"</center></body></html>")
                return
            if self.path == '/searchTransactions':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Search for a transaction</h2>")

                self.wfile.write(b"<form action='/searchTransactions' method='post'>")
                self.wfile.write(b'<label for="acc_id">Account ID:</label>\
                                                                      <input type="number" id="acc_id" name="acc_id"><br><br>\
                                                                      <input type="submit" value="Submit">\
                                                                      </form>')

                self.wfile.write(b"</center></body></html>")
                return

            if self.path == '/deleteAccount':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                                <a href='/transactions'>All Transactions</a>|\
                                                 <a href='/addAccount'>Add Account</a>|\
                                                  <a href='/withdraw'>Withdraw</a>|\
                                                  <a href='/deposit'>Deposit </a>|\
                                                  <a href='/searchTransactions'>Search Transactions</a>|\
                                                  <a href='/deleteAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Delete account</h2>")

                self.wfile.write(b"<form action='/deleteAccount' method='post'>")
                self.wfile.write(b'<label for="acc_id">Account ID:</label>\
                                                                      <input type="number" id="acc_id" name="acc_id"><br><br>\
                                                                      <input type="submit" value="Submit">\
                                                                      </form>')

                self.wfile.write(b"</center></body></html>")
                return



        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


def run(server_class=HTTPServer, handler_class=PortalRequestHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()


run()
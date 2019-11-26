import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    #
    delta = 0
    rows = db.execute(
        "SELECT symbol, company, SUM(shares), user_id FROM transactions WHERE user_id = :id GROUP BY symbol", id=session["user_id"])
    for row in rows:
        if row['SUM(shares)'] >= 1:
            value = lookup(row['symbol'])['price']
            row['price'] = value
            totalvalue = (row['SUM(shares)'] * row['price'])
            delta += totalvalue
            row['price'] = "%.2f" % round(value, 2)
            row['total'] = "%.2f" % round(totalvalue, 2)

    ross = db.execute("SELECT cash FROM users where id= :id", id=session["user_id"])
    totalcash1 = ross[0]['cash']
    totalcash = "%.2f" % round(totalcash1, 2)
    delta += totalcash1
    officialdelta = "%.2f" % round(delta, 2)
    rows = filter(lambda x: x['SUM(shares)'] != 0, rows)
    return render_template("index.html", rows=rows, totalcash=totalcash, officialdelta=officialdelta)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # to buy check that the item exists as a share name then buy the amount that you want
    # subtract cash and then add shares
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        ticker1 = request.form.get("symbol")

        if not request.form.get("symbol"):
            return apology("Missing Symbol!", 400)

        if not request.form.get("shares"):
            return apology("Missing Shares!", 400)

        share_number1 = request.form.get("shares")

        share_number = int(share_number1)
        if share_number < 1:
            return apology("Share Amount must be a Positive Integer")

        quotes = lookup(ticker1)

        if lookup(ticker1) == None:
            return apology("Invalid Symbol")

        cost1 = float(quotes["price"])

        cash1 = db.execute("SELECT cash FROM users WHERE id = :id",
                           id=session["user_id"])

        cash = cash1[0]["cash"]

        transaction_cost = cost1 * share_number
        user_id1 = db.execute("SELECT id FROM users WHERE id = :id",
                              id=session["user_id"])
        user_id = user_id1[0]["id"]

        company = quotes["name"]

        updated_cash = cash - transaction_cost

        ticker = ticker1.upper()

        if transaction_cost < cash:
            db.execute("INSERT INTO transactions (user_id, symbol, company, shares, cost) VALUES (:userid, :symbol, :company, :shares, :cost)",
                       userid=user_id, symbol=ticker, company=company, shares=share_number, cost=transaction_cost)
            db.execute("UPDATE users SET cash = :updatedcash WHERE id=:id", id=session["user_id"], updatedcash=updated_cash)
            return redirect("/")

        if cost1 * share_number > cash:
            return apology("Can't Afford", 400)


@app.route("/history")
@login_required
def history():
    # all we have to do is select things from the transaction table
    # also round value to make sure it is in dollars
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, shares, cost, transacted FROM transactions where user_id = :id", id=session["user_id"])
    for row in rows:
        value = row['cost']
        row['cost'] = "%.2f" % round(value, 2)

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change", methods=["GET", "POST"])
def change():
    """Change Password"""
# to change password just input username and old password
# then get a new hash that is input that works
    if request.method == "GET":
        return render_template("change.html")

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        new_password = request.form.get("new_password")

        if not request.form.get("username"):
            return apology("Make sure to input your Username!")

        if not request.form.get("password"):
            return apology("Insert your Password")

        if not request.form.get("new_password"):
            return apology("Insert a New Password")

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        if len(rows) == 1 and check_password_hash(rows[0]["hash"], request.form.get("password")):
            db.execute("UPDATE users SET hash = :hash WHERE username = :username",
                       hash=generate_password_hash(new_password), username=username)

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        ticker = request.form.get("symbol")

    quotes = lookup(ticker)

    if lookup(ticker) == None:
        return apology("Invalid Symbol")

    company_name1 = quotes["name"]
    cost1 = float(quotes["price"])
    ticker1 = quotes["symbol"]

    return render_template("quoted.html", company_name1=company_name1, ticker1=ticker1, cost1=cost1)


@app.route("/register", methods=["GET", "POST"])
def register():
    """register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("Make sure to input a Username!", 400)

        if not request.form.get("password"):
            return apology("Insert a Password", 400)

        if not request.form.get("confirmation"):
            return apology("Confirm Password", 400)

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if len(rows) == 1:
            return apology("Username already Exists", 400)

        if password != confirmation:
            return apology("Passwords do not match", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=username, hash=generate_password_hash(password))

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
# if get then make sure to go to page

    if request.method == "GET":
        rows = db.execute("SELECT symbol FROM transactions WHERE user_id = :userid GROUP BY symbol", userid=session["user_id"])
        return render_template("sell.html", rows=rows)

    if request.method == "POST":
        # if sell then check that you have enough of stock and then add to money the
        # transaction fee and subtract share

        ticker1 = request.form.get("symbol")

        if not request.form.get("symbol"):
            return apology("Must input a Symbol!")

        if not request.form.get("shares"):
            return apology("Missing Shares!")

        share_number2 = request.form.get("shares")

        share_number1 = int(share_number2)
        if share_number1 < 1:
            return apology("Share Amount must be a Positive Integer")

        quotes = lookup(ticker1)

        price = float(quotes["price"])

        cash1 = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        cash = cash1[0]["cash"]

        personal_stocks1 = db.execute(
            "SELECT shares, symbol FROM transactions WHERE user_id = :id AND symbol = :symbol GROUP BY symbol", id=session["user_id"], symbol=ticker1)

        personal_shares1 = personal_stocks1[0]["shares"]

        personal_shares = int(personal_shares1)

        transaction_add = price * share_number1
        user_id1 = db.execute("SELECT id FROM users WHERE id = :id", id=session["user_id"])
        user_id = user_id1[0]["id"]

        share_number = -1 * share_number1

        company = quotes["name"]

        updated_cash = cash + transaction_add

        if personal_shares >= share_number1:
            db.execute("INSERT INTO transactions (user_id, symbol, company, shares, cost) VALUES (:userid, :symbol, :company, :shares, :cost)",
                       userid=user_id, symbol=ticker1, company=company, shares=share_number, cost=transaction_add)
            db.execute("UPDATE users SET cash = :updatedcash WHERE id=:id", id=session["user_id"], updatedcash=updated_cash)
            return redirect("/")

        if share_number1 > personal_shares:
            return apology("Must own the stocks that you want to Sell!")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

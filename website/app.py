import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # check user money
    user_money_array = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    user_money = user_money_array[0]['cash']
    # check user stocks
    index_db = db.execute(
        "SELECT symbol, SUM(number) AS numbers, price FROM purchases WHERE usernameID = ? GROUP BY symbol", session["user_id"])
    # total holdings
    stockvaluesum = db.execute(
        "SELECT SUM(number) AS numbers, price FROM purchases WHERE usernameID = ? GROUP BY symbol", session["user_id"])
    tot = 0
    for i in stockvaluesum:
        tot += int(i['numbers'])*int(i['price'])
    return render_template("index.html", user_money=user_money, index_db=index_db, tot=tot)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # symbol
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        symbol = request.form.get("symbol")

        # existence
        quoted_stock = lookup(request.form.get("symbol"))
        if quoted_stock == None:
            return apology("stock does not exist", 400)

        # number of stocks
        if not request.form.get("shares"):
            return apology("must provide number", 400)
        try:
            share_number = int(request.form.get("shares"))
        except:
            return apology("number must be a positive integer", 400)

        if share_number < 0:
            return apology("number must be a positive integer", 400)
        if (share_number % 1) != 0:
            return apology("number must be an integer", 400)
        # errors passed

        # price
        purchase_price = share_number*quoted_stock['price']
        # check user money
        user_money_array = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_money = user_money_array[0]['cash']
        # errors
        if purchase_price > user_money:
            return apology("insufficient funds")
        # take money
        new_money = user_money - purchase_price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_money, session["user_id"])

        # give stonks
        db.execute("INSERT INTO purchases (usernameID, symbol, number, price) VALUES (?, ?, ?, ?)",
            session["user_id"], symbol, share_number, quoted_stock['price'])

        return redirect("/")

    else:

        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # check user money
    user_money_array = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    user_money = user_money_array[0]['cash']
    # check user stocks
    index_db = db.execute("SELECT symbol, number, price, time FROM purchases WHERE usernameID = ?", session["user_id"])

    return render_template("history.html", user_money=user_money, index_db=index_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def search():
    """Search for hashtag."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide hashtag", 400)

        searched_hashtag = lookup(request.form.get("symbol"))
        if searched_hashtag == None:
            return apology("hashtag does not exist", 400)

        return render_template("quoted.html", name=searched_hashtag['name'], price=quoted_stock['price'], symbol=quoted_stock['symbol'])

    else:
        return render_template("search.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username was submitted
        intended_username = request.form.get("username")
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Throw error if username already exists.
        usernames = db.execute("SELECT username FROM users WHERE username = ?", intended_username)
        if len(usernames) > 0:
            return apology("username already exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation must match", 400)

        # hash password and insert it and username into db
        hash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", intended_username, hash)

        return redirect("/")

    else:

        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # symbol
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        symbol = request.form.get("symbol")

        # existence
        quoted_stock = lookup(request.form.get("symbol"))
        if quoted_stock == None:
            return apology("stock does not exist", 400)

        # number of stocks
        if not request.form.get("shares"):
            return apology("must provide number", 400)
        share_number = int(request.form.get("shares"))

        if share_number < 0:
            return apology("number must be a positive integer", 400)
        # errors passed

        # price
        sale_price = share_number*quoted_stock['price']
        # check user money
        user_money_array = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_money = user_money_array[0]['cash']

        # share check
        user_share_count_temp = db.execute(
            "SELECT SUM(number) AS numbers FROM purchases WHERE usernameID = ? AND symbol = ?", session["user_id"], symbol)
        print(user_share_count_temp)
        user_share_count = int(user_share_count_temp[0]["numbers"])
        if share_number > user_share_count:
            return apology("insufficient shares")

        # give money
        new_money = user_money + sale_price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_money, session["user_id"])

        # take stonks
        db.execute("INSERT INTO purchases (usernameID, symbol, number, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, (-1 * share_number), quoted_stock['price'])

        return redirect("/")

    else:
        # choosing stocks that are owned in a quantity greater than 0
        available_stocks = db.execute(
            "SELECT symbol FROM purchases WHERE usernameID = ? GROUP BY symbol HAVING SUM(number) > 0", session["user_id"])
        return render_template("sell.html", symbol=[stock["symbol"] for stock in available_stocks])


@app.route("/addmoney", methods=["GET", "POST"])
@login_required
def addmoney():
    """add money."""
    if request.method == "POST":

        if not request.form.get("addmoney"):
            return apology("must provide number", 400)

        added = int(request.form.get("addmoney"))

        if added < 0:
            return apology("must provide positive integer", 400)

        # check user money
        user_money_array = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_money = user_money_array[0]['cash']

        new_money = added + user_money

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_money, session["user_id"])

        return redirect("/")

    else:
        return render_template("addmoney.html")
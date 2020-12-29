import os

from datetime import datetime
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

    rows = db.execute("SELECT * FROM users WHERE id=:id", id=session.get('user_id'))
    cash = rows[0]['cash']
    stocks = db.execute("SELECT * FROM shares WHERE id=:id", id=session.get('user_id'))
    mapped_stock = []
    total = cash
    for stock in stocks:
        temp = {}
        temp['name'] = stock['name']
        temp['symbol'] = stock['symbol']
        temp['price' ] = lookup(stock['symbol'])['price']
        temp['shares'] = stock['shares']
        mapped_stock.append(temp)
        total += stock['price']  * stock['shares']
    if session.get('message'):
        def get_flashed_messages():
            return session.get('message')
    else:
        def get_flashed_messages():
            return None
    return render_template('index.html', stocks=mapped_stock, usd=usd, cash=cash, total=total, get_flashed_messages=get_flashed_messages)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'POST':

        if not request.form.get('symbol'):
            return apology('must provide symbol')
        elif not request.form.get('shares') or int(request.form.get('shares')) <= 0:
            return apology('must provide a positive integer as a number of shares')
        else:
            result = lookup(request.form.get('symbol'))
            shares = int(request.form.get('shares'))
            price = result['price']
            total_price = price * shares
            id = session.get('user_id')
            # Ensuring that the user has enough cash to buy stock
            rows = db.execute("SELECT * FROM users WHERE id=:id", id=session.get('user_id'))
            cash = rows[0]['cash']
            if cash >= total_price:
                db.execute("INSERT INTO shares(symbol,name, shares, price, id)\
                VALUES(:symbol, :name, :shares, :price, :id)\
                ", symbol=request.form.get('symbol'), name=result['name'], shares=shares, price=price, id=id)
                db.execute("INSERT INTO history(symbol, shares, price, datetime, user_id, name)\
                VALUES(:symbol, :shares, :price, :datetime, :user_id, :name)\
                ", symbol=request.form.get('symbol'), shares=shares, price=price, datetime=datetime.now(), user_id=id, name=result['name'])
                rows = db.execute("SELECT * FROM users WHERE id=:id", id=id)
                cash = rows[0]['cash']
                db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash = (cash - total_price), id = id)
                session['message']  = 'Bought!'
                return redirect('/')
            else:
                return apology("Sorry! You don't have enough cash to buy shares")

    else:
        return render_template('buy.html')

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Need to access all history form the database
    histories= db.execute("SELECT * FROM history WHERE user_id=:user_id", user_id=session.get('user_id'))
    print(f'histories: {histories}')
    return render_template('history.html', histories=histories, usd=usd)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Ensuring user has entered symbol
        if not request.form.get('symbol'):
            return apology('must provide symbol')

        symbol = request.form.get("symbol")
        quoted = lookup(symbol)
        if quoted  ==  None:
            return apology('Sorry, there is no stock with that symbol!')
        return render_template('quoted.html', quoted=quoted)
    else:
        return render_template('quote.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensuring user entered a username
        if not request.form.get('username'):
            return apology("must provide username", 403)
        # Ensuring user entered password
        elif not request.form.get('password'):
            return apology("must provide password", 403)
        # Ensuring user re-entered password
        elif not request.form.get("re-entered-password"):
            return apology("must re-enter password", 403)
        # Check if password matches
        if request.form.get("password") != request.form.get("re-entered-password"):
            return apology("passwords do not match", 403)
        else:
            username = request.form.get("username")
            # Hashing the password
            hash = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users(hash, username) VALUES(:hash, :username)", hash=hash, username=username)
            return redirect('/login')
    else:
        return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == 'POST':
        # Ensuring user has entered symbol
        if not request.form.get('symbol'):
            return apology("You must enter a symbol to sell stock")
        # Ensuring user has entered shares
        if not request.form.get('shares') or int(request.form.get('shares')) <= 0:
            return apology("You must enter number of share to sell stock")
        stock = db.execute("SELECT * FROM shares WHERE id=:id AND symbol=:symbol\
        ", id=session.get('user_id'), symbol=request.form.get('symbol'))
        if len(stock) == 0:
            return apology("You don't have stocks to sell")
        if stock[0]['shares'] >= int(request.form.get('shares')):
            result = lookup(request.form.get('symbol'))
            selling_price = result['price'] * int(request.form.get('shares'))
            buying_price = stock[0]['price'] * stock[0]['shares']
            user = db.execute("SELECT * FROM users WHERE id=:id", id=session.get('user_id'))
            cash = user[0]['cash'] + (selling_price - buying_price)
            if stock[0]['shares'] == int(request.form.get('shares')):
                db.execute("DELETE FROM shares WHERE id=:id AND symbol=:symbol\
                ", id=session.get('user_id'), symbol=request.form.get('symbol'))
            else:
                db.execute("UPDATE shares SET shares=:shares WHERE id=:id AND symbol=:symbol\
                ", shares=(stock[0]['shares'] - int(request.form.get('shares'))), id=session.get('user_id'), symbol=request.form.get('symbol'))
            db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash, id=session.get('user_id'))
            db.execute("INSERT INTO history(symbol, shares, price, datetime, user_id, name)\
            VALUES(:symbol, :shares, :price, :datetime, :user_id, :name)\
            ", symbol=request.form.get('symbol'), shares=-int(request.form.get('shares')), price=result['price'], datetime=datetime.now(), user_id=session.get('user_id'), name=result['name'])
        session['message']  = 'Sold!'
        return redirect('/')
    else:
        result = db.execute("SELECT * FROM shares WHERE id=:id", id=session.get('user_id'))
        symbols = []
        for stock in result:
            if stock['symbol'] not in symbols:
                symbols.append(stock['symbol'])

        return render_template('sell.html', symbols=symbols)

@app.route("/add", methods=['GET', 'POST'])
@login_required
def addcash():
    if request.method == 'POST':
        if not request.form.get('amount'):
            return apology("You must enter amount to add")
        amount = request.form.get('amount')
        user = db.execute('SELECT * FROM users WHERE id=:id', id=session.get('user_id'))
        updated_cash = user[0]['cash'] + float(amount)
        db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=updated_cash, id=session.get('user_id'))
        session['message']  = 'Succefully!'
        return redirect('/')
    else:
        return render_template('addcash.html')
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

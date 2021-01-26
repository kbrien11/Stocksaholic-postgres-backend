from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
from util import hash_pass,generate_key, crypto_market_cap,Crypto_Exchange_Data, seven_day_crypto_chart, crypto_coins, Gemini_volume,Coinbase_volume,Binance_volume,get_price, generate_key,get_price_of_ticker, top_gainers,top_losers,crypto_news,usd_chart,crypto_stats, Logo,tracking_chart,related_Companies,Crypto,stats,stats_low,pe_ratio,day_change,stock_description,chart,ytd_change,crypto_chart
from flask_marshmallow import Marshmallow
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.sql import func
from sqlalchemy import func,desc,and_
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mbdask1013@localhost/stocks-backend'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
ma = Marshmallow(app)

def create_session(config):
    engine = create_engine(config['DATABASE_URL'])
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}
    return session


class User(db.Model):
    pk = db.Column(db.Integer, primary_key = True,unique = True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(200))
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(30))
    api_key = db.Column(db.String(32), unique = True,default = "")
    balance = db.Column(db.Integer, default =0)
    equity = db.Column(db.Integer, default =0)

    def __init__(self,pk,email,password,first_name,last_name,api_key,balance,equity):
        self.pk = pk
        self.email = email
        self.password = hash_pass(password)
        self.first_name = first_name
        self.last_name = last_name
        self.api_key = api_key
        self.balance = balance
        self.equity = equity

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
         model = User
         load_instance = True
         fields = ('pk','email','password','first_name','last_name','api_key','balance','equity')
    
user_schemas = UserSchema(many=True)   
   
user_schema = UserSchema()   
     





class Date(db.Model):
    pk = db.Column(db.Integer, primary_key = True)
    user_pk = db.Column(db.Integer,db.ForeignKey('user.pk'))
    equity = db.Column(db.Integer)
    unix_time = db.Column(db.String(15))

    def __init__(self,pk,user_pk,equity,unix_time = ""):
        self.pk = pk
        self.user_pk = user_pk
        self.equity = equity
        self.unix_time = unix_time

class DateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
         model = Date
         load_instance = True
         fields = ('pk','user_pk','equity','unix_time')

date_schemas = DateSchema(many=True)   
   
date_schema = DateSchema()   


class Positions(db.Model):
    pk = db.Column(db.Integer, primary_key = True)
    user_pk = db.Column(db.Integer,db.ForeignKey('user.pk'))
    ticker = db.Column(db.String(30))
    number_shares = db.Column(db.Integer)
    equity = db.Column(db.Integer)

    def __init__(self,pk,user_pk,ticker,number_shares,equity):
        self.pk = pk
        self.user_pk = user_pk
        self.ticker = ticker
        self.number_shares = number_shares
        self.equity = equity


class PositionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
         model = Positions
         load_instance = True
         fields = ('pk','user_pk','ticker','number_shares','equity')

position_schemas = PositionSchema(many=True)   
   
position_schema = PositionSchema()   
     

class Tracking(db.Model):
    pk = db.Column(db.Integer, primary_key = True)
    user_pk = db.Column(db.Integer,db.ForeignKey('user.pk'))
    ticker = db.Column(db.String(30))
    tracking = db.Column(db.Integer,default = 0)

    def __init__(self,pk,user_pk,ticker,tracking):
        self.pk = pk
        self.user_pk = user_pk
        self.ticker = ticker
        self.tracking = tracking

class TrackingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
         model = Tracking
         load_instance = True
         fields = ('pk','user_pk','ticker','tracking')

tracking_schemas = TrackingSchema(many=True)   
   
tracking_schema = TrackingSchema()   


class Trades(db.Model):
    pk = db.Column(db.Integer, primary_key = True)
    user_pk = db.Column(db.Integer,db.ForeignKey('user.pk'))
    ticker = db.Column(db.String(30))
    number_shares = db.Column(db.Integer)
    trade_type = db.Column(db.String(15))
    unix_time = db.Column(db.String(15))
    equity = db.Column(db.Integer)

    def __init__(self,pk, user_pk, ticker, number_shares,equity, trade_type ="", unix_time=""):
        self.pk =pk
        self.user_pk = user_pk
        self.ticker = ticker
        self.number_shares = number_shares
        self.trade_type = trade_type
        self.unix_time = unix_time
        self.equity = equity

class TradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
         model = Trades
         load_instance = True
         fields = ('pk','user_pk','ticker','number_shares','trade_type','unix_time','equity')

trades_schemas = TradeSchema(many=True)   
   
trade_schema = TradeSchema()   



# authentication


# creating user

@app.route('/api/create_user', methods=['POST'])
def create_account():
        if request.method == 'POST':
            data = request.get_json()
            
            # email, password, balance = views.create_account()
            new_account = User(None, email =data['email'], password =data['password'],first_name =data['first_name'],last_name =data['last_name'], api_key = None, balance = None, equity = None)
            new_account.api_key = generate_key()
            db.session.add(new_account)
            db.session.commit()
            print(new_account.api_key)
            return user_schema.jsonify(new_account)

 #  logging user in

@app.route('/api/login',methods =['POST'])
def login():
    data = request.get_json()
    if data:
        email = data['email']
        password = hash_pass(data['password'])
        user = User.query.filter_by(email=email,password=password).first()
        if user:
            print(user)
            result = user_schema.dump(user)
            return user_schema.jsonify(result)
        return False



# gainer/loser info

@app.route('/api/top_gainers/<api_key>',methods = ['GET'])
def gainers(api_key):
    user = User.query.filter_by(api_key=api_key)
    if user:
        gainers = top_gainers()
        return jsonify({"gainers":gainers})
    return jsonify({"error":"failed"})

@app.route('/api/top_losers/<api_key>',methods = ['GET'])
def losers(api_key):
    user = User.query.filter_by(api_key=api_key)
    if user:
        losers = top_losers()
        return jsonify({"losers":losers})
    return jsonify({"error":"failed"})



# crypto stuff

@app.route('/api/crypto_Chart/<ticker>/<api_key>', methods=['GET'])
def crypto_chart_data(ticker,api_key):
    user = User.query.filter_by(api_key=api_key)
    if user:
        data = crypto_chart(ticker)
        seven_day_chart = seven_day_crypto_chart(ticker)
        return jsonify({"chart":data,"sevenDayChart":seven_day_chart})
    return jsonify({"error":"failed"})

@app.route('/api/crypto_price/<ticker>/<api_key>', methods=['GET'])
def lookupCrypto(ticker,api_key):
    user = User.query.filter_by(api_key=api_key)
    if user:
        price = Crypto(ticker)
        return jsonify({'crypto':price})
    return jsonify({"error":"failed"})



@app.route('/api/crypto_news', methods=['GET'])
def crypto_news_story():
    crypto_news_data = crypto_news()
    return jsonify({"cryptoNews":crypto_news_data})

@app.route('/api/exchange_volume', methods=['GET'])
def Exchange_volume():
    Gemini = Gemini_volume()
    Coinbase = Coinbase_volume()
    Binance = Binance_volume()
    return jsonify({"Gemini":Gemini, "Coinbase":Coinbase, "Binance":Binance})

@app.route('/api/crypto_market_cap', methods =['GET'])
def market():
    market_cap = crypto_market_cap()
    return jsonify({"marketCap":market_cap})

@app.route('/api/exchange_data',methods=['GET'])
def exchange_data():
    data = Crypto_Exchange_Data()
    return jsonify({"data":data})

@app.route('/api/exchange_coins',methods=['GET'])
def coins_data():
    data = crypto_coins()
    return jsonify({"data":data})

@app.route('/api/weekly_crypto_chart/<ticker>',methods=['GET'])
def weekly_crypto_chart(ticker):
    seven_day_chart = seven_day_crypto_chart(ticker)
    return jsonify({"sevenDayChart":seven_day_chart})



#  buying and seeling stocks and deposit funds

@app.route('/api/<api_key>/<amount>', methods=['POST'])
def deposit(api_key,amount):
     user = db.session.query(User).filter_by(api_key=api_key).first()
     if user:
        balance = user.balance
        balance += int(amount)
        user.balance = balance
        db.session.commit()
        print(user.balance)
        return user_schema.jsonify(user)
     else:
        return jsonify({"error":"authentication error"})


@app.route('/api/<api_key>/balance', methods=['GET'])
def get_balanace(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        result = user_schema.dump(user)
        return user_schema.jsonify(result)
    return jsonify({'error':'invalid key'})





@app.route('/api/<api_key>/buy', methods=['POST'])
def buy(api_key):
    data=request.get_json()
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:
        bal = user.balance
        equ = user.equity
        ticker = request.get_json()['ticker']
        amount = request.get_json()['amount']
        Deposit = request.get_json()['type']
        current_price = get_price_of_ticker(ticker) * int(amount)
        if user.balance < current_price:
            return jsonify({"Insufficient_funds":"Insufficient_funds"})
        old_position = db.session.query(Positions).filter_by(ticker=ticker,user_pk=user.pk).first()
        if old_position:
            old_position.equity+=current_price
            old_position.number_shares += int(amount)
            bal -= current_price
            user.balance = bal
            equ += current_price
            user.equity = equ
            db.session.commit()
        else:
            current_position = Positions(None,user_pk = user.pk, ticker = ticker,number_shares = amount,equity = current_price)
            bal -= current_price
            user.balance = bal
            equ += current_price
            user.equity = equ
            db.session.add(current_position)
            db.session.commit()
        time=data.get('unix_time')
        new_trade = Trades(None,user_pk = user.pk, ticker = ticker,number_shares = amount,trade_type = Deposit,unix_time = time,equity = current_price)
        db.session.add(new_trade)
        db.session.commit()
        return user_schema.jsonify(user)
    return jsonify({'error':'invalid key'})


@app.route('/api/<api_key>/sell', methods=['POST'])
def sell(api_key):
    data=request.get_json()
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:
        ticker = request.get_json()['ticker']
        amount = request.get_json()['amount']
        Withdrawal = request.get_json()['type']
        position = db.session.query(Positions).filter_by(ticker=ticker,user_pk=user.pk).first()
        if position.number_shares < int(amount):
             return jsonify({"Insufficient_funds":"Insufficient_funds"})
        else:

            transaction_price = get_price_of_ticker(ticker) * int(amount)
            user.balance += (transaction_price)
            user.equity -= transaction_price
            position.equity -= (transaction_price)
            position.number_shares -= int(amount)
            time=data.get('unix_time')
            new_trade = Trades(None,user_pk = user.pk, ticker = ticker,number_shares = amount,trade_type = Withdrawal,unix_time = time,equity = transaction_price)
            db.session.add(new_trade)
            db.session.commit()
            return user_schema.jsonify(user)
    return jsonify({'error':'invalid key'})




# stocks page


@app.route('/api/price/<ticker>/<api_key>', methods=['GET'])
def lookup(ticker,api_key):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:
        price = get_price(ticker)
        description = stock_description(ticker)
        chart_data = chart(ticker)
        logo = Logo(ticker)
        related = related_Companies(ticker)
        return jsonify({'current_price':price,"des":description,"chartData":chart_data,"logo":logo})
    return jsonify({"error":"failed"})


#  sending stocks/tickets to track-- post request
@app.route('/api/track/<ticker>/<api_key>', methods =['POST'])
def track(ticker,api_key):
    data = request.get_json()
    ticker = data.get('ticker')
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:
        new_track = Tracking(None,user_pk = user.pk, ticker = ticker,tracking = None)
        result = tracking_schema.dump(new_track)
        new_track.tracking = 1
        db.session.add(new_track)
        db.session.commit()
        return tracking_schema.jsonify(result)
    return jsonify({"error":"no track added"})

#  getting balance for stocks page
@app.route('/api/<token>/balance', methods=['GET'])
def get_bal(token):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:
        result = user_schema.dump(user)
        return jsonify({'balance': float(account.balance)})
    return jsonify({'error':'invalid key'})

#  tracking chart data-- price and change
@app.route('/api/prices/<ticker>/<api_key>', methods=['GET'])
def look_price(api_key,ticker):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:
        price = get_price_of_ticker(ticker)
        change = day_change(ticker)
        # tracker = tracking_chart(ticker)
        return jsonify({'current_price':price,'change':change})
    return jsonify({"error":"failed"})

#  tracking chart-- chart data

@app.route('/api/tracking_chart/<ticker>/<api_key>', methods=['GET'])
def tracker_chart(api_key,ticker):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:      
        tracker = tracking_chart(ticker)
        return jsonify({"tracker":tracker})
    return jsonify({"error":"failed"})


# Homepage/dashboard

# getting the positions for the home page

@app.route('/api/<api_key>/positions',methods=['GET'])
def get_positions(api_key):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:
        zero = 0
        res = db.session.query(Positions).filter_by(user_pk =user.pk).filter(Positions.number_shares >0).order_by(Positions.equity.desc()).limit(5)
        result = position_schemas.dump(res)
        for pos in res:
            number_shares = pos.number_shares
            if pos.number_shares < 0:
                pass
            else:
                equ = pos.equity
                pk = pos.pk
                ticker = pos.ticker
                equ = 0
                equ = get_price_of_ticker(ticker) * int(number_shares)
                pos.equity = equ
                pos.ticker = ticker
                pos.number_shares = number_shares
                print(pos.number_shares)
                db.session.commit()
        return position_schemas.jsonify(result)

@app.route('/api/logo/<ticker>',methods=['GET'])     
def get_logo(ticker):
    logo = Logo(ticker)
    return jsonify({"logo":logo})


#  sending the date to the database and then updating the equity in the database

@app.route('/api/equity_date/<api_key>',methods=['POST'])
def get_date(api_key):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    result = user_schema.dump(user)
    if user:
        equity = user.equity
        data = request.get_json()
        time = data.get("unix_time")
        new_date = Date(None,user.pk,equity,time)
        db.session.add(new_date)
        db.session.commit()
        return user_schema.jsonify(user)
    return jsonify({"token": ""})


# chart of equity by each day

@app.route('/api/equity_chart/<api_key>', methods = ['GET'])
def equity_chart(api_key):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    result = user_schema.dump(user)
    if user:
        output = db.session.query(Date).filter_by(user_pk=user.pk).distinct(Date.unix_time).order_by(Date.unix_time.desc())
        chart = date_schemas.dump(output)
        return date_schemas.jsonify(chart)
    return ({"error":"error"})

#  home equity that dates updated when price of stocks change

@app.route('/api/<api_key>/equity', methods=['GET'])
def get_equ(api_key):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    data = request.get_json()
    solutions = []
    if user:
        res = db.session.query(Positions).filter_by(user_pk=user.pk)
        result = position_schemas.dump(res)
        for i in res:
            equ = i.equity
            solutions.append(equ)
        total = sum(solutions)
        user.equity = total
        db.session.commit()
        return user_schema.jsonify(user)
    return jsonify({'error':'invalid key'})


# home usd/eur chart

@app.route('/api/<api_key>/usd_chart',methods=['GET'])
def usd_daily_chart(api_key):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:
        return jsonify({"USD":usd_chart()})
    return jsonify({'error':'invalid key'})


#  home transactions

@app.route('/api/<api_key>/recent',methods=['GET'])
def get_home_trades(api_key):
    user = db.session.query(User).filter_by(api_key=api_key).first()
    if user:
        trades = db.session.query(Trades).filter_by(user_pk=user.pk).order_by(Trades.unix_time.desc()).limit(5)
        result = trades_schemas.dump(trades)
        return trades_schemas.jsonify(result)
    return jsonify({'error':'invalid key'})

#  getting tracking stocks for homepage 
@app.route('/api/gettracking/<api_key>', methods =['GET'])
def get_tracking(api_key):
     user = db.session.query(User).filter_by(api_key=api_key).first()
     if user:
        tracks = db.session.query(Tracking).filter_by(user_pk = user.pk, tracking = 1).all()
        result = tracking_schemas.dump(tracks)
        return tracking_schemas.jsonify(result)
     return jsonify({"error":"failed"})

#  history page

#  getting trade history

@app.route('/api/<api_key>/trades',methods=['GET'])
def get_trades(api_key):
     user = db.session.query(User).filter_by(api_key=api_key).first()
     if user:
        result = db.session.query(Trades).filter_by(user_pk = user.pk).all()
        total_trades = trades_schemas.dump(result)
        return trades_schemas.jsonify(total_trades)
     return jsonify({'error':'invalid key'})

#   test route

@app.route('/', methods=['GET'])
def hi ():
    return jsonify ({"hi":"there"})


if __name__ == "main":
    app.run()
    
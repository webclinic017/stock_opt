import pandas as pd
from flask import Flask, render_template, redirect, request, session


app = Flask(__name__)

# 
# in show.html need to change month in each table
exp_date_zerodha = '2021-07-29'  

def create_url_for_options(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url

df = pd.read_csv('https://api.kite.trade/instruments')
# df1 is for futures
df1 = df
df = df[(df['segment'].str.contains("NFO-OPT") == True)]
df.drop(df[df['name'] == 'NIFTY'].index, inplace=True)
df.drop(df[df['name'] == 'BANKNIFTY'].index, inplace=True)
df.drop(df[df['name'] == 'FINNIFTY'].index, inplace=True)
ls = (df.expiry.unique())
print(ls[0])
# exp_date = ls[0]
df.drop(df[df['expiry'] != exp_date_zerodha].index, inplace=True)
df['url'] = df.apply(lambda row: create_url_for_options(row), axis=1)


def create_url_for_futures(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NFO-FUT/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url

df1 = df1[(df1['segment'].str.contains("NFO-FUT") == True)]
df1.drop(df1[df1['expiry'] != exp_date_zerodha].index, inplace=True)
df1['url'] = df1.apply(lambda row: create_url_for_futures(row), axis=1)



@app.route('/')
@app.route('/home', methods=["GET", "POST"])
def home():

    global df

    if request.method == "POST":
        statename = request.form.get("statename")
        statename = str(statename)
        print(statename)
        global date
        date = statename
        print(type(date))

    lis = df.name.unique()
    
    return render_template('index.html',lis = lis)


@app.route('/get_strikes', methods=["GET", "POST"])
def somework():

    global df

    ce = df
    pe = df
    if request.method == "POST":
        statename = request.form.get("statename")
        statename = str(statename)
        print(statename)    


        ce = ce[(ce['url'].str.contains(statename) == True)
                & (ce['instrument_type'] == 'CE')]
        ce_list = ce['url'].tolist()

        pe = pe[(pe['url'].str.contains(statename) == True)
                & (pe['instrument_type'] == 'PE')]
        pe_list = pe['url'].tolist()
        
        return render_template('show.html', ce_list=ce_list,pe_list=pe_list)

    return "hello"


@app.route('/get_fut', methods=["GET", "POST"])
def fut():

    global df1

    df2 = df1
    
    statename = request.args.get('statename')
    print(statename)
   
    ans = df2.loc[df2['url'].str.contains(statename, case=False)]
    lis = ans['url'].tolist()
    print(lis[0])
    req_url = lis[0]

    return redirect(req_url)

    return "hello"


@app.route('/get_opt', methods=["GET", "POST"])
def opt():
    global df

    ce = df
    pe = df
  
    statename = request.args.get('statename')
    print(statename)
    
   
    ce = ce[(ce['url'].str.contains(statename) == True)
            & (ce['instrument_type'] == 'CE')]
    ce_list = ce['url'].tolist()

    pe = pe[(pe['url'].str.contains(statename) == True)
            & (pe['instrument_type'] == 'PE')]
    pe_list = pe['url'].tolist()

    return render_template('show.html', ce_list=ce_list, pe_list=pe_list)




@app.route('/req_opt', methods=["GET", "POST"])
def reqopt():
    global df

    ce = df
    pe = df
  
    statename = request.args.get('statename')
    ltp = request.args.get('ltp')
    print(statename)
    print(ltp)
    
    ltp = int(float(ltp))
   
    ce = ce[(ce['url'].str.contains(statename) == True)
            & (ce['instrument_type'] == 'CE')]
    # ce_list = ce['url'].tolist()
    idx = ce['strike'].lt(ltp).argmin()
    out = ce['url'].iloc[max(idx-4, 0):min(idx+4, len(df))]
    ce_list = out.tolist()
    print(ce_list)

    pe = pe[(pe['url'].str.contains(statename) == True)
            & (pe['instrument_type'] == 'PE')]
    # pe_list = pe['url'].tolist()
    idx = pe['strike'].lt(ltp).argmin()
    out = pe['url'].iloc[max(idx-4, 0):min(idx+3, len(df))]
    pe_list = out.tolist()
    print(pe_list)

    return render_template('show.html', ce_list=ce_list, pe_list=pe_list)


if __name__ == '__main__':
    app.run(debug=True)


# http://localhost:5000/abcd?user = 123

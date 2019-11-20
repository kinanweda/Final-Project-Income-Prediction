from flask import Flask, render_template, request, redirect
from datetime import date, timedelta
import numpy as np
import pandas as pd
import matplotlib as plt
import plotly.graph_objects as go
import requests,plotly,json,folium,mysql.connector, sqlalchemy, pickle, sqlalchemy,datetime


app = Flask(__name__)

db = mysql.connector.connect(
    host =  '127.0.0.1',
    port = 3306,
    user = 'kinanweda',
    passwd = '12345',
    database = 'ProjectAkhir2' 
)


conn = sqlalchemy.create_engine(
    'mysql+pymysql://kinanweda:Jimbamamba22@localhost:3306/ProjectAkhir2'
)

country_geo = 'world-countries.json'

df = pd.read_csv('income_evaluation.csv')
df.columns = ['age','workclass','finalweight',
              'education','educationNumber','maritalStatus',
              'occupation','relationship','race',
              'sex','capitalGain','capitalLoss',
              'hoursperweek','nativeCountry','income']
categorical = [i for i in df.columns.drop(['income']) if df[i].dtype == 'O']
for i in categorical:
    df[i] = [col.replace(' ','') for col in df[i].values]
cache={'foo':0,'page':'data'}

def loadlemar():
    global lemar
    with open('lemar.pickle','rb') as j:
        lemar = pickle.load(j)

def loadlenc():
    global lenc
    with open('lenc.pickle','rb') as j:
        lenc = pickle.load(j)

def loadleoc():
    global leoc
    with open('leoc.pickle','rb') as j:
        leoc = pickle.load(j)

def loadlerc():
    global lerc
    with open('lerc.pickle','rb') as j:
        lerc = pickle.load(j)

def loadlerl():
    global lerl
    with open('lerl.pickle','rb') as j:
        lerl = pickle.load(j)

def loadlesx():
    global lesx
    with open('lesx.pickle','rb') as j:
        lesx = pickle.load(j)

def loadlewc():
    global lewc
    with open('lewc.pickle','rb') as x :
        lewc = pickle.load(x)

def loadModel():
    global model
    with open('XGB.pickle','rb') as y :
        model = pickle.load(y)

def loadScaler():
    global scaler
    with open('scaler.pickle','rb') as f :
        scaler = pickle.load(f)


def create_plot():
    df = pd.read_csv('income_evaluation.csv')
    df.columns = ['age','workclass','finalweight',
                'education','educationNumber','maritalStatus',
                'occupation','relationship','race',
                'sex','capitalGain','capitalLoss',
                'hoursperweek','nativeCountry','income']

    categorical = [i for i in df.columns.drop(['income']) if df[i].dtype == 'O']
    for i in categorical:
        df[i] = [col.replace(' ','') for col in df[i].values]

    df = df.replace('?', np.NaN)
    df['workclass'].fillna(df['workclass'].mode()[0], inplace=True)
    labels = (df['workclass'].value_counts()/(df['workclass'].value_counts()+len(df))*100).index
    values = (df['workclass'].value_counts()/(df['workclass'].value_counts()+len(df))*100).values

    data=[go.Pie(labels=labels, values=values, title='Pie Chart Workclass', titleposition='top center', titlefont=dict(size=18))]
    graphJson = json.dumps(data,cls=plotly.utils.PlotlyJSONEncoder)
    return graphJson


def bar_plot():
    body = request.form
    df = pd.read_csv('income_evaluation.csv')
    df.columns = ['age','workclass','finalweight',
                'education','educationNumber','maritalStatus',
                'occupation','relationship','race',
                'sex','capitalGain','capitalLoss',
                'hoursperweek','nativeCountry','income']
    categorical = [i for i in df.columns.drop(['income']) if df[i].dtype == 'O']
    for i in categorical:
        df[i] = [col.replace(' ','') for col in df[i].values]
    df = df.replace('?', np.NaN)
    df['workclass'].fillna(df['workclass'].mode()[0], inplace=True)
    x1 = sorted(df[df['income']==' <=50K']['workclass'].unique())
    y1 = df[df['income']==' <=50K']['workclass'].value_counts().sort_index().values
    x2 = sorted(df[df['income']==' >50K']['workclass'].unique())
    y2 = df[df['income']==' >50K']['workclass'].value_counts().sort_index().values
    trace_comp0 = go.Bar(
            x=x1,
            y=y1,
            name = '<=50K'
        )
    trace_comp1 = go.Bar(
            x=x2,
            y=y2,
            name = '>50K'
        )
    data = [trace_comp0,trace_comp1]

    barGraph = json.dumps(data,cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph

def bar_plot1():
    body = request.form
    df = pd.read_csv('income_evaluation.csv')
    df.columns = ['age','workclass','finalweight',
                'education','educationNumber','maritalStatus',
                'occupation','relationship','race',
                'sex','capitalGain','capitalLoss',
                'hoursperweek','nativeCountry','income']
    categorical = [i for i in df.columns.drop(['income']) if df[i].dtype == 'O']
    for i in categorical:
        df[i] = [col.replace(' ','') for col in df[i].values]
    df = df.replace('?', np.NaN)
    df['occupation'].fillna(df['occupation'].mode()[0], inplace=True)
    x1 = sorted(df[df['income']==' <=50K']['occupation'].unique())
    y1 = df[df['income']==' <=50K']['occupation'].value_counts().sort_index().values
    x2 = sorted(df[df['income']==' >50K']['occupation'].unique())
    y2 = df[df['income']==' >50K']['occupation'].value_counts().sort_index().values
    trace_comp0 = go.Bar(
            x=x1,
            y=y1,
            name = '<=50K'
        )
    trace_comp1 = go.Bar(
            x=x2,
            y=y2,
            name = '>50K'
        )
    data = [trace_comp0,trace_comp1]

    barGraph1 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph1

def bar_plot2():
    body = request.form
    df['education'].fillna(df['education'].mode()[0], inplace=True)
    x1 = sorted(df[df['income']==' <=50K']['education'].unique())
    y1 = df[df['income']==' <=50K']['education'].value_counts().sort_index().values
    x2 = sorted(df[df['income']==' >50K']['education'].unique())
    y2 = df[df['income']==' >50K']['education'].value_counts().sort_index().values
    trace_comp0 = go.Bar(
            x=x1,
            y=y1,
            name = '<=50K'
        )
    trace_comp1 = go.Bar(
            x=x2,
            y=y2,
            name = '>50K'
        )
    data = [trace_comp0,trace_comp1]

    barGraph2 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph2

def bar_plot3():
    body = request.form
    df['maritalStatus'].fillna(df['maritalStatus'].mode()[0], inplace=True)
    x1 = sorted(df[df['income']==' <=50K']['maritalStatus'].unique())
    y1 = df[df['income']==' <=50K']['maritalStatus'].value_counts().sort_index().values
    x2 = sorted(df[df['income']==' >50K']['maritalStatus'].unique())
    y2 = df[df['income']==' >50K']['maritalStatus'].value_counts().sort_index().values
    trace_comp0 = go.Bar(
            x=x1,
            y=y1,
            name = '<=50K'
        )
    trace_comp1 = go.Bar(
            x=x2,
            y=y2,
            name = '>50K'
        )
    data = [trace_comp0,trace_comp1]

    barGraph3 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph3

def bar_plot4():
    body = request.form
    df['relationship'].fillna(df['relationship'].mode()[0], inplace=True)
    x1 = sorted(df[df['income']==' <=50K']['relationship'].unique())
    y1 = df[df['income']==' <=50K']['relationship'].value_counts().sort_index().values
    x2 = sorted(df[df['income']==' >50K']['relationship'].unique())
    y2 = df[df['income']==' >50K']['relationship'].value_counts().sort_index().values
    trace_comp0 = go.Bar(
            x=x1,
            y=y1,
            name = '<=50K'
        )
    trace_comp1 = go.Bar(
            x=x2,
            y=y2,
            name = '>50K'
        )
    data = [trace_comp0,trace_comp1]

    barGraph4 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph4

def bar_plot5():
    body = request.form
    df['race'].fillna(df['race'].mode()[0], inplace=True)
    x1 = sorted(df[df['income']==' <=50K']['race'].unique())
    y1 = df[df['income']==' <=50K']['race'].value_counts().sort_index().values
    x2 = sorted(df[df['income']==' >50K']['race'].unique())
    y2 = df[df['income']==' >50K']['race'].value_counts().sort_index().values
    trace_comp0 = go.Bar(
            x=x1,
            y=y1,
            name = '<=50K'
        )
    trace_comp1 = go.Bar(
            x=x2,
            y=y2,
            name= '>50K'
        )
    data = [trace_comp0,trace_comp1]

    barGraph5 = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return barGraph5

@app.route('/')
def home():
    return render_template('reg.html')

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    requestForm = request.form.to_dict()
    header = df.columns.tolist()
    length = df.iloc[0:100].index
    pie = create_plot()
    bar = bar_plot()
    bar1 = bar_plot1()
    bar2 = bar_plot2()
    bar3 = bar_plot3()
    bar4 = bar_plot4()
    bar5 = bar_plot5()
    dfPredict = pd.read_sql('dataset', conn)
    dfPredict.drop('education',axis=1,inplace=True)
    dfPredicts = dfPredict.copy()
    categorical = [i for i in dfPredicts.columns.drop(['nativeCountry']) if dfPredicts[i].dtype == 'O']
    numerical = [i for i in dfPredicts.columns.drop(['nativeCountry']) if dfPredicts[i].dtype != 'O']
    dfPredicts['workclass'] = lewc.transform(dfPredicts['workclass'])
    dfPredicts['maritalStatus'] = lemar.transform(dfPredicts['maritalStatus'])
    dfPredicts['occupation'] = leoc.transform(dfPredicts['occupation'])
    dfPredicts['relationship'] = lerl.transform(dfPredicts['relationship'])
    dfPredicts['race'] = lerc.transform(dfPredicts['race'])
    dfPredicts['sex'] = lesx.transform(dfPredicts['sex'])
    dfPredicts['nativeCountry'] = lenc.transform(dfPredicts['nativeCountry'])
    dfScaled = pd.DataFrame(scaler.transform(dfPredicts[numerical]),columns=dfPredicts[numerical].columns)
    dfLabeled = pd.DataFrame(dfPredicts[categorical],columns=df[categorical].columns)
    dfLabeled = dfLabeled.reset_index(drop=True)
    dfScaled = pd.concat([dfLabeled,dfScaled],axis=1)
    predictTest = model.predict(dfScaled)
    probaTest = model.predict_proba(dfScaled)
    dfPredict["income"] = predictTest
    dfPredict['income'] = dfPredict.apply(lambda x : '<=50K' if x['income'] == 0 else '>50K',axis=1)
    dfPredict['Probability'] = f'{round(probaTest.max()*100,2)}%'
    dfPredict = dfPredict.reset_index()
    head = dfPredict.columns.tolist()
    lengths = dfPredict.index
    if request.method == 'POST' :
        if requestForm['submit_button'] == 'Next': 
            cache['foo'] += 1
            length = df.iloc[(cache['foo']*100):((cache['foo']*100)+100)].index
        elif requestForm['submit_button'] == 'Previous':
            if cache['foo'] == 0:
                cache['foo'] = 0
                length = df.iloc[(cache['foo']*100):((cache['foo']*100)+100)].index
            else:
                cache['foo'] -= 1
                length = df.iloc[(cache['foo']*100):((cache['foo']*100)+100)].index   
        elif requestForm['submit_button'] in list(df['workclass']):
                length = df[df['workclass'] == requestForm['submit_button']].index
                body=request.form
        # elif requestForm['submit_button'] in list(df['Country']):
        #         length = df[df['Country'] == requestForm['submit_button']].index
        elif requestForm['submit_button'] == 'Fullscreen':
            return redirect('/map')  
    return render_template('index.html',dfPrediksi = dfPredict, head = head, lengths = lengths, headers=header, length=length, df=df, page=cache['page'], plot = pie,plotbar= bar , plotbar1=bar1, plotbar2=bar2,plotbar3=bar3,plotbar4=bar4,plotbar5=bar5)

@app.route('/map')
def foliumMap():
    df = pd.read_csv('income_evaluation.csv')
    df.columns = ['age','workclass','finalweight',
                'education','educationNumber','maritalStatus',
                'occupation','relationship','race',
                'sex','capitalGain','capitalLoss',
                'hoursperweek','nativeCountry','income']

    categorical = [i for i in df.columns.drop(['income']) if df[i].dtype == 'O']
    for i in categorical:
        df[i] = [col.replace(' ','') for col in df[i].values]

    df = df.replace('?', np.NaN)

    df['nativeCountry'].fillna(df['nativeCountry'].mode()[0], inplace=True)

    df['nativeCountry'] = df['nativeCountry'].replace('United-States','United States of America')
    df['nativeCountry'] = df['nativeCountry'].replace('Puerto-Rico','Puerto Rico')
    df['nativeCountry'] = df['nativeCountry'].replace('Trinadad&Tobago','Trinidad and Tobago')
    df['nativeCountry'] = df['nativeCountry'].replace('Holand-Netherlands','Netherlands')
    df['nativeCountry'] = df['nativeCountry'].replace('El-Salvador','El Salvador')

    idCountry = pd.read_json('world-countries.json')
    idCountry['features']
    a = [i['id'] for i in idCountry['features']]
    b = [j['properties']['name'] for j in idCountry['features']]

    listIdCountry = pd.DataFrame({
            'Negara':b,
            'id' : a,
    })

    a = 0
    listTotal = []
    listCountry = []
    listPct = []
    for i,item in enumerate(df['nativeCountry'].unique()):
        listTotal.append(df[(df['nativeCountry']== item ) & True].shape[0])
        a = a + df[(df['nativeCountry']== item ) & True].shape[0]
        listCountry.append(item)
        listPct.append(round((listTotal[i]/df.shape[0])*100,2))

    country = pd.DataFrame({'Negara' : df['nativeCountry'].unique(),'Total Customer' : listTotal,'Percentage' : listPct})
    country = pd.merge(country,listIdCountry,left_on ='Negara', right_on ='Negara',how='left')
    map = folium.Map(
        location=[53.2202105,-22.2277193], zoom_start=4
    )

    map.choropleth(geo_data=country_geo, data=country,
             columns=['id', 'Percentage'],
             key_on='feature.id',
             fill_color='YlGnBu', fill_opacity=0.8, line_opacity=0.2,
             legend_name='Total Customer')
    map.save('templates/map.html')
    return render_template('map.html')

@app.route('/creator', methods=['POST','GET'])
def creator():
    df = pd.read_csv('income_evaluation.csv')
    df.columns = ['age','workclass','finalweight',
              'education','educationNumber','maritalStatus',
              'occupation','relationship','race',
              'sex','capitalGain','capitalLoss',
              'hoursperweek','nativeCountry','income']
    categorical = [i for i in df.columns.drop(['income']) if df[i].dtype == 'O']
    for i in categorical:
        df[i] = [col.replace(' ','') for col in df[i].values]
    df['occupation'] = df[['occupation','workclass']].apply(lambda x : 'None' if x['occupation'] == '?' and x['workclass']=='Never-worked' else x['occupation'],axis=1)
    listdrop = df[(df['occupation']=='?')&(df['workclass']=='?')].index
    df.drop(listdrop,axis=0,inplace=True)
    if request.method == 'POST':
        df = pd.read_csv('income_evaluation.csv')
        df.columns = ['age','workclass','finalweight',
              'education','educationNumber','maritalStatus',
              'occupation','relationship','race',
              'sex','capitalGain','capitalLoss',
              'hoursperweek','nativeCountry','income']
        categorical = [i for i in df.columns.drop(['income']) if df[i].dtype == 'O']
        for i in categorical:
            df[i] = [col.replace(' ','') for col in df[i].values]
        numerical = [i for i in df.columns.drop(['income','nativeCountry']) if df[i].dtype != 'O']
        df['occupation'] = df[['occupation','workclass']].apply(lambda x : 'None' if x['occupation'] == '?' and x['workclass']=='Never-worked' else x['occupation'],axis=1)
        listdrop = df[(df['occupation']=='?')&(df['workclass']=='?')].index
        df.drop(listdrop,axis=0,inplace=True)
        body = request.form
        used = db.cursor()
        age =  body['age']
        workclass = body['workclass']
        finalweight = body['weight']
        education = body['education']
        listEdu = list(df['education'].unique())
        listItem = []
        for i in listEdu:
            listItem.append([i,np.unique(df[df['education']==i]['educationNumber'].values)[0]])

        dfEdu = pd.DataFrame(listItem,columns=['education','educationNumber'])
        educationNumber = int(dfEdu[dfEdu['education'] == body['education']]['educationNumber'].values[0])
        gain = body['gain']
        loss = body['loss']
        hpw = body['hpw']
        country = body['country']
        marital = body['marital']
        occupation = body['occupation']
        relation = body['relation']
        race = body['race']
        sex = body['sex']
        email = body['email']
        qry1 = 'select * from login where email = %s'
        val1 = (email,)
        used.execute(qry1,val1)
        hasil = used.fetchall()
        cust = hasil[0][0]
        password = body['password']
        qry = 'insert into dataset (age,workclass,finalweight,education,educationNumber,maritalStatus,occupation,relationship,race,sex,capitalGain,capitalLoss,hoursperweek,nativeCountry) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        val = (age,workclass,finalweight,education,educationNumber,marital,occupation,relation,race,sex,gain,loss,hpw,country)
        used.execute(qry, val)
        db.commit()
        return render_template('success.html', email=email, password=password) #cost=cost)
    return render_template('creator.html',country=df['workclass'].unique())

@app.route('/signup', methods = ['POST'])
def signup():
    try:
        request.method == 'POST'
        # body = request.json
        body = request.form
        used = db.cursor()
        qry = 'insert into login (email, password) values(%s,%s)'
        val = (body['email'],body['password'])
        used.execute(qry, val)
        db.commit()
        return redirect('/')    
    except mysql.connector.Error:
        msg = 'Customer ID has been registered!'
        return render_template('reg.html', msg1=msg) 

@app.route('/login', methods=['POST'])
def login():
    df = pd.read_csv('income_evaluation.csv')
    df.columns = ['age','workclass','finalweight',
              'education','educationNumber','maritalStatus',
              'occupation','relationship','race',
              'sex','capitalGain','capitalLoss',
              'hoursperweek','nativeCountry','income']
    categorical = [i for i in df.columns.drop(['income']) if df[i].dtype == 'O']
    for i in categorical:
        df[i] = [col.replace(' ','') for col in df[i].values]
    df['occupation'] = df[['occupation','workclass']].apply(lambda x : 'None' if x['occupation'] == '?' and x['workclass']=='Never-worked' else x['occupation'],axis=1)
    listdrop = df[(df['occupation']=='?')&(df['workclass']=='?')].index
    df.drop(listdrop,axis=0,inplace=True)
    wc = df['workclass'].unique()
    marital = df['maritalStatus'].unique()
    occupation = df['occupation'].unique()
    print(occupation)
    relation = df['relationship'].unique()
    race = df['race'].unique()
    sex = df['sex'].unique()
    country = df['nativeCountry'].unique()
    education = df['education'].unique()
    if request.method == 'POST':
        body = request.form
        email = body['email']
        password = body['password']
        used = db.cursor()
        qry = 'select * from login where email = %s'
        val = (email,)
        used.execute(qry,val)
        hasil = used.fetchall()
        msg = 'Your Email Has Not Been Registered!'
        if hasil == []:
            return render_template('reg.html', msg2=msg)
        else:
            qry = 'select * from login where email = %s and password = %s'
            val = (body['email'],body['password'])
            used.execute(qry,val)
            hasil = used.fetchall()
            msg = 'Your password is wrong!'
            if hasil == [] :
                return render_template('reg.html', msg3= msg)
            else :
                return render_template('creator.html', email=email,password=password, wc=wc, marital=marital,occupation=occupation,relation=relation,race=race,sex=sex,country=country, education=education)

if (__name__) == '__main__':
    loadlemar()
    loadlenc()
    loadleoc()
    loadlerc()
    loadlerl()
    loadlesx()
    loadlewc()
    loadModel()
    loadScaler()
    app.run(
        debug=True,
        host='localhost',
        port=5000
        )

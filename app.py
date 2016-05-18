from flask import Flask, render_template, redirect, request
from datetime import datetime
import pandas as pd
import json


app = Flask(__name__)

formdata = pd.read_excel('Dane.xls', index_col=None, na_values=['-'])

labels=['Country', 'Happines', 'Salary', 'Rate', 'Cancer', 'Urbanisation']
labels_long=['Country', 'Happiness Level [%]', 'Disposable salary [100$]', 'Unemployment rate [%]', 'Heart disease deaths', 'Urbanisation [%]']
global nrofrows
nrofcoutries=len(formdata.Country)
nrofrows=nrofcoutries

@app.route("/")
def welcome():
    return render_template('welcome.html')


@app.route("/raw")
def show_raw():
    return render_template('raw.html', formdata=formdata.iloc[0:nrofrows, :].as_matrix())


@app.route("/save", methods=['POST'])
def save():
    global nrofrows
    # Get data from FORM

    action=request.form['action']
    if action=="all":
        nrofrows = nrofcoutries
    else:
        nrofrows = int(request.form['nrofrows'])
        if nrofrows > nrofcoutries or nrofrows < 1:
            nrofrows = nrofcoutries
    return redirect('/raw')

@app.route("/result")
def show_result():

    #Happiness level
    data = formdata.iloc[:, [0, 1]]
    lis=[]
    for val in data.iloc[:,1].values:
        if val>30:
            lis.append('green')
        elif val==14:
            lis.append('blue')
        else:
            lis.append('red')
    data.insert(2,'color',lis)
    data=data.values.tolist()


    #Disposable salary
    data2 = formdata.sort_values('Salary')
    data2 = data2.loc[:, ['Country', 'Salary']]
    lis=[]
    for val in data2.iloc[:,1].index:
        if val==8:
            lis.append('blue')
        else:
            lis.append('green')
    data2.insert(2,'color',lis)
    data2 = data2.values.tolist()

    #Unempolyment rate
    max = formdata.loc[:, labels[1:6]].max()
    min = formdata.loc[:, labels[1:6]].min()
    q1 = formdata.loc[:, labels[1:6]].quantile(q=0.25, axis=0)
    q2 = formdata.loc[:, labels[1:6]].quantile(q=0.75, axis=0)
    data3=[]

    data3.append([labels_long[1], min[0], q1[0], q2[0], max[0]])
    data3.append([labels_long[2], min[1]/100, q1[1]/100, q2[1]/100, max[1]/100])
    data3.append([labels_long[3], min[2], q1[2], q2[2], max[2]])
    data3.append([labels_long[4], min[3], q1[3], q2[3], max[3]])
    data3.append([labels_long[5], min[4], q1[4], q2[4], max[4]])

    #Scatter chart
    data4 = formdata.loc[:, ['Salary', 'Urbanisation']]
    data4 = data4.values.tolist()

    #Bubble chart
    data5 = formdata.loc[:,['Country', 'Happines', 'Rate', 'Cancer']]
    data5 = data5.values.tolist()


    #Show all
    return render_template('result.html', data=data, data2=data2, data3=data3, data4=data4, data5=data5)



if __name__ == "__main__":
    app.debug = True
    app.run()
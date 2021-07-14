
"""
Created on Wed Jul 14 12:54:47 2021

@author: Aviral Shukla
"""

from flask import Flask,render_template,request
import pandas as pd
import sqlite3 as sql
import os


      
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/data',methods=['GET','POST'])
def data():
    if request.method == 'POST':
        f=request.form['csvfile']
        global data
        data=[]
        
        data=pd.read_csv(f)
        
        global data_frontend
        data_frontend=data.head(10)
        
        return render_template('index.html',data=data_frontend.to_html(header=True,index=False))

@app.route('/query',methods=['GET','POST'])
def query():    
    if request.method == 'POST':
        os.remove("dataset.db")
        q=str(request.form['sql'])
        dataset=data
        conn = sql.connect('dataset.db')
        dataset.to_sql('dataset', conn)
        
        conn = sql.connect('dataset.db')
        dataset = pd.read_sql(q, conn)
        conn.close()
        
        return render_template('data.html',data=data_frontend.to_html(header=True,index=False),data_return=dataset.to_html(header=True,index=False))

        
                

if __name__=='__main__':
    app.run(debug=True)



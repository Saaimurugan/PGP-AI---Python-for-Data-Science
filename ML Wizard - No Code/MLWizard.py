#Web page
from flask import Flask, render_template, request, redirect
import os
#Modeling
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__, template_folder='templates')

app.config["IMAGE_UPLOADS"] = "C:/Users/saaim/Documents/GitHub/PGP-AI---Python-for-Data-Science/ML Wizard/uploads"
 
@app.route("/", methods=["GET", "POST"])

def upload():  
    return render_template("file_upload_form.html")  

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        #f.save(f.filename)  
        plt.figure(figsize=(14,9))
        f.save(os.path.join(app.config["IMAGE_UPLOADS"], f.filename))
        datasetCvdTs = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], f.filename))
    return render_template("success.html", name = datasetCvdTs, filename=f.filename)  

@app.route('/update', methods = ['GET'])  
def update():  
    if request.method == 'GET': 
        Task = request.args['Task']
        datasetCvdTs = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], request.args['filename']))
        
        if Task == "UpdateNull":
            ChangeNull = request.args['change']
            ColumnName = request.args['Column']
            if ChangeNull == "Remove abservations":
                datasetCvdTs = datasetCvdTs[datasetCvdTs[ColumnName].notna()]
                datasetCvdTs.to_csv(os.path.join(app.config["IMAGE_UPLOADS"], request.args['filename']), index=False)
            else:
                datasetCvdTs[ColumnName] = datasetCvdTs[ColumnName].fillna(ChangeNull)
                datasetCvdTs.to_csv(os.path.join(app.config["IMAGE_UPLOADS"], request.args['filename']), index=False)

        if Task == "UpdateHead":
            #datasetCvdTs = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], request.args['filename']))
            requestHeadstring = request.args['heads']
            requestHeadstring = requestHeadstring[:-1]
            requestHeadArray = requestHeadstring.split("|")
            print(requestHeadArray)
            if request.args['addheads'] == "1":
                datasetCvdTs = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], request.args['filename']), sep=',', header=None)
                datasetCvdTs.columns = requestHeadArray
                datasetCvdTs.to_csv(os.path.join(app.config["IMAGE_UPLOADS"], request.args['filename']), index=False)
            else:
                datasetCvdTs = pd.read_csv(os.path.join(app.config["IMAGE_UPLOADS"], request.args['filename']), sep=',')
                for i in range(len(datasetCvdTs.columns)):
                    tru = {datasetCvdTs.columns[i]: requestHeadArray[i]}
                    datasetCvdTs.rename(columns=tru, index=tru, inplace=True)
                    datasetCvdTs.to_csv(os.path.join(app.config["IMAGE_UPLOADS"], request.args['filename']), index=False)
    return render_template("success.html", name = datasetCvdTs, filename=request.args['filename']) 

    # def missing_zero_values_table(df):
    #     zero_val = (df == 0.00).astype(int).sum(axis=0)
    #     mis_val = df.isnull().sum()
    #     mis_val_percent = 100 * df.isnull().sum() / len(df)
    #     mz_table = pd.concat([zero_val, mis_val, mis_val_percent], axis=1)
    #     mz_table = mz_table.rename(
    #     columns = {0 : 'Zero Values', 1 : 'Missing Values', 2 : '% of Total Values'})
    #     mz_table['Total Zero Missing Values'] = mz_table['Zero Values'] + mz_table['Missing Values']
    #     mz_table['% Total Zero Missing Values'] = 100 * mz_table['Total Zero Missing Values'] / len(df)
    #     mz_table['Data Type'] = df.dtypes
    #     mz_table = mz_table[
    #         mz_table.iloc[:,1] != 0].sort_values(
    #     '% of Total Values', ascending=False).round(1)
    #     print ("Your selected dataframe has " + str(df.shape[1]) + " columns and " + str(df.shape[0]) + " Rows.\n"      
    #         "There are " + str(mz_table.shape[0]) +
    #             " columns that have missing values.")
    #     # mz_table.to_excel('D:/sampledata/missing_and_zero_values.xlsx', freeze_panes=(1,0), index = False)
    #     return mz_table

    #     #missing_zero_values_table(results)

if __name__ == '__main__':  
    app.run(debug = True)  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 10:26:12 2018

@author: Shivendra Kumar


Awesome exercises on machine learning
"""



import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from sklearn import tree



loan_data = pd.read_csv(
'/Users/sumogroup/shivendra/AnancondaProjects/classifLoan/LoanApplicationData.csv',
                           sep= ',')


print ("Dataset Lenght:: ", len(loan_data))
print ("Dataset Shape:: ", loan_data.shape)

print ("Dataset:: ")
loan_data.head()

X = loan_data.iloc[:, 0:4]
Y = loan_data.iloc[:,4]

#X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.01, random_state = 100)
X_train = X
y_train = Y

clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100,
                               max_depth=3, min_samples_leaf=1)
clf_gini.fit(X_train, y_train)



"""features = loan_data.columns[1:]

#My method to create visualization
#def visualize_tree(tree, feature_names):
   Create tree png using graphviz.

    Args
    ----
    tree -- scikit-learn DecsisionTree.
    feature_names -- list of feature names.
    
    with open("dt.dot", 'w') as f:
        export_graphviz(tree, out_file=f,
                        feature_names=feature_names)

    command = ["dot", "-Tpng", "dt.dot", "-o", "dt.png"]
    try:
        subprocess.check_call(command)
    except:
        exit("Could not run dot, ie graphviz, to "
             "produce visualization")
        """
        
        
#Draw the tree for visalization
        
#visualize_tree(clf_gini,features)
from sklearn.externals.six import StringIO 
from IPython.display import Image 

import pydotplus
dot_data = StringIO()
export_graphviz(clf_gini, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
Image(graph.create_png())

#visualize_tree



from sklearn.externals.six import StringIO 
from IPython.display import Image 
clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,
 max_depth=3, min_samples_leaf=3)
clf_entropy.fit(X_train, y_train)

import pydotplus
dot_data = StringIO()
export_graphviz(clf_entropy, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
Image(graph.create_png())


# Visualize our decision trees

	
clf_gini.predict([[1, 1, 1, 1]])

clf_gini.predict([[1, 0, 0, 1]])

y_pred=clf_entropy.predict(X)

print ("Accuracy is ", accuracy_score(Y,y_pred)*100)


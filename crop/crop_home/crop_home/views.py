from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from .models import Production
from .models import Recomendation
import os
from django.conf import settings
import time
import glob
from sklearn.utils import shuffle
from sklearn.datasets import make_classification
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import random

def home(request):
        #    call='this page is now dynamic'
        #    response='Thanks for reading this tutorial!'
        #    context={'call':call, 'response':response}
        #    return render(request, 'home.html', context)
    return render(request, 'home.html')

def get_prediction(request):
    crop_data= pd.read_csv(os.path.join(os.path.dirname(__file__), "crop_production.csv"))
    print(crop_data)
    # crop_data = Production.objects.all()
    # crop_data = pd.DataFrame(crop_data)
    # crop_data = pd.DataFrame(list(Production.objects.all().values()))
    # crop_data = crop_data.tail(crop_data.shape[0] -1)
    # crop_data['Production'] = crop_data['Production'].str.replace('\r', '', regex=True)
    # os.remove(file) for file in os.listdir('static/images/predict') if file.endswith('.png')

    # start from here
    files = glob.glob('static/images/predict/*.png')
    for i in files:
        os.remove(i)

    print(crop_data.columns)

    crop_data.describe()

    crop_data.isnull().sum()
    print(crop_data)

    crop_data = crop_data.dropna()
    print(crop_data)

    crop_data.isnull().values.any()

    crop_data.Division_Name.unique()

    # crop_data['Production'].astype(float)
    # crop_data['Area'].astype(float)
    # crop_data['Production'] = pd.to_numeric(crop_data['Production'],errors='coerce')
    # crop_data['Area'] = pd.to_numeric(crop_data['Area'],errors='coerce')

    crop_data['Yield'] = (crop_data['Production'] / crop_data['Area'])
    crop_data['Season'] = crop_data['Season'].str.strip()
    # max_yeild = crop_data['A'].idxmax()

    # crop_data = crop_data.loc[crop_data['District_Name'] == request.GET['district']]
    print(request.GET['district'])
    print(request.GET['season'])

    max_yeild = crop_data.loc[(crop_data['District_Name'] == request.GET['district']) & (crop_data['Season'] == request.GET['season'])]
    # max_yeild = crop_data.loc[crop_data['District_Name'] == request.GET['district'] and crop_data['Season'] == request.GET['season']]
    # max_yeild.reset_index(drop=True)
    if max_yeild.empty:
        if request.GET['season'] == 'Whole Year':
            max_yeild = 'Paddy'
        elif request.GET['season'] == 'Rabi':
            max_yeild = 'Wheat'
        elif request.GET['season'] == 'Autumn':
            max_yeild = 'Brinjal'
        elif request.GET['season'] == 'Kharif':
            max_yeild = 'Jute'
        elif request.GET['season'] == 'Winter':
            max_yeild = 'Tomato'
        elif request.GET['season'] == 'Summer':
            max_yeild = 'Boro'
        elif request.GET['season'] == 'Spring':
            max_yeild = 'Pumpkin'
        else:
            max_yeild = 'Boro'
    else:
        max_yeild.index = np.arange(1, len(max_yeild) + 1)
        print(f'crop_data according to district : {max_yeild}')
        max_yeild = max_yeild.iloc[max_yeild['Yield'].idxmax()]
        max_yeild = max_yeild['Crop']
    print(f'Max Yield: {max_yeild}')


    crop_data.head(10)

    # ax = sns.pairplot(crop_data)
    # # print(ax)

    data = crop_data.drop(['Division_Name'], axis = 1)


    data.corr()

    sns.heatmap(data.corr(), annot =True)
    plt.title('Correlation Matrix')

    dummy = pd.get_dummies(data)
    print(dummy)


    x = dummy.drop(["Production","Yield"], axis=1)
    y = dummy["Production"]

    # # Splitting data set - 25% test dataset and 75%

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25, random_state=5)

    print("x_train :",x_train.shape)
    print("x_test :",x_test.shape)
    print("y_train :",y_train.shape)
    print("y_test :",y_test.shape)

    # x_train.replace(np.nan, 0)
    # y_train.replace(np.nan, 0)
    x_train = x_train.dropna()
    y_train = y_train.dropna()
    print(f'x_train : {x_train}')
    print(f'y_train : {y_train}')
    # print(f'y_train cols: {y_train.columns}')
    print(f'y_train : {type(y_train)}')

    model = LinearRegression()
    model.fit(x_train,y_train)



    lr_predict = model.predict(x_test)
    print(lr_predict)


    model.score(x_test,y_test)

    r = r2_score(y_test,lr_predict)
    print("R2 score : ",r)

    plt.scatter(y_test,lr_predict)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Linear Regression')
    # plt.savefig("D:\xampp\htdocs\crop\crop_yield\crop\crop_home\static\images\predict\my_plot.png")
    # plt.savefig("squares.png")
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/predict/linear_reg.png'))
    # plt.show()

    time.sleep(2)
    model = RandomForestRegressor(n_estimators = 11)
    model.fit(x_train,y_train)
    rf_predict = model.predict(x_test)
    print(rf_predict)

    model.score(x_test,y_test)

    r1 = r2_score(y_test,rf_predict)
    print("R2 score : ",r1)

    Adjr2_1 = 1 - (1-r)*(len(y_test)-1)/(len(y_test)-x_test.shape[1]-1)
    print("Adj. R-Squared : {}".format(Adjr2_1))


    ax = sns.distplot(y_test, hist = False, color = "r", label = "Actual value ")
    sns.distplot(rf_predict, hist = False, color = "b", label = "Predicted Values", ax = ax)
    plt.title('Random Forest Regression')

    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.fit_transform(x_test)

    print(x_train)
    print(x_test)

    # regressor = SVR(kernel = 'rbf')
    # regressor.fit(x_train,y_train)

    # svr_predict = regressor.predict(x_test)
    # print(svr_predict)

    # ax = sns.distplot(y_test, hist = False, color = "r", label = "Actual value ")
    # sns.distplot(svr_predict, hist = False, color = "b", label = "Predicted Values", ax = ax)
    # plt.title('Support Vector Regression')


    regressor = DecisionTreeRegressor(random_state = 5)
    regressor.fit(x_train,y_train)

    # Predicting results
    decisiontree_predict = regressor.predict(x_test)
    print(decisiontree_predict)

    regressor.score(x_test,y_test)


    r2 = r2_score(y_test,decisiontree_predict)
    print("R2 score : ",r2)


    Adjr2_2 = 1 - (1-r)*(len(y_test)-1)/(len(y_test)-x_test.shape[1]-1)
    print("Adj. R-Squared : {}".format(Adjr2_2))


    ax = sns.distplot(y_test, hist = False, color = "r", label = "Actual value ")
    sns.distplot(decisiontree_predict, hist = False, color = "b", label = "Predicted Values", ax = ax)
    plt.title('Decision Tree Regression')


    accuracies = cross_val_score(estimator = model, X = x_train, y=y_train, cv = 10)


    a1 = (accuracies.mean()*100)
    b1 = (accuracies.std()*100)

    acc1 = "{:.2f}".format (accuracies.mean()*100)
    std1 = "{:.2f}".format(accuracies.std()*100)

    print(f"Accuracy of random forest: {acc1} %")
    print(f"Standard Deviation  of random forest: {std1} %")


    accuracies = cross_val_score(estimator = regressor, X = x_train, y=y_train)

    a2 = (accuracies.mean()*100)
    b2 = (accuracies.std()*100)

    acc2 = "{:.2f}".format (accuracies.mean()*100)
    std2 = "{:.2f}".format(accuracies.std()*100)

    print(f"Accuracy of decission tree: {acc2} %")
    print(f"Standard Deviation of decission tree: {std2} %")

    Algorithms = ['Random Forest', 'Decision-tree']
    Accuracy = [a1, a2]

    x_pos = np.arange(len(Accuracy))
    plt.bar(x_pos, Accuracy, color=['#488AC7','#ff8c00'])


    plt.xticks(x_pos, Algorithms)
    plt.ylabel('Accuracy(in %)')
    plt.xlabel('Machine Learning Regression Techniques')

    # # Show graph
    # plt.show()
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/predict/ml_regression.png'))


    # Algorithms = ['Random Forest', 'Decision-tree']
    # Accuracy = [b1, b2]

    # x_pos = np.arange(len(Accuracy))

    # plt.bar(x_pos, Accuracy, color=['#488AC7','#ff8c00'])

    # plt.xticks(x_pos, Algorithms)
    # plt.ylabel('Standard Deviation(in %)')
    # plt.xlabel('Machine Learning Regression Techniques')

    # # Show graph
    # # plt.show()
    # plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/predict/ml_regression_2.png'))
    # # plt.savefig('SD.png')


    # Algorithms = ['Random Forest', 'Decision-tree']
    # Accuracy = [Adjr2_1, Adjr2_2]

    # x_pos = np.arange(len(Accuracy))

    # plt.bar(x_pos, Accuracy, color=['#488AC7','#ff8c00'])

    # plt.xticks(x_pos, Algorithms)
    # plt.ylabel('Standard Deviation(in %)')
    # plt.xlabel('Machine Learning Regression Techniques')

    # # plt.show()
    # # plt.savefig('SD.png')
    # plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/predict/ml_regression_3.png'))




    # Algorithms = ['Random Forest', 'Decision-tree']
    # Accuracy = [r1, r2]

    # x_pos = np.arange(len(Accuracy))

    # # Create bars with different colors
    # plt.bar(x_pos, Accuracy, color=['#488AC7','#ff8c00'])

    # # Create names on the x-axis
    # plt.xticks(x_pos, Algorithms)
    # plt.ylabel('R-Squared Score')
    # plt.xlabel('Machine Learning Regression Techniques')

    # # Show graph
    # # plt.show()
    # # plt.savefig('SD.png')

    # plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/predict/ml_regression_4.png'))




    # # create a dataset
    # Algorithms = ['Random Forest', 'Decision-tree']
    # Accuracy = [Adjr2_1, Adjr2_2]

    # x_pos = np.arange(len(Accuracy))

    # # Create bars with different colors
    # plt.bar(x_pos, Accuracy, color=['#488AC7','#ff8c00'])

    # # Create names on the x-axis
    # plt.xticks(x_pos, Algorithms)
    # plt.ylabel('Adjusted R-Squared Score')
    # plt.xlabel('Machine Learning Regression Techniques')

    # # Show graph
    # # plt.show()
    # # plt.savefig('SD.png')
    # plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/predict/ml_regression_4.png'))



    print('Mean Absolute Error:', metrics.mean_absolute_error(rf_predict,y_test))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, rf_predict))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, rf_predict)))



    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(8, 5))

    # set height of bar
    Algorithms = ['Random Forest', 'Decision-tree']
    Accuracy = [a1, a2]
    Standard_Deviation = [b1,b2]

    # Set position of bar on X axis
    br1 = np.arange(len(Accuracy))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    # Make the plot
    plt.bar(br1, Accuracy, color ='blue', width = barWidth,
            edgecolor ='grey', label ='Accuracy')
    plt.bar(br2, Standard_Deviation, color ='maroon', width = barWidth,
            edgecolor ='grey', label ='Standard Devation')

    # Adding Xticks
    plt.xlabel('Algorithms', fontweight ='bold', fontsize = 10)
    plt.ylabel('Accuracy (in %)', fontweight ='bold', fontsize = 10)
    plt.xticks([r + barWidth for r in range(len(Accuracy))],
            Algorithms)

    # plt.legend()
    # plt.show()
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/predict/ml_regression_4.png'))
    npk = getNPK(request.GET, max_yeild)
    data = {
        'payload' : request.GET,
        'status' : 'success',
        'prediction' : acc1,
        'suggestion' : max_yeild,
        'N' : str(npk[0]),
        'P' : str(npk[1]),
        'K' : str(npk[2]),
    }
    # End here
    # max_yeild = 'Boro'
    # npk = getNPK(request.GET, max_yeild)

    # print(f'npk : {npk}')
    # data = {
    #     'payload' : request.GET,
    #     'status' : 'success',
    #     'prediction' : '80',
    #     'suggestion' : 'rice',
    #     'N' : str(npk[0]),
    #     'P' : str(npk[1]),
    #     'K' : str(npk[2]),
    # }
    return JsonResponse(data)

def getNPK(data, max_yeild):

    print(data['season'])
    temp = 26
    if data['season'] == 'Whole Year':
        temp = 26
    elif data['season'] == 'Rabi':
        temp = 19
    elif data['season'] == 'Autumn':
        temp = 30
    elif data['season'] == 'Kharif':
        temp = 27
    elif data['season'] == 'Winter':
        temp = 15
    elif data['season'] == 'Summer':
        temp = 32
    elif data['season'] == 'Spring':
        temp = 20
    else:
        temp = 26
    print(f'temp : {temp}')
    res = []


    crop_rec_init = pd.read_csv(os.path.join(os.path.dirname(__file__), "Crop_recommendation.csv"))

    crop_rec_init.describe()
    crop_rec_init.isnull().sum()
    crop_rec_init = crop_rec_init.dropna()
    crop_rec_init.isnull().values.any()
    print(crop_rec_init)

    crop_rec = crop_rec_init.loc[(crop_rec_init['label'] == max_yeild)]
    # print(crop_rec.isnull())
    if crop_rec.empty:
        res.append(random.randrange(50, 80, 2))
        res.append(random.randrange(40, 60, 2))
        res.append(random.randrange(20, 40, 2))
    else:
        crop_rec['rec'] = abs(crop_rec['temperature'] - temp)
        print(crop_rec)
        crop_rec = crop_rec[crop_rec.rec == crop_rec.rec.min()]
        crop_rec.reset_index(drop=True, inplace=True)
        print(crop_rec)
        N = crop_rec.iloc[0]['N']
        P = crop_rec.iloc[0]['P']
        K = crop_rec.iloc[0]['K']
        res.append(N)
        res.append(P)
        res.append(K)

    # makeRecomendGraph(crop_rec_init)

    return res

def makeRecomendGraph(crop_data):
    print('makeRecomendGraph')
    files = glob.glob('static/images/recomend/*.png')
    for i in files:
        os.remove(i)

    crop_data.rename(columns = {'label':'Crop'}, inplace = True)
    print(crop_data)
    crop_data.describe()
    crop_data.isnull().sum()
    crop_data = crop_data.dropna()
    print(crop_data)
    crop_data.isnull().values.any()
    crop_data.Crop.unique()
    n = 5
    crop_data['Crop'].value_counts()[:5].index.tolist()

    sns.barplot(crop_data["Crop"], crop_data["temperature"])
    plt.xticks(rotation = 90)
    # plt.show()
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/recomend/temperature.png'))


    sns.barplot(crop_data["Crop"], crop_data["ph"])
    plt.xticks(rotation = 90)
    # plt.show()
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/recomend/ph.png'))

    sns.barplot(crop_data["Crop"], crop_data["humidity"])
    plt.xticks(rotation = 90)
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/recomend/humidity.png'))

    sns.barplot(crop_data["Crop"], crop_data["rainfall"])
    plt.xticks(rotation = 90)
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/recomend/rainfall.png'))

    crop_data.corr()
    sns.heatmap(crop_data.corr(), annot =True)
    plt.title('Correlation Matrix')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/recomend/correlation.png'))

    df  = shuffle(crop_data,random_state=5)
    df.head()
    x = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
    target = df['Crop']
    y = pd.get_dummies(target)
    print(y)
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25, random_state= 0)

    print("x_train :",x_train.shape)
    print("x_test :",x_test.shape)
    print("y_train :",y_train.shape)
    print("y_test :",y_test.shape)


    print('Random Forest Classifier starts')
    forest = RandomForestClassifier(random_state=1)
    multi_target_forest = MultiOutputClassifier(forest, n_jobs=-1)
    multi_target_forest.fit(x_train, y_train)
    forest_pred = multi_target_forest.predict(x_test)

    a1 = accuracy_score(y_test, forest_pred)
    print('Accuracy score:', accuracy_score(y_test, forest_pred))
    score = cross_val_score(multi_target_forest,X = x_train, y = y_train,cv=5)
    b1 = "{:.2f}".format(score.mean()*100)
    b1 = float(b1)
    c1 = (score.std()*100)
    print("Accuracy : {:.2f}%".format (score.mean()*100))
    print("Standard Deviation : {:.2f}%".format(score.std()*100))

    print('Decision Tree Classifier starts')
    clf = DecisionTreeClassifier(random_state=6)
    multi_target_decision = MultiOutputClassifier(clf, n_jobs=-1)
    multi_target_decision.fit(x_train, y_train)

    decision_pred = multi_target_decision.predict(x_test)

    print(f"decision_pred : {decision_pred}")

    a2 = accuracy_score(y_test,decision_pred)
    print(f'Accuracy score : {a2}')

    score = cross_val_score(multi_target_decision,X = x_train, y = y_train,cv=7)

    b2 = "{:.2f}".format(score.mean()*100)
    b2 = float(b2)
    print(f'cross_val_score : {b2}')

    c2 = (score.std()*100)
    print(f'std : {c2}')

    print('KNN classifier starts')
    knn_clf=KNeighborsClassifier()
    model = MultiOutputClassifier(knn_clf, n_jobs=-1)
    model.fit(x_train, y_train)

    knn_pred = model.predict(x_test)
    print(f"knn_pred : {knn_pred}")

    a3 = accuracy_score(y_test,knn_pred)
    print(f'Accuracy score: {a3}')

    score = cross_val_score(model,X = x_train, y = y_train,cv=7)
    print(f'cross_val_score : {score}')

    b3 = "{:.2f}".format(score.mean()*100)
    b3 = float(b3)
    print(f'cross_val_score : {b3}')
    c3 = (score.std()*100)

    data = {'Algorithms':['Random Forest', 'Decision-tree', 'KNN Classifier'],
        'Accuracy':[b1, b2, b3],
        'Standard Deviation':[c1,c2,c3]}

    # Creates pandas DataFrame.
    print('creating graph for showing 3 algorithms accuracy')
    df = pd.DataFrame(data)

    Algorithms = ['Random Forest', 'Decision-tree','KNN Classifier']
    Accuracy = [b1, b2, b3]

    x_pos = np.arange(len(Accuracy))

    # Create bars with different colors
    plt.bar(x_pos, Accuracy, color=['#488AC7','#ff8c00','#009150'])

    # Create names on the x-axis
    plt.xticks(x_pos, Algorithms)
    plt.ylabel('Accuracy(in %)')
    plt.xlabel('Machine Learning Classifying Techniques')

    # plt.show()
    plt.savefig(os.path.join(settings.BASE_DIR, 'static/images/recomend/accuracy.png'))

    return True





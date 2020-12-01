import pandas as pd
import numpy as np
import sklearn.svm as svm
import sklearn.decomposition as dec

def cabin_parse(cabin):
    if str(cabin) == 'nan' : return 0
    # C23 C25 C27 --> ['C23', 'C25', 'C27'] [0] --> 'C23'
    c = cabin.split()[0]
    # ord(char) --> kod asci
    ic = (1+ord(c[0])-ord('A'))*1000
    if len(c)>1 :
        ic += int(c[1:])
    return ic

def age_parse(age):
    if str(age) == 'nan': return 0
    return age

def normalize(s):
    return s/s.max()

def svm_test(X_train, Y_train, X_test, Y_test):
    model = svm.SVC(kernel='linear')
    print("Fitting ....")
    model.fit(X_train, Y_train)
    print("Fitted to data")
    Y_pred = model.predict(X_test)
    score = 0
    for i in range(len(Y)):
        if Y_test[i] == Y_pred[i]: score += 1
    print('score', score / len(Y_test))

dataset = pd.read_csv("../Titanic_train.csv")

print(dataset)



dataset['Embarked'] = pd.Categorical(dataset['Embarked'])
dataset['Embarked'] = dataset.Embarked.cat.codes

dataset['Sex'] = pd.Categorical(dataset['Sex'])
dataset['Sex'] = dataset.Sex.cat.codes

dataset['Cabin'] = dataset.Cabin.apply(cabin_parse)
dataset['Age'] = dataset.Age.apply(age_parse)


columns = list(dataset.columns[2:])
columns.remove('Name')
columns.remove('Ticket')


X = dataset[columns].values
Y = dataset['Survived'].values
X_train = X
X_test =X
Y_train =Y
Y_test = Y

print("SVM on pure data")
svm_test(X_train, Y_train, X_test, Y_test)

print("------------------")
print("SVM on data after pca without reduction")
pca = dec.PCA(n_components=len(columns))
pca.fit(X)
X_pca = pca.transform(X_train)
print(pca.explained_variance_ratio_)
X_pca_test = pca.transform(X_test)
svm_test(X_pca, Y_train, X_pca_test, Y_test)

print("------------------")
print("SVM on data after pca with reduction of 1 component")
pca = dec.PCA(n_components=len(columns)-1)
pca.fit(X)
X_pca = pca.transform(X)
print("explained ratio:")
X_pca_test = pca.transform(X_test)
print(pca.explained_variance_ratio_)
svm_test(X_pca, Y_train, X_pca_test, Y_test)



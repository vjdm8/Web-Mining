"""
A simple script that demonstrates how we can use grid search to set the parameters of a classifier
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

#read the reviews and their polarities from a given file
def loadData(fname):
    reviews=[]
    labels=[]
    f=open(fname)
    for line in f:
        review,rating=line.strip().split('\t')  
        reviews.append(review.lower())    
        labels.append(rating)
    f.close()
    return reviews,labels

rev_train,labels_train=loadData('reviews_train.txt')
rev_test,labels_test=loadData('reviews_test.txt')

#Build a counter based on the training dataset
counter = CountVectorizer(stop_words=stopwords.words('english'))
counter.fit(rev_train)

#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(rev_train)#transform the training data
counts_test = counter.transform(rev_test)#transform the testing data

#KNN=KNeighborsClassifier()
#KNN.fit(counts_train,labels_train)


model = LogisticRegression(penalty='l2', C=0.1)
model.fit(counts_train,labels_train)

#use the classifier to predict
predicted=model.predict(counts_test)

#print the accuracy
print accuracy_score(predicted,labels_test)

def loadData1(fname):
    reviews=[]
    f=open(fname)
    for line in f:
        review=line.strip()
        reviews.append(review.lower())    
    f.close()
    return reviews


rev_test1=loadData1('test.txt')
    
counts_test1 = counter.transform(rev_test1)

predicted1=model.predict(counts_test1)

fw=open('out.txt','w')
for item in predicted1:
    fw.write(item+'\n')
fw.close()

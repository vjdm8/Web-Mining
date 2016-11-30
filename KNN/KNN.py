# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 20:54:01 2016

@author: Vivek
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
os.chdir("\KNN")

from operator import itemgetter
import numpy as np
from collections import Counter

#to load data and extract and store ratings and reviews 
def loadData(fname):
    reviews=[]
    labels=[]
    f=open(fname)
    for line in f:
        review,rating=line.strip().split('\t')
        reviews.append(review.lower())
        labels.append(int(rating))
    f.close()
    return reviews,labels

#to load lexicons
def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close()

    return newLex

#function to obtain distance
# given two reviews, calculate similarity measure
# return distance (same text yields d = 0)
def get_distance(review1, review2):
    postrain=set(review1.split(' '))& posLex
    negtrain=set(review1.split(' '))& negLex

    postest=set(review2.split(' '))& posLex
    negtest=set(review2.split(' '))& negLex

    d1 = abs(len(postest) - len(postrain))
    d2 = abs(len(negtest) - len(negtrain))

    d = (d1+d2)
    return d

#------------------------------------------------------------------------------
"""
# euclidian distance
def get_distance(review1, review2):
    postrain=set(review1.split(' '))& posLex
    negtrain=set(review1.split(' '))& negLex

    postest=set(review2.split(' '))& posLex
    negtest=set(review2.split(' '))& negLex

    d1 = (len(postest) - (len(postrain)))**2
    d2 = (len(negtest) - (len(negtrain)))**2

    d = (d1+d2)**0.5
    return d
"""
#------------------------------------------------------------------------------
"""
# cosine distance (divide by zero errors | even worse if you add 1)
def get_distance(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    postrain=set(v1.split(' '))& posLex
    negtrain=set(v1.split(' '))& negLex

    postest=set(v2.split(' '))& posLex
    negtest=set(v2.split(' '))& negLex

    sumxx = (len(postest)+1)**2+(len(postrain)+1)**2
    sumyy = (len(postest)+1)**2+(len(postrain)+1)**2
    sumxy = ((len(postest)+1)*(len(negtest)+1))+((len(postrain)+1)*(len(negtrain)+1))
    return sumxy/((sumxx*sumyy)**0.5)
"""

#------------------------------------------------------------------------------
# 2) given a training set and a test instance, use getDistance to calculate all pairwise distances
def get_neighbours(training_set, test_instance, k):
    distances = [_get_tuple_distance(training_instance, test_instance) for training_instance in training_set]
    # index 1 is the calculated distance between training_instance and test_instance
    sorted_distances = sorted(distances, key=itemgetter(1))
    # extract only training instances
    sorted_training_instances = [tuple[0] for tuple in sorted_distances]
    # select first k elements
    return sorted_training_instances[:k]

def _get_tuple_distance(training_instance, test_instance):
    return (training_instance, get_distance(test_instance, training_instance[0]))

# 3) given an array of nearest neighbours for a test case, tally up their classes to vote on test case class
def get_majority_vote(neighbours):
    # index 1 is the class
    classes = [neighbour[1] for neighbour in neighbours]
    count = Counter(classes)
    return count.most_common()[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
                if testSet[x][1] == predictions[x]:
                        correct += 1

    accuracy = correct/float(len(testSet))*100.0
    return accuracy


# setting up main executable method
def main():

    global posLex
    global negLex

    posLex=loadLexicon('positive-words.txt')
    negLex=loadLexicon('negative-words.txt')

    # prepare data
    train_data = 'reviews_train.txt'
    test_data = 'reviews_test.txt'
    rev_train,labels_train = loadData(train_data)
    rev_test, labels_test = loadData(test_data)


    print 'Training set reviews: ' + repr(len(rev_train))
    print 'Test set reviews: ' + repr(len(rev_test))

    print 'Training set labels: ' + repr(len(labels_train))
    print 'Test set labels: ' + repr(len(labels_test))


    # reformat train/test datasets for convenience
    train = np.array(zip(rev_train, labels_train))
    test = np.array(zip(rev_test, labels_test))

    # generate predictions
    predictions = []

    # let's arbitrarily set k equal to 5, meaning that to predict the class of new instances,
    knn = 5

    for k in range(knn+1):
        # for each instance in the test set, get nearest neighbours and majority vote on predicted class
        for x in range(len(rev_test)):


            #print 'Classifying test instance number ' + str(x) + ":",
            neighbours = get_neighbours(training_set=train, test_instance=test[x][0], k=5)
            majority_vote = get_majority_vote(neighbours)
            predictions.append(majority_vote)
            #print 'Predicted label=' + str(majority_vote) + ', Actual label=' + str(test[x][1])


        accuracy = getAccuracy(test, predictions)
        print
        print('Accuracy@ K=' + repr(k) + " " + repr(accuracy) + '%')
        print
        print

if __name__ == "__main__":
    main()

import os
import sys

import numpy as np
import pandas as pd
import pydotplus
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, ShuffleSplit, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

Saving_PATH = r'C:\Users\haora\Desktop\invest\byd_tree_clf_fina_indicator_'
Lib_PATH = r'C:\Users\haora\PycharmProjects\pythonProject\venv\Lib'




def get_importance_dict(feature_names, importance_score):
    if len(importance_score) != len(feature_names):
        sys.stderr.write("Error: importance_score length not fit feature_names!")
        return

    importance_dict = {'feature': feature_names, 'importance': importance_score}
    return pd.DataFrame.from_dict(importance_dict)


def get_precision_score(Y_predict, Y_test):
    if len(Y_predict) != len(Y_test):
        sys.stderr.write("Error: importance_score length not fit feature_names!")
        return False
    count_cor = 0
    for i in range(len(Y_predict)):
        if Y_predict[i] == Y_test[i]:
            count_cor += 1
    return round(count_cor/len(Y_test), 2)

'''
return both cleaned and origin data
'''
def clean_data(X):
    imputer = SimpleImputer(missing_values=np.NaN, strategy='median')
    X_cleaned = imputer.fit_transform(X)
    return X_cleaned, X


def decison_tree_clf(X, Y, tree_name):
    X_data, X = clean_data(X)
    X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y, test_size=0.3, random_state=1)
    clf = DecisionTreeClassifier(max_depth=5)
    clf = clf.fit(X_train, Y_train)

    # graph tree
    with open(Saving_PATH + r'byd_tree_clf_fina_indicator.dot', 'w') as f:
        f = tree.export_graphviz(clf, out_file=f)

    dot_data = tree.export_graphviz(clf, out_file=None,
                                    feature_names=X.columns,
                                    class_names=['decrease', 'increase'],
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)
    os.environ["PATH"] += os.pathsep + Lib_PATH + r'/site-packages\graphviz\bin'
    graph.write_pdf(Saving_PATH + str(tree_name) + '.pdf')
    # view feature importance
    importance_list = clf.feature_importances_
    importance_df = get_importance_dict(X.columns, importance_list)
    importance_df.sort_values(['importance'], ascending=False, inplace=True)

    # predict
    Y_predict = clf.predict(X_test)
    precision_score = get_precision_score(Y_predict, Y_test)
    sys.stdout.write('tree_score - MODEL: %s, SCORE: %s\n' % (tree_name, precision_score))


def cv(X, Y, model_name):
    X_data, X = clean_data(X)
    clf = DecisionTreeClassifier(max_depth=4)
    cv = ShuffleSplit(n_splits=10, test_size=.3, random_state=0)
    scores = cross_val_score(clf, X_data, Y, cv=cv)
    sys.stdout.write("MODEL: %s, MED_SCORE: %s, SV_SCORES: %s\n" % (model_name, np.median(scores), scores))


def cv_grid_search(X, Y, model_name):
    X_data, X = clean_data(X)
    best_score = 0
    best_scores_list = []
    best_depth = 10

    for max_depth in range(2, 10):
        clf = DecisionTreeClassifier(max_depth=max_depth)
        cv = ShuffleSplit(n_splits=10, test_size=.3, random_state=0)
        scores = cross_val_score(clf, X_data, Y, cv=cv)
        sys.stdout.write("MODEL: %s, MED_SCORE: %s, MIN: %s, MAX: %s, STD: %s\n" %
                         (model_name+'_'+str(max_depth), np.median(scores), np.min(scores), np.max(scores), round(np.std(scores), 4)))
        if np.median(scores) > best_score:
            best_depth = max_depth
            best_score = np.median(scores)
            best_scores_list = scores

    sys.stdout.write(
        "--BEST_MODEL: %s, MED_SCORE: %s, SV_SCORES: %s\n" % (model_name + '_' + str(best_depth), best_score, best_scores_list))

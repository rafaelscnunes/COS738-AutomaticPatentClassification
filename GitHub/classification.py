
# coding: utf-8

# # Automatic Patent Classification

def main():
    import os
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    plt.style.use("classic")
    sns.set()

    from time import time
    ## Pre-processing...
    ### Importing data into pandas.DataFrame
    # LOAD DATA DIRECTLY FROM .CSV INTO PYTHON_LIST()
    t0 = time()
    print('Importing data...')
    try:
        dataset = open('dataset_ipc_first.csv', 'r', encoding='latin-1')
    except:
        dataset = open('./output/dataset_ipc_first.csv', 'r', encoding='latin-1')
    else:
        pass
    if dataset:
        X_title, X_resume, y = [], [], []
        header = dataset.readline()
        if header[:-1] == 'title|resume|ipc':
            for line in dataset:
                line = line[:-1].split('|')
                if line[2][0:1] in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                    X_title.append(line[0])  # title
                    X_resume.append(line[1]) # resume
                    y.append(line[2][0:1])   # only first level IPC class (A..H)
        print('Number of occurences on X_title: ', len(X_title))
        print('Number of occurences on X_resume: ', len(X_resume))
        print('Number of occurences on y: ', len(y))
        categories = pd.DataFrame(y, columns = ['ipc_level1'])
    print('done in %0.3fs.' % (time() - t0))


    ## Analyzing data
    ### first look on data
    # plt.figure(figsize=(12,6))
    # ax = sns.countplot(x="ipc_level1", data=categories)
    # plt.ylabel('Patent requests', fontsize=12)
    # plt.xlabel('First level IPC', fontsize=12)
    # plt.xticks(rotation='horizontal')
    # plt.show()
    # print('Total count of patent requests: ', len(categories))


    ## Extracting features...
    ### Vectorization
    from time import time
    from sklearn.feature_extraction.text import CountVectorizer
    t0 = time()
    print('Extracting features...')
    vec = CountVectorizer(ngram_range = (1, 1), max_df = .95, min_df = 1)
    X_title_features = vec.fit_transform(X_title)
    print('Title vector matrix shape: ', X_title_features.shape)
    X_resume_features = vec.fit_transform(X_resume)
    print('Resume vector matrix shape: ', X_resume_features.shape)
    print('done in %0.3fs.' % (time() - t0))


    ### Reducing deminsionality with SVD
    from sklearn.decomposition import TruncatedSVD
    t0 = time()
    print('Selecting most relevant features...')
    svd = TruncatedSVD(n_components = 200)
    X_title_svd = svd.fit_transform(X_title_features)
    print('Title most relevant features matrix shape: ', X_title_svd.shape)
    svd = TruncatedSVD(n_components = 800)
    X_resume_svd = svd.fit_transform(X_resume_features)
    print('Resume most relevant features matrix shape: ', X_resume_svd.shape)
    print('done in %0.3fs.' % (time() - t0))


    ### Encoding each category into one exclusive integer
    from sklearn.preprocessing import LabelEncoder
    t0 = time()
    print('Encoding labels...')
    l_enc = LabelEncoder()
    y_encoded = l_enc.fit_transform(y)
    print('Encoded classes: ', l_enc.classes_)
    print('done in %0.3fs.' % (time() - t0))


    ## Sampling...
    from sklearn.model_selection import train_test_split
    t0 = time()
    print('Creating sampling...')
    X_concatenated = np.concatenate((X_title_svd, X_resume_svd), axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(X_concatenated,
                                                        y_encoded,
                                                        test_size = 0.2,
                                                        random_state = 583)
    print('X_train matrix shape: ', X_train.shape)
    print('X_test matrix shape: ', X_test.shape)
    print('y_train matrix shape: ', y_train.shape)
    print('y_test matrix shape: ', y_test.shape)
    print('done in %0.3fs.' % (time() - t0))


    ## Training...
    import itertools
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import accuracy_score

    def plot_confusion_matrix(cm, classes,
                              normalize = False,
                              title = 'Confusion matrix',
                              cmap = plt.cm.Blues):
        plt.imshow(cm, interpolation='nearest', cmap = cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation = 45)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment = "center",
                     color = "white" if cm[i, j] > thresh else "black")
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')


    ### Naïve Bayes - Gaussian
    from sklearn.naive_bayes import GaussianNB
    from sklearn.model_selection import cross_val_predict
    t0 = time()
    print('Training and predicting classes using Naïve Bayes (Gaussian)...')
    classifier = GaussianNB()
    y_pred = classifier.fit(X_train, y_train).predict(X_test)
    # y_pred = cross_val_predict(classifier, X_concatenated, y_encoded,
    #                            cv = 3, n_jobs = -1, verbose = 1)
    print('done in %0.3fs.' % (time() - t0))
    # Printing accuracy
    acc = accuracy_score(y_test, y_pred)
    print('Accuracy: ', str(acc))
    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    # np.set_printoptions(precision=2)
    # class_names = ['A','B','C','D','E','F','G','H']
    # plt.figure(figsize=(12,6))
    # plot_confusion_matrix(cm, classes=class_names, title='Confusion matrix')
    # plt.show()


    ### Naïve Bayes - Bernoulli
    from sklearn.naive_bayes import BernoulliNB
    t0 = time()
    print('Training and predicting classes using Naïve Bayes (Bernoulli)...')
    classifier = BernoulliNB()
    y_pred = classifier.fit(X_train, y_train).predict(X_test)
    print('done in %0.3fs.' % (time() - t0))
    # Printing accuracy
    acc = accuracy_score(y_test, y_pred)
    print('Accuracy: ', str(acc))
    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    # np.set_printoptions(precision=2)
    # class_names = ['A','B','C','D','E','F','G','H']
    # plt.figure(figsize=(12,6))
    # plot_confusion_matrix(cm, classes=class_names, title='Confusion matrix')
    # plt.show()


    ### Random Forest Classifier
    from sklearn.ensemble import RandomForestClassifier
    t0 = time()
    print('Training and predicting classes using Random Forest Classifier...')
    classifier = RandomForestClassifier(n_estimators = 100,
                                        criterion = 'entropy', n_jobs = -1,
                                        verbose = 1)
    y_pred = classifier.fit(X_train, y_train).predict(X_test)
    print('done in %0.3fs.' % (time() - t0))
    # Printing accuracy
    acc = accuracy_score(y_test, y_pred)
    print('Accuracy: ', str(acc))
    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    # np.set_printoptions(precision = 2)
    # class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    # plt.figure(figsize = (12, 6))
    # plot_confusion_matrix(cm, classes = class_names,
    #                       title = 'Confusion matrix')
    # plt.show()


    ### Multi-layer Perceptron
    from sklearn.neural_network import MLPClassifier

    t0 = time()
    print('Training and predicting classes using Randon Forest Classifier...')
    classifier = MLPClassifier(hidden_layer_sizes=(100, 50), verbose=False)
    y_pred = classifier.fit(X_train, y_train).predict(X_test)
    print('done in %0.3fs.' % (time() - t0))

    # Printing accuracy
    acc = accuracy_score(y_test, y_pred)
    print('Accuracy: ', str(acc))

    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    # np.set_printoptions(precision=2)
    # class_names = ['A','B','C','D','E','F','G','H']
    # plt.figure(figsize=(12,6))
    # plot_confusion_matrix(cm, classes=class_names, title='Confusion matrix')
    # plt.show()

if __name__ == '__main__':
    main()

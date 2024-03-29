# %%
import pandas as pd
# %%
df = pd.read_csv(
    '/Volumes/Sandisk/Projects/data_samples/ml/multi_classfier.txt', sep='\t')
df.head()
# %%

df = df[pd.notnull(df['desc'])]
# %%
df.info()
# %%

col = ['info_type', 'desc']
df = df[col]
# %%

df.columns
# %%

df.columns = ['info_type', 'desc']
# %%

df['category_id'] = df['info_type'].factorize()[0]
from io import StringIO
category_id_df = df[['info_type', 'category_id']
                    ].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'info_type']].values)

# %%
df.head()
# %%

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8, 6))
df.groupby('info_type').desc.count().plot.bar(ylim=0)
plt.show()

# %%

from sklearn.feature_extraction.text import TfidfVectorizer

#mn_df = 5
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=2, norm='l2',
                        encoding='latin-1', ngram_range=(1, 2), stop_words='english')

features = tfidf.fit_transform(df.desc).toarray()
labels = df.category_id
features.shape

# %%

from sklearn.feature_selection import chi2
import numpy as np

N = 2
for Product, category_id in sorted(category_to_id.items()):
    features_chi2 = chi2(features, labels == category_id)
    indices = np.argsort(features_chi2[0])
    feature_names = np.array(tfidf.get_feature_names())[indices]
    unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
    bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
    print("# '{}':".format(Product))
    print("  . Most correlated unigrams:\n       . {}".format(
        '\n       . '.join(unigrams[-N:])))
    print("  . Most correlated bigrams:\n       . {}".format(
        '\n       . '.join(bigrams[-N:])))

# %%
# training

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

X_train, X_test, y_train, y_test = train_test_split(
    df['desc'], df['info_type'], random_state=0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, y_train)

# %%
print(clf.predict(count_vect.transform(
    ["This company refuses to provide me verification and validation of debt per my right under the FDCPA. I do not believe this debt is mine."])))


print(clf.predict(count_vect.transform(
    ["business type limited"])))

# %%


# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.svm import LinearSVC

# from sklearn.model_selection import cross_val_score


# models = [
#     RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
#     LinearSVC(),
#     MultinomialNB(),
#     LogisticRegression(random_state=0),
# ]
# CV = 5
# cv_df = pd.DataFrame(index=range(CV * len(models)))
# entries = []
# for model in models:
#     model_name = model.__class__.__name__
#     accuracies = cross_val_score(
#         model, features, labels, scoring='accuracy', cv=CV)
#     for fold_idx, accuracy in enumerate(accuracies):
#         entries.append((model_name, fold_idx, accuracy))
# cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

# %%

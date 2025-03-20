import numpy as np # linear algebra
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("punkt")
nltk.download("stopwords")
nltk.download('punkt_tab')

featurizer=TfidfVectorizer(
    stop_words=stopwords.words('english'),
    norm='l1',
)

def get_sentence_score(tfidf_row):
    ##return thr avg of non-0 values
    # of the tf*odf vector representation of the sentence

    ## if sentence non null
    ## avg of none null sents
    x=tfidf_row[tfidf_row!=0]
    return x.mean()

def summarize(text):
    # extract sentences
    text = text.strip()
    sents= nltk.sent_tokenize(text)

    #perform tf-idf
    X=featurizer.fit_transform(sents)

    #compute scores for each sentence
    scores = np.zeros(len(sents))
    for i in range(len(sents)):
        score=get_sentence_score(X[i,:])
        scores[i]=score

    #sort the scores
    sort_idx=np.argsort(-scores)

    #print summary
    res = []
    for i in sort_idx[:5]:
        res.append(sents[i])
    return ' '.join(res)    
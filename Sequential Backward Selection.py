"""
Sequential Backword Selection算法
SBS依次从特征集合中删除某些特征，直到新的特征子空间包含指定数量的特征。
为了确定每一步的所需删除的特征，定义一个需要最小化的标准衡量函数J
该函数计算准则：比较判定分类器的性能在删除某个特定特征前后的差异。
算法步骤：
1.设k=d进行算法初始化，其中d是特征空间Xd的维度
2.定义x-为满足标准x-=argmaxJ(Xk-x)最大花的特征，其中x∈Xk
3.将特征x-从特征集合中删除：X(k-1)=Xk-x-,k=k-1
4.如果k等于目标特征数量，算法终止，否则跳转步骤2
"""
from itertools import combinations

import numpy as np
from sklearn.base import clone
from sklearn.metrics import accuracy_score
import sklearn.cross_validation


class SBS():
    def __init__(self, estimator, k_features, scoring=accuracy_score,
                 test_size=0.25, random_state=1):
        self.scoring = scoring
        self.estimator = clone(estimator)
        self.k_features = k_features
        self.test_seize = test_size
        self.random_state = random_state

    def fit(self, X, y):
        X_train, X_test, y_train, y_test = \
            sklearn.cross_validation.train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)

        dim = X_train.shape[1]
        self.indces_ = tuple(range(dim))
        self.subsets_ = [self.indices_]
        score = self._calc_score(X_train, y_train, X_test, y_test, self.indices_)

        self.scores_ = [score]

        while dim>self.k_features:
            scores=[]
            subsets=[]

            for p in combinations(self.indices_,r=dim-1):
                score=self._calc_score(X_train,y_train,X_test,y_test,p)
                scores.append(score)
                subsets.append(p)

            best=np.argmax(scores)
            self.indices_=subsets[best]
            self.subsets_.append(self.indices_)
            dim-=1

            self.scores_.append(scores[best])
        self.k_score_=self.scores_[-1]

        return self

    def transform(self,X):
        return X[:,self.indices_]

    def _calc_score(self,X_train,y_train,X_test,y_test,indices):
        self.estimator.fit(X_train[:,indices],y_train)
        y_pred=self.estimator.predict(X_test[:,indices])
        score=self.scoring(y_test,y_pred)
        return score

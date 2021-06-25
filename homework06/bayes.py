import collections
import math


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.classes = list()
        self.classes_p = dict()
        self.X_set = set()
        self.d = int()
        self.counters = dict()
        self.count_words = dict()

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        y_list = y
        self.classes = list(set(y))
        for class_ in self.classes:
            self.classes_p[class_] = y_list.count(class_) / len(y_list)

        set_x = str()
        for x in X:
            set_x += x
        self.X_set = set(set_x.split(" "))
        self.d = len(self.X_set)

        sort_massages = {}
        for key in self.classes:
            sort_massages[key] = str()
        for i, msg in enumerate(X):
            sort_massages[y[i]] += msg
        for key in self.classes:
            sort_massages[key] = sort_massages[key].split(" ")

        for key in self.classes:
            self.counters[key] = collections.Counter()
            for word in sort_massages[key]:
                self.counters[key][word] += 1
            self.count_words[key] = sum(self.counters[key].values())

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        predicts = []
        for msg in X:
            words = msg.split(" ")
            words_p = {}
            for key in self.classes:
                words_p[key] = []
            for word in words:
                if word in self.X_set:
                    for key in self.classes:
                        words_p[key].append(
                            (self.counters[key][word] + self.alpha)
                            / (self.count_words[key] + self.d * self.alpha)
                        )
                else:
                    for key in self.classes:
                        words_p[key].append(0)

            keys_res = {}
            for key in self.classes:
                keys_res[key] = math.log(self.classes_p[key]) + sum(
                    [math.log(x) for x in words_p[key] if x > 0]
                )

            max_ = keys_res[self.classes[0]]
            predict = self.classes[0]
            for key in self.classes:
                if max_ < keys_res[key]:
                    max_ = keys_res[key]
                    predict = key
            predicts.append(predict)
        return predicts

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        v_len = len(X_test)
        predicts = self.predict(X_test)
        same_results = 0
        for i, target in enumerate(predicts):
            if target == y_test[i]:
                same_results += 1
        return same_results / v_len

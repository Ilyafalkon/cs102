import csv
import pathlib

import bayes
import hackernews


def test_classification_massages_dataset() -> None:
    with (pathlib.Path(__file__).parent / "data/SMSSpamCollection").open() as file:
        dataset = list(csv.reader(file, delimiter="\t"))
    msgs, targets = [], []
    for target, msg in dataset:
        msgs.append(msg)
        targets.append(target)

    msgs = [hackernews.clean(msg).lower() for msg in msgs]
    msgs_train, targets_train, msgs_test, targets_test = (
        msgs[:3900],
        targets[:3900],
        msgs[3900:],
        targets[3900:],
    )

    model = bayes.NaiveBayesClassifier()
    a = model.fit(msgs_train, targets_train)

    assert model.score(msgs_test, targets_test) > 0.95

from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    row = s.query(News).filter_by(id=request.query.id).first()
    row.label = request.query.label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    rows = s.query(News).filter().all()
    check = []
    dict_of_author_with_title = {}
    for i in range(len(rows)):
        dict_of_author_with_title[rows[i].author] = rows[i].title
        check.append(dict_of_author_with_title)
        dict_of_author_with_title = {}

    news = get_news("https://news.ycombinator.com/newest")
    for new in news:
        check_in_rows = {}
        check_in_rows[new["author"]] = new["title"]
        if check_in_rows in check:
            break
        else:
            s = session()
            new = News(
                title=new["title"],
                author=new["author"],
                url=new["url"],
                comments=new["comments"],
                points=new["points"],
            )
            s.add(new)
            s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    marked_news = s.query(News).filter(News.label != None).all()
    marked_news = [[new.title, new.label] for new in marked_news]
    X_train = [n[0] for n in marked_news]
    y_train = [n[1] for n in marked_news]

    model = NaiveBayesClassifier(alpha=1)
    model.fit(X_train, y_train)

    news = s.query(News).filter(News.label == None).all()
    news_ids = [new.id for new in news]
    news = [new.title for new in news]
    predicts = model.predict(news)

    classified_news = {}
    labels = []
    for label in list(set(y_train)):
        classified_news[label] = []
        labels.append(label)

    for i, predict in enumerate(predicts):
        classified_news[predict].append(news_ids[i])

    rows_good = []
    rows_maybe = []
    rows_never = []
    for label in labels:
        for id in classified_news[label]:
            if label == "good":
                rows_good.append(s.query(News).filter(News.id == id).first())
            if label == "maybe":
                rows_maybe.append(s.query(News).filter(News.id == id).first())
            if label == "never":
                rows_never.append(s.query(News).filter(News.id == id).first())
    return template(
        "classification_template", good_rows=rows_good, maybe_rows=rows_maybe, never_rows=rows_never
    )


if __name__ == "__main__":
    run(host="localhost", port=8080)

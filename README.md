# gunosy_assignment

## 環境構築

- Python 3.6
- Django 1.11
- mysql 5.7.21

## 動作手順

### 1. Gunosyの記事をスクレイピングし、データベースに保存。

```
python manage.py scrape_articles
```

### 2. モデルの学習

```
python manage.py fit_model
```

### 3. ローカル環境でdjangoプロジェクトを立ち上げる。

```
python manage.py runserver
```

ブラウザ上で、`localhost:8000/search_form`に接続し、Gunosyの記事URLを指定フォームに入力する。


## 作った分類器の精度

0.767

### 精度の評価関数

「正解率」を利用。

```py
def score(self, docs, cats):
    acc_count = 0
    total_len = len(cats)
    for i in range(total_len):
        pred = self.predict(docs[i])
        if pred == cats[i]:
            acc_count += 1

    score = acc_count / total_len
    return score
```

### 分類器ごとの精度の比較

| 分類器 | 精度 |
|:-----------:|:------------:|
| NaiveBayes（自作） | 0.767 |
| MultinomialNB | 0.846 |
| SGDClassifier | 0.858 |
| KNeighborsClassifier | 0.289 |
| LogisticRegression | 0.888 |
| LinearSVC | 0.869 |
| RandomForestClassifier | 0.753 |
| DecisionTreeClassifier | 0.661 |

### 精度向上のための工夫

#### 記事コンテンツにタイトルを加えた

- 記事コンテンツの文字数が100文字に満たない「動画はこちら...」という記事が5%ほどあった。
- たい部分の記事においてタイトルは重要で分類に寄与する単語が入っている確率が高いという仮説

以上から、文書 = タイトル + コンテンツとしたところ、精度が1%〜4%向上した。

#### 文書を形態素解析する際に、名詞・動詞のみを抜き出す

カテゴリ分類に寄与する単語は、名詞と動詞くらいではないか？という仮説より。



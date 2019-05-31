#Request Record
#検索では大文字小文字の区別をなくす(case insensitive) 済
#PrintでPostされた内容をコンソールに出しておくようにすれば見れるよ　済
#プロジェクト名を入力する
#じゃ追加仕様として、検索結果が存在するプロジェクトの名前一覧をテーブルの上に表示してもらってもいい？(検索結果が含まれるPJ: Barzan, KNPC,　みたいな感じで)

# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
import re

# MLCLファイル取得
df = pd.read_table('MLCL007DL_KNPC.txt')
df = df.fillna('')
df['Description'] = df['Piping Class']+' '+df['ShortCd']+' '+df['OptCd'].astype(str)+' '+df['Sch1']+' '+df['Sch2']+' '+df['Commodity Code']+' '+df['Part Desc']+' '+df['Matl Std']+' '+df['Rating/Seam']


# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# メッセージをランダムに表示するメソッド
def picked_up():
    messages = [
        "配管サイズや検索条件を入力してください",
        "配管サイズや検索条件を入力してみて？"
    ]
    # NumPy の random.choice で配列からランダムに取り出し
    return np.random.choice(messages)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "MLCL test"
    message = picked_up()
    # index.html をレンダリングする
    return render_template('index.html',
                           message=message, title=title)

# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "検索結果"
    if request.method == 'POST':
        # リクエストフォームから「サイズ、キーワード」を取得して
        size = request.form['size']
        key = request.form['key']
        rekey = re.compile(key, re.IGNORECASE)
        
        if size != '':
            if key != '':
                #その条件でテーブルを抽出
                df_query = df[df['Description'].str.contains(rekey)==True].query('Size1 =='+str(size))
            elif key == '':
                df_query = df.query('Size1 =='+str(size))
        elif size == '':
            if key != '':
                df_query = df[df['Description'].str.contains(rekey)==True]
                size ='ALL_'
            elif key == '':
                df_query = df
                size = 'ALL_'
                key = '全条件'
        
        df_list = []
        for i in range(len(df_query)):
            for j in range(len(df_query.columns)):
                df_list.append(df_query.iat[i,j])
        
        # index.html をレンダリングする
        print(size,key, 'で検索されました')
        df_query.to_csv(r'http:\\10.1.82.225:8050\test.csv')
        return render_template('index.html',size=size,key=key,head=df_query,data=df_list, title=title)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0',port=8050) # どこからでもアクセス可能に
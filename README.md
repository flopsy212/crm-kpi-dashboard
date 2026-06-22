# crm-kpi-dashboard

CRMの商談データを想定し、Python・SQL・SQLite・Streamlitを使って、データ整形からKPI可視化までを行うダッシュボードを作成しました。

# Demo

Streamlit Community Cloudでデプロイしています。
https://crm-kpi-dashboard-mxzspgar3faejwppknu5x7.streamlit.app

## 概要

このプロジェクトでは、CRMに蓄積された商談データを想定したサンプルCSVを作成し、Pythonでデータ整形を行ったうえでSQLiteに格納しています。

その後、SQLで売上合計・商談件数・受注率・月別売上・担当者別売上などのKPIを集計し、Streamlitでダッシュボードとして可視化しています。

データ抽出・整形・DB格納・SQL集計・ダッシュボード化までの一連の流れを確認できるポートフォリオです。

## 使用技術

* Python
* pandas
* SQLite
* SQL
* Streamlit

## 作成した機能

* CRM商談データを想定したダミーCSVの作成
* Python / pandasによるデータ整形
* 日付・金額・欠損値の整形
* SQLiteへのデータ格納
* SQLによるKPI集計
* Streamlitによるダッシュボード表示

## 表示しているKPI

* 売上合計
* 商談件数
* 受注率
* 平均商談金額
* 月別売上推移
* 担当者別売上
* ステージ別商談金額
* 商談データ一覧

## ファイル構成

```text
crm-kpi-dashboard/
├── data/
│   ├── raw_crm_opportunities.csv
│   └── processed_crm_opportunities.csv
├── db/
│   └── crm.db
├── sql/
│   └── kpi_queries.sql
├── src/
│   ├── generate_sample_data.py
│   ├── etl.py
│   └── app.py
├── README.md
└── requirements.txt
```

## 処理の流れ

### 1. サンプルデータ作成

`generate_sample_data.py` で、CRMの商談データを想定したダミーCSVを作成しています。

主な項目は以下です。

* 商談ID
* 顧客名
* 業界
* 地域
* 担当者
* 商談ステージ
* 商談金額
* 作成日
* クローズ予定日

### 2. データ整形

`etl.py` でCSVを読み込み、分析しやすい形に整形しています。

主な処理内容は以下です。

* 日付データの型変換
* 金額データの数値変換
* 担当者の欠損値補完
* 月次集計用カラムの追加
* 受注フラグの追加
* 失注フラグの追加
* リードタイムの算出

### 3. SQLiteへの格納

整形後のデータをSQLiteの `opportunities` テーブルに格納しています。

また、集計でよく使う以下の項目にはインデックスを作成しています。

* close_month
* owner
* stage

### 4. SQLによるKPI集計

`kpi_queries.sql` に、KPI集計用のSQLをまとめています。

主な集計内容は以下です。

* 全体KPI
* 月別売上
* 担当者別売上
* ステージ別商談金額
* 業界別受注率

### 5. ダッシュボード化

`app.py` でSQLiteからデータを読み込み、StreamlitでKPIとグラフを表示しています。

画面上では、担当者・商談ステージ・業界で絞り込みながら、売上や受注率を確認できます。

## 実行方法

### 1. ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 2. サンプルデータの作成

```bash
python src/generate_sample_data.py
```

### 3. ETL処理の実行

```bash
python src/etl.py
```

### 4. Streamlitアプリの起動

```bash
streamlit run src/app.py
```

## 工夫した点

* CRMの商談データを想定し、実務に近い項目構成にしたこと
* 生データと整形後データを分け、ETLの流れが分かるようにしたこと
* 受注率や月別売上など、業務で確認されやすいKPIを設定したこと
* SQLで集計しやすいように、月次カラムや受注フラグを追加したこと
* Streamlitで、非エンジニアでも確認しやすいダッシュボードにしたこと

## 今後の改善案

* Power BIで同様のダッシュボードを作成する
* SnowflakeなどのクラウドDWHを想定した構成に変更する
* データマート設計を追加する
* KPI定義書を作成する
* 顧客別・業界別の分析を追加する
* 売上予測や受注確度分析を追加する

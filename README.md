# DB Framework Comparison Project

## 1.プロジェクト概要
- Flask / FastAPI / Django
- SQLite / MySQL / PostgreSQL
- Native SQL / ORM

## 2.プロジェクト一覧
| Framework | DB         | Access     |
| --------- | ---------- | ---------- |
| Flask     | SQLite     | Native     |
| Flask     | SQLite     | SQLAlchemy |
| Flask     | MySQL      | Native     |
| Flask     | MySQL      | SQLAlchemy |
| Flask     | PostgreSQL | Native     |
| Flask     | PostgreSQL | SQLAlchemy |
| FastAPI   | SQLite     | Native     |
| FastAPI   | SQLite     | SQLAlchemy |
| FastAPI   | MySQL      | Native     |
| FastAPI   | MySQL      | SQLAlchemy |
| FastAPI   | PostgreSQL | Native     |
| FastAPI   | PostgreSQL | SQLAlchemy |
| Django    | SQLite     | ORM        |
| Django    | MySQL      | ORM        |
| Django    | PostgreSQL | ORM        |

## 3.共通機能
- 一覧表示
- 詳細表示
- 新規登録
- 編集
- 削除
- CSV一括取り込み
- キーワード検索
- 誕生日範囲検索

## ４．技術比較
### Flask
- 一番手軽
- 取り組みやすい

### FastAPI
- HTMLへの引数の授受がFlaskよりも多くなる
- フォルダ構成はFlaskと似ている

### Django
- app.pyを用いず、Pythonファイルを多数作成
- Djangoの各種コマンドにより上記をある程度自動作成
- DBを作ると、独自管理画面がデフォルトで付属し、自動ででCRUDになる

## 5.DB比較
### SQLite
- プロジェクト内にDBファイルが作られる
- create_db.pyを実行すると、DB作成、テーブル作成が出来る
- DB接続がシンプル

### MySQL
- DBにログインして空のDBを作成の上、create_db.pyを実行してテーブル作成
- DB接続の設定項目が多い
- 普及率が高いとのこと

### PostgreSQL
- DB接続の設定項目が多い（４つ以上）
- 高機能　画像なども扱える

## 6.ORM比較
### Native SQL
- SQLを直接記述
- 基本となる方法

### SQLAlchemy
- SQLでしたいことをPythonコードで記述する
- SQLite/MySQL/PostgreSQL間で殆ど差異がない

### Django ORM
- 管理画面の自動作成など慣れると使い易いとのこと

## 7.本番環境
### flask-sqlite-native
- URL:https://db-framework-tests-production.up.railway.app/
- リリース：2026/10/09 Fri

### flask-sqlite-sqlalchemy
- URL:https://db-framework-tests-production-df88.up.railway.app/
- リリース：2026/10/10 Sat

### fastapi-sqlite-native
- URL:https://db-framework-tests-production-6106.up.railway.app/
- リリース：2026/10/10 Sat

### fastapi-sqlite-sqlalchemy
- URL:https://db-framework-tests-production-e24c.up.railway.app/
- リリース：2026/10/11 Sun

### django-sqlite-orm
- URL:

## 8.開発で苦労した点
- フレームワークが異なると書き方が変わる。
- リポジトリを一つにまとめ、配下に15プロジェクトを配したため、ローカルからgitで何かPUSHすると、Railway上の各プロジェクトで一斉に再デプロイが走ってしまう。

## 9.今後の予定
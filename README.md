# Home Server
家庭内に以下のサーバを構築する。

* NAS
* Web Server
* Database
* Infrared Controller

## 使い方
### ビルド
以下のコマンドを実行し、docker imageのビルドを行う。

```sh
# docker-compose.ymlがあるディレクトリで実行
docker-compose build
```

### 起動
以下のコマンドを実行し、コンテナを起動する。

```sh
# docker-compose.ymlがあるディレクトリで実行
docker-compose up -d
```

### コマンドの登録
1. コンテナを起動後、`database/controller.csv`と`database/command.csv`をGitHubからダウンロードしておく。
1. Webブラウザから`http://raspberrypi.local:8080`にアクセスする。
1. 「Page Links」にある「phpMyAdmin」を押下する。
1. phpMyAdminに接続する。

#### Controllerのデータ追加
1. 左側のツリーから、「database」→「Controller」の順に押下する。
1. 表示されたテーブルのリボンメニューから「インポート」を押下する。
1. ファイル選択から、ダウンロードした「controller.csv」を選択する。
1. ページ下部の「実行」を押下する。

#### Commandのデータ追加
1. 左側のツリーから、「database」→「Command」の順に押下する。
1. 表示されたテーブルのリボンメニューから「インポート」を押下する。
1. ファイル選択から、ダウンロードした「command.csv」を選択する。
1. ページ下部の「実行」を押下する。

### docker-composeの利用
#### ログの確認
```sh
# ログを出力
docker-compose logs
# 時間でソート
docker-compose logs -t | sort -k 2
```

#### 不要なイメージを削除
```sh
# 中間イメージ、ビルド時のキャッシュも削除
docker system prune -a
# 未使用のボリュームの削除
docker system prune --volumes
```

## コンテナ構成
### NAS
* 使用するベースイメージ

    dperson/samba

* サービス名

    nas

* マウント対象

    /mnt/portable_ssd/storage

### Infrared Controller
* 使用するベースイメージ

    node:16-alpine3.11

* サービス名

    infrared_controller

### Node-Red
* 使用するベースイメージ

    nodered/node-red:2.2.2-12

* サービス名

    nodered

* HTTPリクエストのパターン

    | link          | command | 処理内容        |
    | :----         | :----   | :----           |
    | /light        | on      | 照明ON          |
    | /light        | off     | 照明OFF         |
    | /light        | night   | こだまにする    |
    | /light        | up      | 明るくする      |
    | /light        | down    | 暗くする        |
    | /light        | all     | 全灯            |
    | /electric-fan | on      | 扇風機の電源ON  |
    | /electric-fan | off     | 扇風機の電源OFF |
    | /electric-fan | up      | 扇風機の風量UP  |
    | /cooler       | on      | 冷房ON          |
    | /cooler       | off     | 冷房OFF         |
    | /heater       | on      | 暖房ON          |
    | /heater       | off     | 暖房OFF         |
    | /dry          | on      | 除湿ON          |
    | /dry          | off     | 除湿OFF         |

### Nginx
* 使用するベースイメージ

    nginx:latest

* サービス名

    nginx

* ルーティング

    | url         | access to        |
    | :---        | :---             |
    | /           | web_server:3000/ |
    | /phpmyadmin | phpmyadmin:9000/ |

### Database
* 使用するベースイメージ

    linuxserver/mariadb:10.5.15

* サービス名

    database

### phpMyAdmin
* 使用するベースイメージ

    arm64v8/phpmyadmin:fpm-alpine

* サービス名

    phpmyadmin

### Web Server
* 使用するベースイメージ

    node:16-alpine3.11

* サービス名

    web_server

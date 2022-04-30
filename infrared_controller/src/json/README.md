# Shell Scriptの使い方
## 対象
* 赤外線学習リモコンとして「ADRSIR」を利用している。
* python3版のsmbusがインストール済み。

## 事前準備
* 学習させたいリモコンを用意する。
* 赤外線学習リモコンのモード切替スイッチを「記憶（learn）」に変更する。
* 操作スイッチの0～9を押下後、リモコンのボタンを押下し、学習させる。

    この時、ボタンとリモコンのボタンが対応するようにメモを取ること。

* docker-composeコマンドでinfrared_controllerのサービスを起動する。

## JSONファイルの生成
* create_json.shをエディタで開く。
* 「制御ボタン番号 制御名」を1行に出力する関数を定義する。ここでは、サンプルとして以下の関数が定義済みである。

    * mapping_light

        制御ボタン番号と照明制御時の制御名とのマッピング

* 関数を増やした場合、同一ファイル内にあるcase文に実行時のオプションとして追加する。
* 以下のコマンドを実行し、JSONファイルを生成する。

    ```bash
    docker exec -it infrared_controller /infrared_controller/json/create_json.sh "実行コマンド" > json-filename
    ./create_json.sh "実行コマンド" > json-filename
    # ex) docker exec -it infrared_controller /infrared_controller/json/create_json.sh light > light.json # 照明
    ```

## config.jsonの更新
生成したjsonファイルをconfig.jsonに登録する。形式は以下の通り。

## 注意点
* 定義した「制御名」は、Node-Red側でコマンドを呼び出す際に利用する。

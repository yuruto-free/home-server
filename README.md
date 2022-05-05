# Home Server
家庭内に以下のサーバを構築する。

* NAS
* Web Server
* Database
* Infrared Controller

## NAS
* 使用するベースイメージ

    dperson/samba

* サービス名

    nas

* マウント対象

    /mnt/portable_ssd/storage

## Infrared Controller
* 使用するベースイメージ

    node:16-alpine3.11

* サービス名

    infrared_controller

## Node-Red
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

## Nginx
* 使用するベースイメージ

    nginx:latest

* サービス名

    nginx

* ルーティング

    | url         | access to        |
    | :---        | :---             |
    | /           | web_server:3000/ |
    | /phpmyadmin | phpmyadmin:9000/ |

## Database
* 使用するベースイメージ

    linuxserver/mariadb:10.5.15

* サービス名

    database

## phpMyAdmin
* 使用するベースイメージ

    arm64v8/phpmyadmin:fpm-alpine

* サービス名

    phpmyadmin

## Web Server
* 使用するベースイメージ

    node:16-alpine3.11

* サービス名

    web_server

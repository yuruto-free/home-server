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

    nodered/node-red:1.3.5-12-minimal-arm32v6

* サービス名

    nodered

# JPHACKS-WBonPC

October, 3, 2019 YusukeKyokawa

## About

This is an app for managing post-it on a whiteboard on your laptop.

ホワイトボードに貼られたポストイットをパソコンにて管理するためのWebアプリ

## Descritption

I'll show you how I implement this app.

1. send a picture of whiteboard to a server.
2. detect the region of post-it using image processing on the server and crop the image.
3. reproduce the whiteboard on your laptop using the croppped image

実装手順を簡単に示す．

1. スマホで撮影したホワイトボードの写真をサーバに送信
2. サーバ側で画像処理を行い，四角いポストイットの領域を抽出．画像を切り取る．
3. 切り取った画像からホワイトボードをPC上で再現する．

## Usage

## Requirements

- Flask==1.1.1
- Flask-Login==0.4.1
- bottle==0.12.17
- opencv-python==4.1.0.25
- Pillow==6.0.0
- numpy==1.16.4

## Install

you need to build and execute docker container

```bash
$sudo docker-compose up --build
```

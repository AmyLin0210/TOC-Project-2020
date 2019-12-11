# TOC Project 2018

## Introduce

在放假或者收假時，高速公路總是塞車，
因此使用 python 爬蟲獲得高速公路的即時區間速度，
並時作為聊天機器人方便查詢。


## Finite State Machine
![](https://i.imgur.com/u3uejTD.png)


## Usage

在除了 user state 外輸入離開，即可回到 `start_chatting` state

- user
    - Input: 任意文字
        - Reply: "輸入任意字開始查詢"
- start_chatting
    - Input: 任意文字
        - Reply: "輸入任意字開始查詢"
- which_road
    - Input: 哪條國道
        - Reply: "請問你要查詢哪條國道？"
- which_direction
    - Input: 北上/南下
        - Reply: "請問您要北上/南下？"
- from_location
    - Input: 起始交流道
        - Reply: "請輸入起始交流道"
- end_location
    - Input: 終點交流道
        - Reply: "請輸入終點交流道"
- show_speed
    - Input: 任意文字
        - Reply: "start_chatting"

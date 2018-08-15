# pycon18-tutorial-chatterbox

PyconKR'18에서 진행하는 `chatterbox` 라는 간단한 채팅앱을 완성시켜보는 튜토리얼입니다. 단계적 설명문을 따라오신다면 어렵지 않게 완성하실 수 있습니다.

## Features

- 일대 다수 채팅
- 예약 메세지 보내기
- 프로필 변경
- 랜덤 채팅

## Lessons

### 1. 시작하기

#### Setup

Sanic 서버와 클라이언트를 설치해서 채팅앱을 실행시켜봅니다.

##### Server

1. install python 3.6.1

pyenv, virtualenv(optional) 이용하여 설치합니다.

2. install python packages
```
$ pip install -r requirements
```

##### Client

1. install npm(https://www.npmjs.com/get-npm)

2. install node modules

```
$ cd client/
$ npm install
```

자, 이제 서버와 클라이언트를 실행시켜봅니다.

```
$ python lesson01/server.py # run server
$ npm start # run client
```

서버에 curl 또는 Postman으로 hello world로 응답하는 걸 확인하실 수 있습니다.
이제 이 서버를 websocket 에코 서버로 만들어봅시다. sanic의 websocket 이용해서 구현합니다.

참고 자료:
http://sanic.readthedocs.io/en/latest/sanic/routing.html#websocket-routes
https://breadcrumbscollector.tech/dive-into-pythons-asyncio-part-4-simple-chat-with-sanic/

### 2. 메세지 보내기

에코 서버를 일대 다수 채팅을 할 수 있게 만들어봅시다. 받은 메세지를 접속해 있는 모든 유저들에게 보내줍니다.
복잡도를 줄이기 위해 데이터베이스 레이어 없이 구현합니다.

참고 자료:
https://github.com/r0fls/sanic-websockets/blob/master/examples/chat/chat.py

### 3. 예약 메세지 보내기

### 4. 프로필 변경하기

### 5. 랜덤 채팅 구현하기 (Optional)
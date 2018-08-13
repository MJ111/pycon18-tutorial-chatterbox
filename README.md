# pycon18-tutorial-chatterbox

PyconKR'18에서 진행하는 `chatterbox` 라는 간단한 채팅앱을 완성시켜보는 튜토리얼입니다. 단계적 설명문을 따라오신다면 어렵지 않게 완성하실 수 있습니다.

### Features

- 일대 다수 채팅
- 예약 메세지 보내기
- 프로필 변경
- 랜덤 채팅

## Lessons

### 1. 시작하기

Sanic 서버와 클라이언트를 설치해서 채팅앱을 실행시켜봅니다.

#### Server

1. install python 3.6.1

pyenv, virtualenv(optional) 이용하여 설치합니다.

2. install python packages
```
$ pip install -r requirements
```

#### Client

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

메세지를 보내면 그대로 응답하는 에코 서버를 확인할 수 있습니다.

### 2. 메세지 보내기


### 3. 예약 메세지 보내기

### 4. 프로필 변경하기

### 5. 랜덤 채팅 구현하기 (Optional)
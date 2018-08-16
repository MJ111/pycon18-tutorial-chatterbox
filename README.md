# pycon18-tutorial-chatterbox

PyconKR'18에서 진행하는 `chatterbox` 라는 간단한 채팅앱을 완성시켜보는 튜토리얼입니다. 
단계적으로 기능을 더하면서 좀더 쉽게 이해할 수 있게 구성했습니다.
웹 클라이언트는 이미 완성되어 있어 서버 구현에만 집중할 수 있습니다.

## Features

- 일대 다수 채팅
- 예약 메세지 보내기
- 랜덤 채팅

## Lessons

각 디렉토리 안의 server.py 파일을 기반으로 구현을 시작하게 됩니다. 
순서대로 진행하는 것을 권장하며 각 레슨의 솔루션은 다음번 레슨의 server.py에 구현되어 있습니다.
최종 완성본은 루트 디렉토리의 server.py 입니다.

### Client - Server 통신시 주의사항
- `client/src/App.js:52:url`의 server host를 알맞게 변경해주셔야합니다.

- 웹 클라이언트에서 메세지를 입력하면 서버로 메세지를 가공하여 보냅니다. 이때 보내오는 JSON 데이터의 구조는 다음과 같습니다.
```json
{
    "author": "811f560b0a503505a46e4843a1a25b0a", 
    "type": "text", 
    "data": {
      "text": "Hello, World!"
    }
}
```

author; 보낸 이, type; text 혹은 emoji 인지 메세지 유형, data; 유저가 입력한 실제 메세지.

좀 더 다양한 예시는 `client/src/messageHistory.js`를 참조해주세요.
 

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

### 3. 유저 구별하기

다른 유저가 보낸 메세지를 받았지만 누구에게서 메세지를 받은 건지 구별할 수가 없습니다. 서버에서 클라이언트로 메세지를 보낼 때 구별할 수 있는 아이디를 보내줘서 클라이언트가 메세지를 구별할 수 있게 해봅시다.
클라이언트에서는 데이터의 `"author"` 값으로 메세지를 구별합니다.

참고 자료:
https://docs.python.org/3/library/uuid.html

### 4. 예약 메세지 보내기

슬랙의 "/remind" 커맨드와 유사한 "/schedule" 커맨드를 만들어봅니다. 시분초와 메세지 입력을 받아 해당 시간이 지나면 메세지를 보냅니다.
다음과 같은 문법으로 이루어져 있습니다. 커맨드 뒤에 hours, minutes, seconds 를 중복해서 적을 수 있고 그 다음 `message`, 실제 메세지를 적습니다. `' '`로 구분자를 사용합니다.
```
/schedule ({timeunits} {timedelta number})+ message {real message}
```

예를 들어,
```
/schedule hours 1 seconds 9 message how are you doing future?
```
과 같이 유저가 입력을 하면 서버에서 이 커맨드를 인식하여 알맞게 실행해야 합니다.

참고 자료:
https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep

### 5. 랜덤 채팅 구현하기 (Optional)

랜덤 채팅 버튼을 누르면 1:1로 랜덤한 사람과 대화할 수 있습니다.

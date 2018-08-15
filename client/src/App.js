import React, { Component } from 'react';
import {ChatWindow} from './react-chat-window/src';

class App extends Component {
  constructor() {
    super();
    this.state = {
      messageList: [],
      myId: ''
    };
  }

  _onMessageWasSent(message) {
    if (message.data.text.startsWith('/schedule ')) {
        const allowedUnits = ['hours', 'minutes', 'seconds']
        const messageRegex = /["'].*["']/;

        let scheduleMsg;
        const scheduleData = {}
        let userScheduleInput;

        const result = messageRegex.exec(message.data.text)
        if (result) {
            userScheduleInput = message.data.text.slice(0, result.index)
            scheduleMsg = result[0]
            scheduleMsg = scheduleMsg.slice(1,scheduleMsg.length-1)

            if (userScheduleInput) {
                userScheduleInput = userScheduleInput.split(' ')

                for (let i=1; i<userScheduleInput.length; i++) {
                    if (allowedUnits.includes(userScheduleInput[i])) {
                        scheduleData[userScheduleInput[i]] = userScheduleInput[i+1]
                    }
                }
            }
        }

        if (Object.keys(scheduleData).length && scheduleMsg) {
            message.data = {'schedule': scheduleData, "text": scheduleMsg}
            this.socket.send(JSON.stringify(message));
        }
    } else {
        this.setState({
          messageList: [...this.state.messageList, message]
        })
        this.socket.send(JSON.stringify(message));
    }
  }

  componentDidMount() {
    const url = "ws://192.168.0.9:8000/feed";
    this.socket = new WebSocket(url);
    this.socket.onopen = (event) => {
        console.log(`Socket is connected to "${url}"`)
    };
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data['id']) {
        this.setState({myId: data['id']})
        console.log(this.state.myId)
      } else {
          this.setState({
              messageList: [...this.state.messageList, data]
          })
      }
    }
  }

  componentWillUnmount() {
    this.socket.close();
  }

  render() {
    return (
    <div>
        <ChatWindow
          messageList={this.state.messageList}
          onUserInputSubmit={this._onMessageWasSent.bind(this)}
          agentProfile={{
              teamName: 'chatterbox',
              imageUrl: 'https://a.slack-edge.com/66f9/img/avatars-teams/ava_0001-34.png'
          }}
          myId={this.state.myId}
          isOpen
          onClose={() => {}}
          showEmoji
        />
    </div>)
  }
}

export default App;

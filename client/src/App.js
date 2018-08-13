import React, { Component } from 'react';
import {Launcher, ChatWindow} from './react-chat-window/src';

class App extends Component {
  constructor() {
    super();
    this.state = {
      messageList: []
    };
  }

  _onMessageWasSent(message) {
    this.setState({
      messageList: [...this.state.messageList, message]
    })
    this.socket.send(JSON.stringify(message));
  }

  componentDidMount() {
    const url = "ws://192.168.0.9:8000/feed";
    this.socket = new WebSocket(url);
    this.socket.onopen = (event) => {
        console.log(`Socket is connected to "${url}"`)
    };
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.setState({
          messageList: [...this.state.messageList, data]
      })
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
          isOpen
          onClose={() => {}}
          showEmoji
        />
    </div>)
  }
}

export default App;

import React, { Component } from 'react';
import {Launcher, ChatWindow} from './react-chat-window/src';
import messageHistory from './messageHistory';

class App extends Component {
  constructor() {
    super();
    this.state = {
      messageList: messageHistory
    };
  }

  _onMessageWasSent(message) {
    this.setState({
      messageList: [...this.state.messageList, message]
    })
  }

  _sendMessage(text) {
    if (text.length > 0) {
      this.setState({
        messageList: [...this.state.messageList, {
          author: 'them',
          type: 'text',
          data: { text }
        }]
      })
    }
  }

  render() {
    return (
    <div>
        <ChatWindow
          messageList={this.state.messageList}
          onUserInputSubmit={this._onMessageWasSent.bind(this)}
          agentProfile={{
              teamName: 'react-live-chat',
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

import React, { Component } from 'react'
import TextMessage from './TextMessage'
import EmojiMessage from './EmojiMessage'


class Message extends Component {

  _renderMessageOfType(type) {
    switch(type) {
      case 'text':
        return <TextMessage {...this.props.message} myId={this.props.myId} />
      case 'emoji':
        return <EmojiMessage {...this.props.message} myId={this.props.myId}/>
    }
  }

  render () {
    let contentClassList = [
      "sc-message--content",
      (this.props.message.author === this.props.myId ? "sent" : "received")
    ];
    return (
      <div className="sc-message">
        <div className={contentClassList.join(" ")}>
          {this._renderMessageOfType(this.props.message.type)}
        </div>
      </div>)
  }
}

export default Message
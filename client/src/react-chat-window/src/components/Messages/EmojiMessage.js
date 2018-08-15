import React from 'react'

const EmojiMessage = (props) => {
  return <div className="sc-message--emoji"
            style={props.author !== props.myId ? {backgroundColor: `#${props.author.slice(0, 6)}`, color: 'white'} : null}>
            {props.data.emoji}
        </div>
}

export default EmojiMessage
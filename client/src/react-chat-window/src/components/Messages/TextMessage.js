import React from 'react';

const TextMessage = (props) => {
  return <div className="sc-message--text"
            style={props.author !== props.myId ? {backgroundColor: `#${props.author.slice(0, 6)}`, color: 'white'} : null}>
            {props.data.text}
        </div>
}

export default TextMessage
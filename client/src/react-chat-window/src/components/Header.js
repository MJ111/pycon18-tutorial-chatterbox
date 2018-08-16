import React, { Component } from 'react';


class Header extends Component {

  render() {
    return (
      <div className="sc-header">
        <img className="sc-header--img" src={this.props.imageUrl} alt="" />
        <div className="sc-header--team-name" onClick={() => {window.location.href = '/'}}> {this.props.teamName} </div>
        <div className="sc-header--random" onClick={this.props.joinRandom}>random</div>
      </div>
    );
  }
}

export default Header;

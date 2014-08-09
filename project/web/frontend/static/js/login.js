/**
 * @jsx React.DOM
 */

const React = require('React');
const Immutable = require('immutable');
const Profile = require('./profile');
const http = require('./http');

module.exports = React.createClass({
  getInitialState: function() {
    return Immutable.Map({username: '', password: ''});
  },
  shouldComponentUpdate: function(nextProps, nextState) {
    return nextState != this.state;
  },
  handleUsernameChange: function(event) {
    this.state = this.state.set('username', event.target.value);
  },
  handlePasswordChange: function(event) {
    this.state = this.state.set('password', event.target.value);
  },
  handleSubmit: function(e) {
    e.preventDefault();
    http.post('/api/auth', JSON.stringify(this.state.toObject()))
      .then((response) => {
        http.setToken(response.token);
        React.renderComponent(<Profile />, document.getElementById('app'));
      })
      .catch((response) => {
        alert(response.responseJSON.description);
      });
  },

  render: function() {
    return (
        <div>
            <h1>Login</h1>
            <hr/>
            <form method="POST" name="form" role="form" onSubmit={this.handleSubmit}>
              <div className="form-group">
                 <label htmlFor="email">Email</label>
                 <input type="text" id="email" name="email" className="form-control" placeholder="Email" required onChange={this.handleUsernameChange}/>
              </div>
              <div className="form-group">
                 <label htmlFor="password">Password</label>
                 <input type="password" id="password" name="password" className="form-control" placeholder="Password" required onChange={this.handlePasswordChange}/>
              </div>
              <input type="submit" className="btn btn-primary btn-lg" value="Submit" />
            </form>
        </div>
    );
  }
});




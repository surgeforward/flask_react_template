/**
 * @jsx React.DOM
 */

const React = require('React');
const http = require('./http');
const Immutable = require('immutable');

module.exports = React.createClass({
  getInitialState: function() {
    return Immutable.Map({email: '', id: 0});
  },
  shouldComponentUpdate: function(nextProps, nextState) {
    return nextState != this.state;
  },
  componentDidMount: function() {
    http.get('/api/accounts/current')
      .then((data) => {
        this.state = Immutable.Map(data.data);
        this.forceUpdate();
      })
      .catch((response) => {
        console.log(responseJSON.status_code);
      });
  },
  render: function() {
    return (
        <div>Welcome {this.state.get('email')}</div>
    );
  }
});
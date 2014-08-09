const jQuery = require('jQuery');
const Promise = require('bluebird');

exports.setToken = function(token){
  jQuery.ajaxSetup({
      beforeSend: function (xhr)
      {
         xhr.setRequestHeader("Authorization","Bearer " + token);
      }
  });
};

exports.clearToken = function(token){
  jQuery.ajaxSetup({
      beforeSend: function (xhr)
      {
         xhr.setRequestHeader("Authorization", "");
      }
  });
};

exports.get = function(url){
    return Promise.resolve(jQuery.getJSON(url));
};

exports.post = function(url, data){
  return Promise.resolve(jQuery.post(url, data));
};

exports.put = function(url, data){
  return Promise.resolve(jQuery.ajax({
    url: url,
    dataType: 'json',
    contentType: 'json',
    type: 'PUT',
    data: data
  }));
};

exports.delete = function(url){
  return Promise.resolve(jQuery.ajax({
    url: url,
    dataType: 'json',
    contentType: 'json',
    type: 'DELETE'
  }));
};

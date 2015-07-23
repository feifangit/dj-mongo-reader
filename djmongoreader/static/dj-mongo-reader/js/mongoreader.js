(function (root) {
  'use strict';

  /**
   *  if you hava already loaded the jQuery, then use jQuery.ajax(), or use native XMLHttpRequest.
   * @param type -> http method type
   * @param url  -> request url
   * @param callback -> callback function
   * @returns {*}
   */
  var sendAjax = function (type, url, callback) {
    if (typeof jQuery !== 'undefined') {
      $.ajax({
        type: type,
        url: url,
        cache: false,
        dataType: 'json'
      }).done((typeof callback === 'function' && callback) ? callback : jQuery.noop());
    } else {
      var xmlhttp;
      if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
      } else {// code for IE6, IE5
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
      }
      xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
          if (typeof callback === 'function' && callback) {
            callback(JSON.parse(xmlhttp.responseText));
          }
        }
      };
      xmlhttp.open(type, url+'&t=' + Date.now(), true);
      xmlhttp.send();
    }
  };

  /**
   * convert json to string
   * @param obj -> json object
   * @type {JSON.stringify}
   */
  var jsonToString = typeof JSON != "undefined" ? JSON.stringify : function (obj) {
    var arr = [];
    $.each(obj, function (key, val) {
      var next = key + ": ";
      next += $.isPlainObject(val) ? jsonToString(val) : val;
      arr.push(next);
    });
    return "{ " + arr.join(", ") + " }";
  };

  /**
   * mixed url with url cmd criteria sort like '/mongo/db/collection/_find?criteria={...}&sort={...}'
   * @param url -> request url
   * @param cmd -> mongodb command like '_count/_find'
   * @param criteria -> query criteria
   * @param sort -> sort criteria
   * @param options -> mongodb option like '{skip:50, limit:50, batch_size:50 ...}'
   * @returns {string}
   */
  var mixURL = function (url, cmd, criteria, sort, options) {
    return url + cmd + '?' +
      (options ? convertOptions(options) : '') +
      (criteria ? '&criteria=' +
      encodeURIComponent(typeof criteria === 'string' ? criteria : jsonToString(criteria)) : '') +
      (sort ? '&sort=' +
      encodeURIComponent(typeof sort === 'string' ? sort : jsonToString(sort)) : '');
  };

  /**
   * convert option from json to url format, from {skip:10} to '&skip=10'
   * @param opts
   * @returns {string}
   */
  var convertOptions = function (opts) {
    var _temp = [];
    for (var k in opts) {
      _temp.push('&' + k + '=' + opts[k]);
    }
    return _temp.join('');
  };

  /**
   * define MongoReader
   * @constructor
   */
  var MongoReader = function () {
    this.requestURL = ''; // like '/mongo/:db/:collection/'
    this.options = {
      skip: 0,
      batch_size:50,
      limit:50
    };
  };

  /**
   * initial MongoReader setting
   * @param requestURL -> requestURL like '/mongo/:db/:collection/'
   * @param opt -> some options like '{skip:10, limit:10}'
   */
  MongoReader.prototype.init = function (requestURL, opt) {
    requestURL && (this.requestURL = requestURL);
    opt && (this.options = opt);
  };

  /**
   * get mongodb data count with criteria
   * @param criteria -> json object like "{category:'Apple'}"
   * @param callback
   */
  MongoReader.prototype.count = function (criteria, callback) {
    this.execCommand('get', this.requestURL, '_count', criteria, undefined, callback);
  };

  /**
   * get mongodb data with criteria and sort
   * @param criteria -> json object like "{id:'1'}"
   * @param sort -> json object like '{serverTime:-1}'
   * @param callback
   */
  MongoReader.prototype.find = function (criteria, sort, callback) {
    this.execCommand('get', this.requestURL, '_find', criteria, sort, callback);
  };

  /**
   * get mongodb data with criteria and sort
   * @param criteria -> json object like "{id:'1'}"
   * @param sort -> json object like '{serverTime:-1}'
   * @param callback
   */
  MongoReader.prototype.export = function (criteria, sort, projection) {
    window.location = this.requestURL +
      'exportcsv/?criteria=' +
      encodeURIComponent(jsonToString(criteria)) +
      '&sort=' +
      encodeURIComponent(jsonToString(sort)) +
      '&projection=' + encodeURIComponent(jsonToString(projection));

  };

  /**
   * send some others command to mongoreader server,this is a Low-Level function.
   * @param type -> http method type
   * @param url  -> request url
   * @param cmd  -> mongoreader command like '_count/_find'
   * @param criteria -> json object
   * @param sort -> json object
   * @param callback
   */
  MongoReader.prototype.execCommand = function (type, url, cmd, criteria, sort, callback) {
    sendAjax(type, mixURL(url, cmd, criteria, sort, this.options), callback);
  };


  root.MongoReader = new MongoReader(); //export to the window object

})(window);


$(function () {

  var pageCounts = 1;
  var $tbl = $('#tbl_mongo');
  var $page = $('#ul_page');
  var $error = $('#error_msg');
  var CacheData = [];
  var batch_size = rowcount || 50;

  var RenderTable = function () {
    Mustache.tags = ["<%", "%>"];
    Mustache.parse($('#theadTpl').html());
    Mustache.parse($('#tableTpl').html());
    Mustache.parse($('#pageTpl').html());
    Mustache.parse($('#totalTpl').html());
    this.columnsArr = columns.split(',');
    this.columns_trans = (typeof columns_trans === 'string' ? $.parseJSON(columns_trans) : columns_trans);
    this.detailData = {};
  };

  RenderTable.prototype.getCount = function () {
    MongoReader.count(criteria, function (returnedData) {
      if (!returnedData.ok) {
        $error.html('get count error! ' + returnedData.error || '');
        return;
      } else {
        $error.empty();
      }
      $('#span_total').html(Mustache.render($('#totalTpl').html(), {
        total: function () {
          return returnedData.count;
        }
      }));
      $('body').trigger('getCountEvent');
      Pagination.pagination(returnedData.count);
    });
  };

  /**
   * render table head
   */
  RenderTable.prototype.renderThead = function () {
    var renderTableObj = this;
    if (renderTableObj.columnsArr.length <= 0) {
      return;
    }
    var _tplData = [];
    $.each(renderTableObj.columnsArr, function (key, value) {
      _tplData.push({thead: (renderTableObj.columns_trans.hasOwnProperty(value) ? renderTableObj.columns_trans[value] : value)});
    });
    _tplData.push({thead: ''});

    $tbl.find('thead').html(Mustache.render($('#theadTpl').html(), {loop: _tplData}));
  };

  /**
   * get mongodb Data from mongo reader
   */
  RenderTable.prototype.getMongoData = function (currentPage) {
    var renderTableObj = this;
    var _skipVal = 0;
    if (currentPage > 1) {
      _skipVal = rowcount * (currentPage - 1);
    }

    //#todo cache data
    MongoReader.options.skip = _skipVal;
    MongoReader.find(criteria, sort, function (returnedData) {
      if (!returnedData.ok) {
        $error.html('get data error! ' + returnedData.error || '');
        return;
      } else {
        $error.empty();
      }
      CacheData = returnedData.results;
      analyzeData(CacheData, returnedData.span || 0, renderTableObj);
      $('body').trigger('getMongoDataEvent');
    });
  };

  var analyzeData = function (data, timespan, renderTableObj) {
    var _tplData = [];
    $.each(data, function (idx, obj) {
      var _tds = [],_id;
      if (typeof obj._id === 'object'){
        _id = obj._id.$oid;
      } else {
        _id = obj._id;
      }

      renderTableObj.detailData[_id] = obj;

      $.each(renderTableObj.columnsArr, function (k, v) {
        var _tmp = obj[v];
        if (window.hasOwnProperty(v + '_process')) {
          /*jslint evil: true */
          _tmp = eval(v + '_process')(_tmp, obj);
        }
        _tds.push({content: _tmp});
      });
      _tds.push({detail: _id});
      _tplData.push({tds: _tds});
    });
    renderTableObj.renderThead();
    $tbl.find('tbody').html(Mustache.render($('#tableTpl').html(), {
      loop: [{
        hasdata: _tplData,
        len: renderTableObj.columnsArr.length + 1
      }]
    }));
    $('#query_time').html(timespan + 's');
  };

  /**
   * simple detail implement
   * @param e
   */
  RenderTable.prototype.detailClickFun = function (e) {
    e.preventDefault();
    var detailData = renderTable.detailData[$(this).attr('data-id')];
    var _detailArr = [];
    $.each(detailData, function (k, v) {
      if (window.hasOwnProperty(k + '_process')) {
        _detailArr.push((renderTable.columns_trans.hasOwnProperty(k) ? renderTable.columns_trans[k] : k) + ':' + eval(k + '_process')(v, detailData) + '\n');
      } else {
        _detailArr.push((renderTable.columns_trans.hasOwnProperty(k) ? renderTable.columns_trans[k] : k) + ':' + v + '\n');
      }
    });
    alert(_detailArr.join(''));
  };

  /**
   * export to csv
   * @param projection: csv columns header
   */
  RenderTable.prototype.exportFun = function (projection) {
    MongoReader.export(criteria, sort, (projection || this.columns_trans));
  };


  var Pagination = function () {
  };

  /**
   * do paginate
   * @param count
   */
  Pagination.pagination = function (count) {
    $page.empty();
    if (count > 0 && count !== undefined) {
      pageCounts = Math.ceil(count / rowcount);
      Pagination.initPageNumber(pageCounts, 1);
    }
    $page.unbind('click').on('click', 'a', Pagination.pageClick);
  };

  /**
   * click page link to pagination
   */
  Pagination.pageClick = function (e) {
    e.preventDefault();
    var currentPage = $(this).parent().attr('id');

    if($(this).parent().hasClass('disabled')){
      return;
    }
    //special Prev or Next button
    var activePage = $('.pagination .active').text();
    if (currentPage === "li_prev") {
      currentPage = (parseInt(activePage) - 1 < 1) ? 1 : parseInt(activePage) - 1;
    } else if (currentPage === "li_next") {
      currentPage = (parseInt(activePage) + 1 > parseInt(pageCounts)) ? parseInt(pageCounts) : parseInt(activePage) + 1;
    }
    renderTable.getMongoData(currentPage);
    Pagination.initPageNumber(pageCounts, currentPage);
    $('body').trigger('pageClickEvent');
  };

  /**
   * init page btns or change page btns
   * @param pageNumber
   * @param currentPage
   */
  Pagination.initPageNumber = function (pageNumber, currentPage) {

    var _pageData4tpl = [];

    if (typeof currentPage != "number")
      currentPage = parseInt(currentPage);

    if (pageNumber < 5) {
      _pageData4tpl.length = 0;
      for (var n = 1; _pageData4tpl.push(n++) < pageNumber;);
    } else if (currentPage <= 3) {
      for (var i = 1; _pageData4tpl.push(i++) < 5;);
    } else if (pageNumber - currentPage < 3) {
      for (var j = (pageNumber - 4); j <= pageNumber; j++) {
        _pageData4tpl.push(j);
      }
    } else {
      _pageData4tpl = [currentPage - 2, currentPage - 1, currentPage, currentPage + 1, currentPage + 2];
    }

    var _lis = $page.find('li[id!="li_prev"][id!="li_next"]');
    if (_lis.length > 0) {
      $page.find('li').removeClass('active disabled');
      $.each(_lis, function (idx, li) {
        $(li).attr('id', _pageData4tpl[idx]).find('a').text(_pageData4tpl[idx]);
      });
    } else {
      $page.empty();
      $page.html(Mustache.render($('#pageTpl').html(), {loop: _pageData4tpl}));
    }

    var $prev = $('#li_prev');
    var $next = $('#li_next');
    var $currentLi = $('#' + currentPage);

    if (currentPage <= 3) {
      $currentLi.addClass('active');
    } else if (pageNumber - currentPage < 3) {
      $currentLi.addClass('active');
    } else {
      $currentLi.addClass('active');
    }

    if (+pageNumber === 1) {
      $prev.addClass('disabled');
      $next.addClass('disabled');
    } else if (+currentPage === 1) {
      $prev.addClass('disabled');
    } else if (+currentPage === +pageNumber) {
      $next.addClass('disabled');
    }
  };

  var renderTable = new RenderTable();
  window.RenderTable = renderTable;
  MongoReader.init(requestURL, {skip: 0, limit: batch_size, batch_size: batch_size});
});

var NEWSFEED_MAX = 0;
var NEWSFEED_MIN = 0;

function get_newsfeed(id_int, mode) {
  $.ajax({
    url: '/newsfeed/?id_int='+id_int,
    async: false,
    type: 'GET',
    dataType: 'html',
    success: function (data) {
      $obj = $('.content');
      if (mode === 'append') {
        $obj.append(data);
      } else if (mode === 'prepend') {
        $obj.prepend(data);
      } else {
        $obj.html(data);
      }
    }
  });

  var $newsfeed = $('.newsfeed');
  NEWSFEED_MAX = $newsfeed.first().data('id-int');
  NEWSFEED_MIN = $newsfeed.last().data('id-int');
}

function ajax_call(url, selector, mode) {
  $.get(url,
    {},
    function (data) {
      $obj = $(selector);
      if (mode === 'append') {
        $obj.append(data);
      } else if (mode === 'prepend') {
        $obj.prepend(data);
      } else {
        $obj.html(data);
      }
    },
  'html');
}

$(document).ready(function() {
  var $body = $('body');

  $body.on('click', 'a', function() {
    $anchor = $(this);
    var url = $anchor.attr('href');
    var dom = $anchor.data('ajax');
    dom = dom ? dom : '';

    if (dom.length > 0) {
      ajax_call(url, dom, 'replace');
      return false;
    } else {
      return true;
    }

  });

  $('a.playlist-swc').click(function() {
    var flag = $body.attr('data-playlist') === 'on' ? 'off' : 'on';
    $body.attr('data-playlist', flag);
    return false;
  });
});
var NEWSFEED_MAX = 0;
var NEWSFEED_MIN = 0;

function retrieve_hash_page() {
  var url = window.location.hash ? window.location.hash.substring(1) : '/';
  ajax_call(url, '.content', 'replace');
}

function get_newsfeed(id_int, mode) {
  var url = '/newsfeed/?id_int='+id_int;
  if (mode === 'prepend') {
    url = url + '&mode=new';
  } else if (mode === 'append') {
    url = url + '&mode=old';
  }

  ajax_call(url, '.content-middle', mode);

  var $newsfeed = $('.newsfeed');
  NEWSFEED_MAX = $newsfeed.first().data('id-int');
  NEWSFEED_MIN = $newsfeed.last().data('id-int');
}

function ajax_call(url, selector, mode) {
  $.ajax({
    url: url,
    async: false,
    type: 'GET',
    dataType: 'html',
    success: function (data) {
      $obj = $(selector);
      if (mode === 'append') {
        $obj.append(data);
      } else if (mode === 'prepend') {
        $obj.prepend(data);
      } else {
        $obj.html(data);
      }
    }
  });
}

$(document).ready(function() {
  var $body = $('body');

  // initial page load
  var hash = window.location.hash;
  if (hash) retrieve_hash_page();

  // hash change
  $(window).on('hashchange', retrieve_hash_page);

  // load newsfeed
  $body.on('click', 'a.load-newsfeed', function() {
    var dir = $(this).data('dir');
    if (dir === 'new') {
      get_newsfeed(NEWSFEED_MAX, 'prepend');
    } else if (dir === 'old') {
      get_newsfeed(NEWSFEED_MIN, 'append');
    }
    return false;
  });

  // toggle playlist
  $body.on('click', 'a.playlist-swc', function() {
    var flag = $body.attr('data-playlist') === 'on' ? 'off' : 'on';
    $body.attr('data-playlist', flag);
    return false;
  });
});
var NEWSFEED_MAX = 0;
var NEWSFEED_MIN = 0;
var PLAY_STATUS = 'stop';

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
  var NEWSFEED_MAX_NEW = parseInt($newsfeed.first().data('id-int'));
  var NEWSFEED_MIN_NEW = parseInt($newsfeed.last().data('id-int'));

  if (NEWSFEED_MAX_NEW === NEWSFEED_MAX && mode === 'prepend') alert('No more recent feed!');
  NEWSFEED_MAX = NEWSFEED_MAX_NEW;

  if (NEWSFEED_MIN_NEW === NEWSFEED_MIN && mode === 'append') alert('No more old feed!');
  NEWSFEED_MIN = NEWSFEED_MIN_NEW;
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
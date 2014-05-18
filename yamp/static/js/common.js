$(document).ready(function() {
  var $body = $('body');
  $('a.playlist-swc').click(function() {
    var flag = $body.attr('data-playlist') === 'on' ? 'off' : 'on';
    $body.attr('data-playlist', flag);
    return false;
  });
});
function Playlist(player) {
  this.player = player;
  this.playerObj = null;
  this.basket = [];
  this.activeIdx = 0;

  // Wrapper Method
  this.pipe = function(funcname, after) {
    this[funcname]();

    if (typeof after === "function") after();
  };

  // Methods
  this.play = function() {
    if (this.basket.length > 0) {
      var item = this.basket[this.activeIdx];
      this.destroyPlayer();

      if (item.media_type === "youtube") {
        this.playerObj = new YT.Player('player', {
          height: '100%',
          width: '100%',
          videoId: item.id_str,
          suggestedQuality: 'default',
          events: {
            'onReady': onReady,
            'onStateChange': onStateChange,
            'onError': onError
          }
        });

        function onReady(event) {
          event.target.playVideo();
        }

        function onStateChange(event) {
          if (event.data == YT.PlayerState.ENDED) {
            youtube_skip();
          }
        }

        function onError(event) {
          youtube_skip();
        }
      }
    }
  };
  this.pause = function() {};

  this.movePosition = function(idx) {
    this.activeIdx = idx;
  };

  this.next = function() {
    var next = this.activeIdx + 1 == this.basket.length ? 0 : this.activeIdx + 1;
    this.movePosition(next);
    this.play();
  };

  this.prev = function() {
    var prev = this.activeIdx == 0 ? this.basket.length - 1 : this.activeIdx - 1;
    this.movePosition(prev);
    this.play();
  };

  this.jump = function(idx) {
    this.movePosition(idx);
    this.play();
  };

  this.destroyPlayer = function() {
    if (this.playerObj !== null && 'destroy' in this.playerObj) {
      this.playerObj.destroy();
    } else {
      this.playerObj = null;
      $(player).replaceWith('<div id="player" class="player"></div>');
    }
  }

  this.shuffle = function () {
    var o = this.basket;
    // from: http://stackoverflow.com/a/6274381/2198378
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    this.basket = o;
  };
  this.clear = function() {
    this.basket = [];
  };

  this.exportData = function() {
    return this.basket;
  };
  this.importData = function(data) {
    this.basket = data;
  };
}

function youtube_skip() {
  PLAYLIST.next();
}
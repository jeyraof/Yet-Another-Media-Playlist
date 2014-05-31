function PopcornBasket(player) {
  this.player = player;
  this.basket = [];
  this.activeIdx = 0;

  // Wrapper Method
  this.pipe = function(funcname, after) {
    this[funcname]();

    if (typeof after === "function") after();
  };

  // Methods
  this.play = function() {};
  this.pause = function() {};

  this.next = function() {};
  this.prev = function() {};

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
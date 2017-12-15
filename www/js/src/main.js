'use strict';

var Navigo = require('navigo');
var HomeView = require('./views/home.js');

(function() {

  function main() {
    var routes = {
      '*': HomeView
    };

    new Navigo(null, true, '#!')
      .on(routes)
      .resolve();
  }

  main();
}());

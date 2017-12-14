var navigo = require('navigo');
var homeview = require('./views/home.js');

function main() {
  var routes = {
    '*': homeview
  };

  new navigo(null, true, '#!')
    .on(routes)
    .resolve();
}

main();

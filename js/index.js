require('angular/angular');

require('./services');
require('./filters');

angular.module('index', ['index.filters', 'index.services'])
  .config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {templateUrl: 'templates/home.html'});
    $routeProvider.when('/list', {templateUrl: 'templates/list.html'});
    $routeProvider.when('/show', {templateUrl: 'templates/show.html'});
    $routeProvider.otherwise({redirectTo: '/'});
  }]);

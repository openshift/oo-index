require('./angular-1.29.min.js');
require('./angular-route-1.29.js');
require('./ui-bootstrap-tpls-0.10.0.min.js');

require('./services');
require('./filters');

window.HelloController = function($scope) {
  $scope.dude = 'AngularJS';
  $scope.index = require('../quickstart.json');
};

var ListCtrl = function ($scope) {
  $scope.shopping = {
    list: ['Milk', 'Bread', 'Biscuits']
  };
};

angular.module('appindex', ['ngRoute']);

//angular.module('appindex', ['appindex.filters', 'appindex.services'])
//  .config(['$routeProvider', function($routeProvider) {
//    $routeProvider.when('/', {templateUrl: 'templates/home.html'});
//    $routeProvider.when('/list', {templateUrl: 'templates/list.html'});
//    $routeProvider.when('/show', {templateUrl: 'templates/show.html'});
//    $routeProvider.otherwise({redirectTo: '/'});
//  }]);

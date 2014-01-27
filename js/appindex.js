require('./vendor/angular-1.29.min.js');
require('./vendor/angular-route-1.29.js');
require('./vendor/ui-bootstrap-tpls-0.10.0.min.js');

require('./services/services');
require('./filters');

/* Appindex */

angular.module('appindex', ['ngRoute'])

.config(function($routeProvider) {
  $routeProvider
    .when('/', {
      controller: 'HomeController',
      templateUrl: 'templates/home.html'
    })
    .when('/add', {
      controller:'ProjectController',
      templateUrl:'templates/project/add.html'
    })
    .otherwise({
      redirectTo:'/'
    });
})

.controller('HomeController', function($scope) {
})

.controller('ProjectController', function($scope) {
});

//angular.module('appindex', ['appindex.filters', 'appindex.services'])
//  .config(['$routeProvider', function($routeProvider) {
//    $routeProvider.when('/', {templateUrl: 'templates/home.html'});
//    $routeProvider.when('/list', {templateUrl: 'templates/list.html'});
//    $routeProvider.when('/show', {templateUrl: 'templates/show.html'});
//    $routeProvider.otherwise({redirectTo: '/'});
//  }]);
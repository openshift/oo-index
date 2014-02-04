'use strict';

require('./vendor/angular-1.29.min.js');
require('./vendor/angular-route-1.29.js');
require('./vendor/ui-bootstrap-tpls-0.10.0.min.js');
require('./vendor/select2.js');

/*
 * Services
 */ 
require('./services');

/*
 * Filters
 */
require('./filters');

/*
 * Controllers
 */ 
angular.module('ooindex.controllers', []);

require('./controllers/home.js');
require('./controllers/resource.js');
require('./controllers/search.js');

/*
 * Appindex
 */
angular.module('ooindex', ['ngRoute', 'ooindex.controllers', 'ooindex.services', 'ooindex.filters'])

  /*
   * Routes
   */
  .config(function($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'templates/home.html'
      })
      .when('/search', {
        templateUrl: 'templates/search.html'
      })
      .when('/add', {
        templateUrl:'templates/resource/add.html'
      })
      .otherwise({
        redirectTo:'/'
      });
  });

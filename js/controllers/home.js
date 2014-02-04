/*
 * Home Controller
 */
angular.module('ooindex.controllers')

  .controller('HomeController', function($scope) {

    $scope.signin = function() { };
    $scope.signout = function() { };

    $scope.search = function() {
      search();
    };

    // $scope.index = require('../quickstart.json'); // Load quickstart

  });


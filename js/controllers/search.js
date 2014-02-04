/*
 * Search Controller
 */
angular.module('ooindex.controllers')

  .controller('SearchController', function($scope) {

    $scope.search = function() {
      search();
    };

  });
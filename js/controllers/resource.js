/*
 * Resource Controller
 */
angular.module('ooindex.controllers')

  .controller('ResourceController', function($scope) {
    $scope.resource = {};

  	/*
  	 *
  	 */
  	$scope.add = function() {
  		console.log('Resource add');
  	};

  	/*
  	 *
  	 */
  	$scope.cartridges = function() {
  		console.log('Resource cartridges');
  	};

  	/*
  	 *
  	 */
  	$scope.repositories = function() {
  		console.log('Resource repositories');
  	};

    /**
     * Resource values
     */
    $scope.resource.username = 'Nagib';
    $scope.resource.repository = null;
    $scope.resource.name = null;
    $scope.resource.cartridges = [];

    $scope.select2Options = {
      'multiple': true,
      'simple_tags': true,
      'tags': ['tag1', 'tag2', 'tag3', 'tag4']  // Can be empty list.
    };    

  });

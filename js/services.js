/**
 * Services
 */
angular.module('ooindex.services', [])
  
  /* Authentication */

  .factory('authenticate', function ($scope, $q, $window) {
    return {
      request: function (config) {
        config.headers = config.headers || {};

        if ($window.sessionStorage.token) {
          config.headers.Authorization = 'Bearer ' + $window.sessionStorage.token;
        }
        
        return config;
      },
      response: function (response) {
        if (response.status === 401) {
          // handle the case where the user is not authenticated
        }
        return response || $q.when(response);
      }
    };
  })


  /* Search */

  .factory('search', function ($scope) {
    return function() {
      console.log('search');      
    };
  });
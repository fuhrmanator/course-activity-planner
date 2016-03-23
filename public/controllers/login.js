var controllers = angular.module('app.controllers.LoginController', ['satellizer']);


controllers.controller('LoginController', function($scope, $location, $auth, $http) {
    $scope.authenticate = function() {
      $auth.authenticate('google')
        .then(function() {
          $http.get('/api/me')
              .success(function() {
                  $location.path('/');
              })
              .error(function(err, status) {
                  console.log(err, status);
              });
        })
        .catch(function(error) {
          if (error.error) {
            // Popup error - invalid redirect_uri, pressed cancel button, etc.
            console.log(error.error);
          } else if (error.data) {
            // HTTP response error from server
            console.log(error.data, error.status);
          } else {
            console.log(error);
          }
        });
    };
  });

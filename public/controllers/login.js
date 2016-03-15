var controllers = angular.module('app.controllers.LoginController', ['satellizer']);


controllers.controller('LoginController', function($scope, $location, $auth) {
    $scope.authenticate = function() {
      $auth.authenticate('google')
        .then(function() {
          console.log('yay');
          $location.path('/');
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

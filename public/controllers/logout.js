var controllers = angular.module('app.controllers.LogoutController', []);

controllers.controller('LogoutController', function($location, $auth) {
  if (!$auth.isAuthenticated()) {
    return;
  }
  $auth.logout()
  .then(function() {
    $location.path('/login');
  });
});

angular.module('app', [
  'ngRoute',
  'app.controllers.Index',
]).config(['$routeProvider', '$httpProvider', function($routeProvider) {
    $routeProvider.when('/', {templateUrl: 'partials/index.html', controller: 'Index'});
    $routeProvider.otherwise({redirectTo: '/'});
  }]);

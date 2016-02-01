angular.module('app', [
  'ngRoute',
  'app.controllers.IndexController',
  'app.controllers.PlanController',
]).config(['$routeProvider', '$httpProvider', function($routeProvider) {
    $routeProvider.when('/', {templateUrl: 'partials/index.html', controller: 'IndexController'});
    $routeProvider.when('/plan/:uuid', {templateUrl: 'partials/plan.html', controller: 'PlanController'});
    $routeProvider.otherwise({redirectTo: '/'});
  }]);

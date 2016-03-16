angular.module('app', [
  'ngRoute',
  'angularMoment',
  'ui.bootstrap',
  'satellizer',
  'app.controllers.IndexController',
  'app.controllers.LoginController',
  'app.controllers.PlanController',
]).config(function($routeProvider, $authProvider) {
    $routeProvider.when('/', {templateUrl: 'partials/index.html', controller: 'IndexController'});
    $routeProvider.when('/login', {templateUrl: 'partials/login.html', controller: 'LoginController'});
    $routeProvider.when('/plan/:uuid', {templateUrl: 'partials/plan.html', controller: 'PlanController'});
    $routeProvider.otherwise({redirectTo: '/'});
    $authProvider.google({
      clientId: '1050677302865-eee9484qm70v9eqju9vs92n56cane9p4.apps.googleusercontent.com',
      url: 'http://cap.logti.etsmtl.ca/api/auth/google',
      redirectUri: 'http://cap.logti.etsmtl.ca/api/auth/google'
    });
  });

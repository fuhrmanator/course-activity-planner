angular.module('app', [
  'ngRoute',
  'angularMoment',
  'ui.bootstrap',
  'satellizer',
  'ngFileSaver',
  'app.controllers.IndexController',
  'app.controllers.LoginController',
  'app.controllers.PlanController',
  'app.controllers.LogoutController',
]).config(function($routeProvider, $authProvider) {
    $routeProvider.when('/', {
      templateUrl: 'partials/index.html',
      controller: 'IndexController',
      resolve: {loginRequired: loginRequired}
    });

    $routeProvider.when('/about', {
      templateUrl: 'partials/about.html'
    });

    $routeProvider.when('/login', {
      templateUrl: 'partials/login.html',
      controller: 'LoginController',
      resolve: {skipIfLoggedIn: skipIfLoggedIn}
    });

    $routeProvider.when('/logout', {
      templateUrl: '',
      controller: 'LogoutController',
      resolve: {loginRequired: loginRequired}
    });

    $routeProvider.when('/plan/:uuid', {
      templateUrl: 'partials/plan.html',
      controller: 'PlanController',
      resolve: {loginRequired: loginRequired}
    });

    $routeProvider.otherwise({redirectTo: '/'});

    $authProvider.google({
      clientId: '1050677302865-eee9484qm70v9eqju9vs92n56cane9p4.apps.googleusercontent.com',
      url: 'http://cap.logti.etsmtl.ca/api/auth/google',
      redirectUri: 'http://cap.logti.etsmtl.ca/api/auth/google'
    });

    // The following functions are taken from https://github.com/sahat/satellizer/blob/master/examples/client/app.js
    function skipIfLoggedIn($q, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.reject();
      } else {
        deferred.resolve();
      }
      return deferred.promise;
    }

    function loginRequired($q, $location, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.resolve();
      } else {
        $location.path('/login');
      }
      return deferred.promise;
    }
  });

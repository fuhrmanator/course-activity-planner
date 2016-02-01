var controllers = angular.module('app.controllers.PlanController', ['ngFileUpload']);

controllers.controller('PlanController', function($scope, $http, $location, $routeParams) {
    $scope.uuid = $routeParams.uuid;
    console.log($scope.uuid);

    $scope.preview = function() {
        var data = {'planning' : $scope.planning_txt};

        $http.put('/api/planning/' + $scope.uuid, data)
            .success(function() {
                $scope.refresh();
            })
            .error(function(err, status) {
                console.log(err, status);
            });
    };

    $scope.refresh = function() {
        $http.get('/api/planning/preview/' + $scope.uuid)
            .success(function(data) {
                $scope.preview_txt = data;
            })
            .error(function(err, status) {
                console.log(err, status);
            });
    };

});

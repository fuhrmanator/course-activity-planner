var controllers = angular.module('app.controllers.PlanController', ['ngFileUpload']);

controllers.controller('PlanController', function($scope, $http, $location, $routeParams) {
    $scope.uuid = $routeParams.uuid;
    $scope.invKeys = ['Q', 'P', 'S', 'H'];
    $scope.previewKeys = ['Q', 'P', 'S', 'H'];
    $scope.alerts = [];

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.filterInventoryByKey = function (element) {
        return $scope.invSelected(element.key_str);
    };

    $scope.filterPreviewByKey = function (element) {
        return $scope.previewSelected(element.key_str);
    };

    $scope.toggleInventoryKey = function (key_str) {
        $scope.toggleKey(key_str, $scope.invKeys);
    };

    $scope.togglePreviewKey = function (key_str) {
        $scope.toggleKey(key_str, $scope.previewKeys);
    };

    $scope.toggleKey = function (key_str, keys) {
        var index = keys.indexOf(key_str);
        if (index === -1) {
            keys.push(key_str);
        } else {
            keys.splice(index, 1);
        }
    };

    $scope.invSelected = function (key_str) {
        return $scope.invKeys.indexOf(key_str) !== -1;
    };

    $scope.previewSelected = function (key_str) {
        return $scope.previewKeys.indexOf(key_str) !== -1;
    };

    $scope.submit = function() {
        var data = {'planning' : $scope.planning_txt};

        $http.put('/api/planning/' + $scope.uuid, data)
            .success(function() {
                $scope.refresh();
            })
            .error(function(err, status) {
                console.log(err, status);
            });
    };

    $scope.download = function() {
        window.open('/api/planning/'+ $scope.uuid + '/mbz', '_blank', '');
    };

    $scope.refresh = function() {
        $http.get('/api/planning/'+ $scope.uuid + '/')
            .success(function(data) {
                $scope.planning_txt = data.planning.planning_txt;
                $http.get('/api/planning/'+ $scope.uuid + '/preview')
                    .success(function(data) {
                        $scope.preview = data.preview;
                        $scope.inventory = data.inventory;
                        $scope.alerts = data.alerts;
                    })
                    .error(function(err, status) {
                        $scope.alerts = err.alerts;
                        console.log(err, status);
                    });
            })
            .error(function(err, status) {
                $scope.alerts = err.alerts;
                console.log(err, status);
        });
    };

    $scope.refresh();

});

var controllers = angular.module('app.controllers.PlanController', ['ngFileUpload']);

controllers.controller('PlanController', function($scope, $http, $location, $routeParams) {
    $scope.uuid = $routeParams.uuid;
    $scope.key_to_name = {'P': 'Practicas', 'S': 'Seminars', 'Q':'Quizzes', 'H': 'Homeworks', 'L':'Lessons', 'C': 'Choices', 'F': 'Feedbacks'};
    $scope.meetingsKeys = ['P', 'S'];
    $scope.activitiesKeys = ['Q', 'H', 'L', 'C', 'F'];
    $scope.previewKeys = $scope.meetingsKeys.concat($scope.activitiesKeys);
    $scope.keys = $scope.meetingsKeys.concat($scope.activitiesKeys);

    $scope.shownMeetingsKeys = $scope.meetingsKeys.slice(0);
    $scope.shownActivitiesKeys = $scope.activitiesKeys.slice(0);
    $scope.shownPreviewKeys = $scope.previewKeys.slice(0);
    $scope.alerts = [];

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.filterActivityByKey = function (element) {
        return $scope.activitySelected(element.key_str);
    };

    $scope.filterMeetingByKey = function (element) {
        return $scope.meetingSelected(element.key_str);
    };

    $scope.filterPreviewByKey = function (element) {
        return $scope.previewSelected(element.key_str);
    };

    $scope.toggleActivityKey = function (key_str) {
        $scope.toggleKey(key_str, $scope.shownActivitiesKeys);
    };

    $scope.toggleMeetingKey = function (key_str) {
        $scope.toggleKey(key_str, $scope.shownMeetingsKeys);
    };

    $scope.togglePreviewKey = function (key_str) {
        $scope.toggleKey(key_str, $scope.shownPreviewKeys);
    };

    $scope.toggleKey = function (key_str, key_set) {
        var index = key_set.indexOf(key_str);
        if (index === -1) {
            key_set.push(key_str);
        } else {
            key_set.splice(index, 1);
        }
    };

    $scope.activitySelected = function (key_str) {
        return $scope.isSelected(key_str, $scope.shownActivitiesKeys);
    };

    $scope.meetingSelected = function (key_str) {
        return $scope.isSelected(key_str, $scope.shownMeetingsKeys);
    };

    $scope.previewSelected = function (key_str) {
        return $scope.isSelected(key_str, $scope.shownPreviewKeys);
    };

    $scope.isSelected = function(key_str, key_set) {
        return key_set.indexOf(key_str) !== -1;
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
                        $scope.key_counts = {};

                        // Init key count dict with all keys value 0
                        for (var i = 0; i < $scope.keys.length; i++) {
                            var key = $scope.keys[i];
                            $scope.key_counts[key] = 0;
                        }

                        // Fill key count
                        for (var type in $scope.inventory) {
                            for (i = 0; i < $scope.inventory[type].length; i++) {
                                $scope.key_counts[$scope.inventory[type][i].key_str]++;
                            }
                        }
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

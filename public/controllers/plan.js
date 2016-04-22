var controllers = angular.module('app.controllers.PlanController', ['ngFileUpload']);

controllers.controller('PlanController', function($scope, $http, $location, $routeParams, FileSaver, Blob) {
    $scope.uuid = $routeParams.uuid;
    $scope.alerts = [];

    $http.get('/api/keys')
        .success(function(data) {
            $scope.key_to_name = data.names;
            $scope.meetingsKeys = data.associations.meetings;
            $scope.activitiesKeys = data.associations.activities;

            $scope.previewKeys = $scope.meetingsKeys.concat($scope.activitiesKeys).concat(data.associations.user);
            $scope.keys = $scope.meetingsKeys.concat($scope.activitiesKeys);

            $scope.shownMeetingsKeys = $scope.meetingsKeys.slice(0);
            $scope.shownActivitiesKeys = $scope.activitiesKeys.slice(0);
            $scope.shownPreviewKeys = $scope.previewKeys.slice(0);
        })
        .error(function(err, status) {
            console.log(err, status);
        });

    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.isMeeting = function (element) {
        var index = $scope.meetingsKeys.indexOf(element.key_str);
        return index !== -1;
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

    $scope.buildCondensedPreviewDict = function (elements) {
        var condensed = {};

        for (var i = 0; i < elements.length; i++) {
            var e = elements[i];
            var timestamp = e.timestamp;
            // If key is shown, add to condensed preview
            if ($scope.filterPreviewByKey(e)) {
                // Create empty array if undefined
                if (!(timestamp in condensed)) {
                    condensed[timestamp] = [];
                }
                condensed[timestamp].push(e);
            }
        }
        return condensed;
    };

    $scope.toggleActivityKey = function (key_str) {
        $scope.toggleKey(key_str, $scope.shownActivitiesKeys);
    };

    $scope.toggleMeetingKey = function (key_str) {
        $scope.toggleKey(key_str, $scope.shownMeetingsKeys);
    };

    $scope.togglePreviewKey = function (key_str) {
        $scope.toggleKey(key_str, $scope.shownPreviewKeys);
        $scope.condensedPreview = $scope.buildCondensedPreviewDict($scope.preview);
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

    $scope.get_preview = function() {
        $scope.refresh();
    };

    $scope.save = function (next_fn) {
        var data = {'planning' : $scope.planning_txt};

        $http.put('/api/planning/' + $scope.uuid, data)
            .success(function() {
                next_fn();
            })
            .error(function(err, status) {
                console.log(err, status);
            });
    };

    $scope.planets = function () {
        $http.get('/api/planning/' + $scope.uuid + '/planets')
            .success(function(data) {
                $scope.planets_str = data.planets;
            })
            .error(function(err, status) {
                console.log(err, status);
            });
    };

    $scope.download_mbz = function() {
        $http.get('/api/planning/' + $scope.uuid + '/mbz')
            .success(function(data) {
                var byteCharacters = atob(data.mbz_64);
                var byteNumbers = new Array(byteCharacters.length);
                for (var i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                var bytes = new Uint8Array(byteNumbers);
                var blob = new Blob([bytes], {type: "application/x-gzip"});
                FileSaver.saveAs(blob, 'updated.mbz');
            })
            .error(function(err, status) {
                console.log(err, status);
            });
    };

    $scope.refresh = function() {
        $http.get('/api/planning/'+ $scope.uuid)
            .success(function(data) {
                $scope.planning_txt = data.planning.planning_txt;
                $http.get('/api/planning/'+ $scope.uuid + '/preview')
                    .success(function(data) {
                        $scope.preview = data.preview;
                        $scope.inventory = data.inventory;
                        $scope.hasMoodle = data.inventory.activities.length !== 0;
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
                        // Build compact preview
                        $scope.condensedPreview = $scope.buildCondensedPreviewDict(data.preview);
                        if ($scope.planets_str) {
                            $scope.planets();
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

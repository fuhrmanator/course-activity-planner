var controllers = angular.module('app.controllers.IndexController', ['ngFileUpload']);

controllers.controller('IndexController', function($scope, $http, $location, Upload) {
    $scope.alerts = [];

    $scope.closeAlert = function(index) {
       $scope.alerts.splice(index, 1);
    };

    $scope.submit = function() {
      if ($scope.form.mbzFile.$valid && $scope.mbzFile) {
        $scope.upload($scope.mbzFile);
      }
    };

    $scope.get_epoch = function (date_str) {
      return Date.parse(date_str);
    };

    $scope.refresh = function() {
      $http.get('/api/planning/')
          .success(function(data) {
              $scope.plannings = data.plannings;
          })
          .error(function(err, status) {
              console.log(err, status);
          });
    };

    $scope.editPlanning = function(uuid) {
      $location.path('/plan/' + uuid);
    };

    $scope.deletePlanning = function(uuid) {
      $http.delete('/api/planning/' + uuid)
          .success(function() {
              $scope.refresh();
          })
          .error(function(err, status) {
              console.log(err, status);
          });
    };

    $scope.upload = function() {
      delete $scope.uploadSuccess;
      var payload = $scope.planning ? $scope.planning : {};

      if ($scope.mbzFile) {
        payload.mbz_file = $scope.mbzFile;
      }

      if ($scope.ics_url) {
        payload.ics_url = $scope.ics_url;
      } else if ($scope.icsFile) {
        payload.ics_file = $scope.icsFile;
      } else {
        console.log('error: no ics');
      }

      Upload.upload({
          url: '/api/planning',
          data: payload
      }).progress(function (evt) {
          $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
      }).success(function (data) {
          if (data.planning) {
            $location.path("/plan/" + data.planning.uuid);
          }else {
            $scope.alerts.push({msg: 'An error occurred while uploading your file.', type: 'danger'});
          }
          delete $scope.progress;
      }).error(function (data, status) {
          if (status === 413) {
              $scope.alerts.push({msg: 'Your file is too big !', type: 'danger'});
          } else {
              $scope.alerts.push({msg: 'An error occurred while uploading your file.', type: 'danger'});
          }
          delete $scope.mbzFile;
          delete $scope.progress;
      });
  };

  $scope.refresh();

});

var controllers = angular.module('app.controllers.IndexController', ['ngFileUpload']);

controllers.controller('IndexController', function($scope, $http, $location, Upload) {
    $scope.alerts = [];

    $scope.closeAlert = function(index) {
       $scope.alerts.splice(index, 1);
    };

    $scope.submit = function() {
      if ($scope.form.file.$valid && $scope.file) {
        $scope.upload($scope.file);
      }
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

    $scope.upload = function(file) {
      delete $scope.uploadSuccess;

      Upload.upload({
          url: '/api/planning',
          data: {file: file, 'ics_url': $scope.ics_url}
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
          delete $scope.file;
          delete $scope.progress;
      });
  };

  $scope.refresh();

});

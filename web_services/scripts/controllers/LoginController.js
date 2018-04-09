'use strict';
(function() {
	// This is now just a reference to "myModule" in app.js
	let app = angular.module('myModule');

	app.controller('LoginController', function( $http, $log, $location, $scope, validate) {
		console.log('in login controller');
		/* If the user is signed in, redirect them to /home */
		$scope.formData = {
			'email': null,
			'password': null,
		};

		/* Control the visibility of different error messages */
		$scope.notifications = {
			'invalid_credentials': false,
			'generic_error': false,
			'bad_request': false,
		};

		$scope.submitLogin = function() {
			console.log('Submitting login request');
			$http.post('api/user/login', $scope.formData)
				.success(function(data, status, headers, config) {
					$location.path('/home');
				})
			.error(function(data, status, header, config) {
				if (status === 401) {
					$scope.notifications.invalid_credentials = true;
				} else if (status === 400) {
					$scope.notifications.bad_request = true;
				} else {
					$scope.notifications.generic_error = true;
				}
			});
		};
	});
}());

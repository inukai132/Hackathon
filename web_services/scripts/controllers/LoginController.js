'use strict';
(function() {
	// This is now just a reference to "myModule" in app.js
	let app = angular.module('myModule');

	app.controller('LoginController', function( $http, $log, $location, $scope, validate) {
		/* If the user is signed in, redirect them to /home */
		validate_session((is_logged_in)=>{
			/* If the user is logged in, redirect to  home  */
			if (is_logged_in) {
				$location.path('/home');
			}
		});

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
			/* If the form values are valid */
			if ($scope.formData &&
					(null != $scope.formData.email) &&
					(null != $scope.formData.password)) {
				/* Make a request to the services to log in */
				$http.post('http://ec2-18-220-239-17.us-east-2.compute.amazonaws.com:5000/api/user/login', $scope.formData)
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
			}
		};

		$scope.register = function() {
			$location.path('/register');
		};

		function validate_session(callback) {
			$http.get('http://ec2-18-220-239-17.us-east-2.compute.amazonaws.com:5000/api/session/validate', $scope.formData)
				.success(function(data, status, headers, config) {
					console.log(status);
					console.log(data);
					callback(true);
				})
			.error(function(data, status, headers, config) {
				console.log(status);
				console.log(data);
				callback(false);
			});
		}
	});


	//  app.controller("LoginController", function ( $http, $log, $location, $scope, validate) {
	//      $scope.login = function (loginForm) {
	//          if(loginForm.$valid) {
	//            validate.login($scope.firstname);
	//        } else {alert("Please fill in login info!")}
	//      };
	//
	//      $scope.register = function () {
	//          $location.path('/register');
	//      };
	//
	//  });
}());

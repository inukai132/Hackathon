'use strict';
(function() {
	// This is now just a reference to "myModule" in app.js
	let app = angular.module('myModule');

	app.controller('homeController', function( $http, $log, $location, $scope, validate, $window) {
		// $scope.show_name = false;	// Don't show the person's name until it loads

		// Validate the user's session
		validate_session((is_logged_in, user_data)=>{
			/* If the user is not logged in, redirect to the login page*/
			if (!is_logged_in) {
				$location.path('/login');
			} else { // Otherwise, render the page normally
				// console.log(user_data);
				$scope.user_data = user_data.patient_data;

				$scope.username = document.cookie.split("=")[1];

				$('#table').bootstrapTable({});
				function doc(){
					console.log('doc here');
					 $('#table .personal1').show();
					 $('#table .personal2').show();
					 $('#table .personal3').hide();
					 $('#table .billing1').hide();
					 $('#table .billing2').hide();
					 $('#table .medical1').show();
					 $('#table .medical2').show();
				}
				function bill(){
					console.log('in bill');
					 $('#table .personal1').show();
					 $('#table .personal2').show();
					 $('#table .personal3').show();
					 $('#table .billing1').show();
					 $('#table .billing2').show();
					 $('#table .medical1').show();
					 $('#table .medical2').hide();
				}
				function intake(){
					 $('#table .personal1').show();
					 $('#table .personal2').show();
					 $('#table .personal3').show();
					 $('#table .billing1').show();
					 $('#table .billing2').hide();
					 $('#table .medical1').hide();
					 $('#table .medical2').hide();
				}
				function janitor(){
					 $('#table .personal1').show();
					 $('#table .personal2').hide();
					 $('#table .personal3').hide();
					 $('#table .billing1').hide();
					 $('#table .billing2').hide();
					 $('#table .medical1').hide();
					 $('#table .medical2').hide();

				}
				function load(){
					 $('#table').bootstrapTable("load",$scope.user_data);
					 switch($scope.username){
	 					case 'Dana':
	 						doc();
	 						break;
	 					case 'William':
	 						bill();
	 						break;
						case 'Inigo':
							intake();
							break;
						case 'Janet':
							janitor();
							break;
	 					default:
	 						break;
	 				}
					 // console.log($scope.user_data);
					 // console.log('here');
				}
			 $(document).ready(load());
			}
		});

		function validate_session(callback) {
			$http.post('/api/session/validate/')
				.success(function(data, status, headers, config) {
					// console.log('in update_session');
					// console.log(data);
					callback(true, data);
				})
			.error(function(data, status, headers, config) {
				callback(false);
			});
		}

		$scope.sign_in = function() {
			console.log('clicked sign in');
			$http.post('http://ec2-18-220-239-17.us-east-2.compute.amazonaws.com:5000/api/event/sign_in')
				.success(function(data, status, headers, config) {
					alert('Thanks for signing in, ' + $scope.full_name + '.');
				})
			.error(function(data, status, headers, config) {
				alert('Something went wrong');
			});
		};

		$scope.log_out = function() {
			$http.post('http://ec2-18-220-239-17.us-east-2.compute.amazonaws.com:5000/api/session/logout');
			$location.path('/login');
		};
	    //redirect to sharepoint that stores lecture content
	    $scope.redirect_lecture_content = function(){
	      $window.open('https://uflorida-my.sharepoint.com/personal/elan22_ufl_edu/_layouts/15/guestaccess.aspx?folderid=0d67d1c9bc1be4aa68ea7bd61d21b612a&authkey=AbD-gTKCDdCIpE8vtELGWzw', '_blank');
	    };
	    //redirect to googleForms that allows resume' uploads
	    $scope.redirect_update_resume = function(){
	      $window.open('https://docs.google.com/forms/d/e/1FAIpQLScP-7T3VGFAcgVOcr12ErLfM0qIh4P9YjaxvCE8dqxIQ2sxVQ/viewform', '_blank');
	    };
	    //redirect to ufsit.org/blog that allows member to see latest events
	    $scope.redirect_events_news = function(){
	      $window.open('http://ufsit.org/blog/', '_blank');
	    };


	});
}());

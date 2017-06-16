// AngularJS 1.x.x Simple Clock Widget
// Written by S. Carotenuto of StartupSolutions

"use strict";

angular.module("ui.clockwidget", []).component('clockwidget', {
    /*bindings: {
		label: '@',
		model: '='
    },*/
    controller: function($scope, $rootScope, $interval) {
		//
		$scope.dayNames = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];
		$scope.monthNames = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
		$scope.time = { hours: "00", minutes: ":00", date: "..."};
		//
		$scope.tick = function() {
			var currentTime = new Date();
			//console.log(currentTime);
			$scope.time.hours = ("00" + currentTime.getHours()).substr(-2, 2);
			var minutes = ":" + ("00" + currentTime.getMinutes()).substr(-2, 2);
			if(minutes != $scope.time.minutes)
				// fires event on minute change
				$rootScope.$broadcast('clockwidget', 'minutes-changed');
			$scope.time.minutes = minutes;
			$scope.time.dayname = $scope.dayNames[currentTime.getDay()];
			$scope.time.date    = currentTime.getDate() + " " + $scope.monthNames[currentTime.getMonth()] + " " + currentTime.getFullYear();
		}
		
		// Start the timer
		$interval($scope.tick, 1000);

    },
    template: [
		'<table class="clockwidget">',
			'<tr>',
				'<td><span class="clockwidget-hours">{{time.hours}}</span><span class="clockwidget-minutes">{{time.minutes}}</span></td>',
			'</tr>',
			'<tr>',
				'<td class="clockwidget-date">',
					'{{time.dayname}}&nbsp;{{time.date}}',
				'</td>',
			'</tr>',
		'</table>'

		/*'<table class="clockwidget">',
			'<tr>',
				'<td rowspan="2"><span class="clockwidget-hours">{{time.hours}}</span><span class="clockwidget-minutes">{{time.minutes}}</span></td>',
				'<td>{{time.dayname}}</td>',
			'</tr>',
			'<tr>',
				'<td>&nbsp;&nbsp;&nbsp;{{time.date}}</td>',
			'</tr>',
		'</table>'*/

		/*'<table class="clockwidget">',
			'<tr>',
				'<td class="clockwidget-hours">{{time.hours}}</td>',
				'<td class="clockwidget-minutes">{{time.minutes}}</td>',
			'</tr>',
			'<tr>',
				'<td colspan="2">{{time.dayname}}</td>',
			'</tr>',
			'<tr>',
				'<td colspan="2">{{time.date}}</td>',
			'</tr>',
		'</table>'*/
    ].join('')

});


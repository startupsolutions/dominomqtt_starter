ngApp.controller('DisplayCtrl', ['$scope', 'toastr',
    function($scope, toastr) {

        $scope.temperatures = null;
		$scope.warnings = [];
		$scope.alerts = [];
		$scope.garage_door_status = null;

		// ---------------------------------------------------------------------------------
		// websocket: incoming messages handlers
		//
		socket.on('FRONTEND/TEMPERATURE/UPDATE', function (data) {
			console.log("[websocket] - received:", data);
			payload = angular.fromJson(data.payload)
			console.log("[websocket] - payload:", payload);
			$scope.temperatures = payload.temperatures;
		});
		//
		socket.on('FRONTEND/EVENT/WARNING', function (data) {
			console.log("[websocket] - received:", data);
			toastr.warning(data.payload);
			var warning = { timestamp: new Date().toISOString(), message: data.payload }
			$scope.warnings.push(warning);
		});
		//
		socket.on('FRONTEND/EVENT/ALERT', function (data) {
			console.log("[websocket] - received:", data);
			payload = angular.fromJson(data.payload)
			console.log("[websocket] - payload:", payload);
			var message = "Detected human presence in areas: ";
			for (var i=0; i<payload.areas.length; i++) {
				message += payload.areas[i];
				message += " ";
				}
			toastr.error(message);
			var alert = { timestamp: new Date().toISOString(), message: message }
			$scope.alerts.push(alert);
		});
		//
		socket.on('FRONTEND/STATUS/UPDATE', function (data) {
			console.log("[websocket] - received:", data);
			payload = angular.fromJson(data.payload)
			console.log("[websocket] - payload:", payload);
			if(payload.class == 'action_done')
				if(payload.item == 'garage_door') {
					$scope.garage_door_status = payload.status.toUpperCase();
					toastr.info("Garage door is " + $scope.garage_door_status);
				}
		});
		//
		// ---------------------------------------------------------------------------------

		$scope.onOpenGarageDoorBtn = function() {
			socket.emit('json', { class: "user_request", data: 'garage_door_open' });
		}

		$scope.onCloseGarageDoorBtn = function() {
			socket.emit('json', { class: "user_request", data: 'garage_door_close' });
		}
		
    }
]);
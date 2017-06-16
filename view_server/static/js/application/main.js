// ----------------------------------------------------------------------------

var ngApp = angular.module('ngApp', ['ui.clockwidget', 'toastr']);


console.log('### Socket.io connection to ' + location.protocol + '//' + document.domain + ':' + location.port);
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


socket.on('connect', function() {
	socket.emit('debug', {data: 'Display unit connected!'});
});


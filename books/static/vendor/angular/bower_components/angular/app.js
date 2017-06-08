(function(angular) {
    'use strict';

var app = angular.module('MyApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

})(window.angular);
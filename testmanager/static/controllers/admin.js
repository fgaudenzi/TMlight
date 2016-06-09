var myApp = angular.module('myApp', ['']);



myApp.config(function(RestangularProvider) {
    var login = '',
        password = '',
        token = '';
    RestangularProvider.setDefaultHeaders({'Authorization': 'Basic ' + token});
});
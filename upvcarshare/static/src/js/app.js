import jQuery from 'jquery';
import Tether from 'tether';
import angular from 'angular';

// We define jQuery as global (using window object) and include Bootstrap
// JavaScript code. We use 'require' to avoid problems with npm bootstrap
// module.
window.$ = window.jQuery = jQuery;
window.Tether = Tether;
var bootstrap = require('bootstrap');


// General Angular 1.5 App
// -----------------------------------------------------------------------------
angular
  .module('upvcarshare', [])
  .config(['$httpProvider', '$interpolateProvider', ($httpProvider, $interpolateProvider) => {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.srfHeaderName = 'X-CSRFToken';
  }]);

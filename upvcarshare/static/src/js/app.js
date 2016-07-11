import jQuery from 'jquery';
import Tether from 'tether';

// We define jQuery as global (using window object) and include Bootstrap
// JavaScript code. We use 'require' to avoid problems with npm bootstrap
// module.
window.$ = window.jQuery = window.jquery = jQuery;
window.Tether = Tether;
var bootstrap = require('bootstrap');
require("fullcalendar");


// General Angular 1.5 App
// -----------------------------------------------------------------------------
import angular from 'angular';
import Common from './common';
import Messenger from './messenger';
import Journeys from './journeys';


angular
  .module('upvcarshare', [
    Common.name,
    Messenger.name,
    Journeys.name
  ])
  .config(['$httpProvider', '$interpolateProvider', ($httpProvider, $interpolateProvider) => {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  }]);

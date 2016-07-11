import angular from 'angular';
import PreventSubmit from './common.directive';


const common = angular
  .module('common', [])
  .directive('preventSubmit', PreventSubmit);


export default common;

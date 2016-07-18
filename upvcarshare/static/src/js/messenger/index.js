import angular from 'angular';
import 'angularjs-scroll-glue';
import 'angular-cookies';

import MessengerService from './messenger.service';
import MessageUserColor from './messenger.directive';
import {MessengerComponent, MessageListComponent, MessageFormComponent} from  './messenger.component';


// Messenger module
const messenger = angular
  .module('messenger', [
    'ngCookies',
    'luegg.directives'
  ])
  .service('MessengerService', MessengerService)
  .directive('userColor', MessageUserColor)
  .component('messenger', MessengerComponent)
  .component('messageList', MessageListComponent)
  .component('messageForm', MessageFormComponent);

export default messenger;

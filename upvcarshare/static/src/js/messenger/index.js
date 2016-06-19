import angular from 'angular';
import MessengerService from './messenger.service'
import {MessengerComponent, MessageListComponent, MessageFormComponent} from  './messenger.component';


// Messenger module
const messenger = angular
  .module('messenger', [])
  .service('MessengerService', MessengerService)
  .component('messenger', MessengerComponent)
  .component('messageList', MessageListComponent)
  .component('messageForm', MessageFormComponent);

export default messenger;

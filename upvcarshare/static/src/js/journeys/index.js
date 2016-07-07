import angular from 'angular';
import JourneyService from './journeys.service';
import {OriginDestinationSelectComponent, DatetimeComponent, CalendarComponent} from './journeys.component';

import 'angular-ui-bootstrap';
import 'bootstrap-ui-datetime-picker';
import 'angular-ui-calendar';


const journeys = angular
  .module('journeys', [
    'ui.bootstrap',
    'ui.bootstrap.datetimepicker',
    'ui.calendar'
  ])
  .service('JourneyService', JourneyService)
  .component('originDestinationSelect', OriginDestinationSelectComponent)
  .component('journeyDatetime', DatetimeComponent)
  .component('calendar', CalendarComponent);

export default journeys;

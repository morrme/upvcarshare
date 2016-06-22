import angular from 'angular';
import JourneyService from './journeys.service';
import {OriginDestinationSelectComponent, DatetimeComponent} from './journeys.component';

import 'angular-ui-bootstrap';
import 'bootstrap-ui-datetime-picker';


const journeys = angular
  .module('journeys', [
    'ui.bootstrap',
    'ui.bootstrap.datetimepicker'
  ])
  .service('JourneyService', JourneyService)
  .component('originDestinationSelect', OriginDestinationSelectComponent)
  .component('journeyDatetime', DatetimeComponent);

export default journeys;

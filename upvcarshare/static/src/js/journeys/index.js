import angular from 'angular';
import JourneyService from './journeys.service';
import {OriginDestinationSelectComponent, DatetimeComponent, CalendarComponent, CircleMapComponent} from './journeys.component';
import JourneyForm from './journey.directive';

import 'angular-ui-bootstrap';
import 'bootstrap-ui-datetime-picker';
import 'angular-ui-calendar';
import 'lodash';
import 'angular-simple-logger';
import 'angular-google-maps';


const journeys = angular
  .module('journeys', [
    'ui.bootstrap',
    'ui.bootstrap.datetimepicker',
    'ui.calendar',
    'uiGmapgoogle-maps'
  ])

  .service('JourneyService', JourneyService)

  .component('originDestinationSelect', OriginDestinationSelectComponent)
  .component('journeyDatetime', DatetimeComponent)
  .component('calendar', CalendarComponent)
  .component('circleMap', CircleMapComponent)

  .directive('journeyForm', JourneyForm)

  // Angular Google Maps
  .config(['uiGmapGoogleMapApiProvider', (uiGmapGoogleMapApiProvider) => {
    uiGmapGoogleMapApiProvider.configure({
      key: 'AIzaSyAUuXiJ-kthJMHdXerksxYbqIbrRFrVfG4',
      v: '3.24',
      libraries: 'geometry,visualization,places'
    });
  }]);


export default journeys;

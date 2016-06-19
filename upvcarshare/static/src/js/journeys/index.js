import angular from 'angular';
import JourneyService from './journeys.service';
import OriginDestinationSelectComponent from './journeys.component';

const journeys = angular
  .module('journeys', [])
  .service('JourneyService', JourneyService)
  .component('originDestinationSelect', OriginDestinationSelectComponent);

export default journeys;

// Component for select origin and destination of a journey.
import controller from './journeys.controller';


const OriginDestinationSelectComponent = {
  controller,
  templateUrl: "/partials/journeys/origin_destiny_select.html",
  bindings: {
    originField: '@',
    destinyField: '@'
  }
};


export default OriginDestinationSelectComponent;

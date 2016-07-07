// Component for select origin and destination of a journey.
import {OriginDestinationSelectController, DatetimeController, CalendarController} from './journeys.controller';


const OriginDestinationSelectComponent = {
  controller: OriginDestinationSelectController,
  templateUrl: "/partials/journeys/origin_destiny_select.html",
  bindings: {
    originField: '@',
    originFieldId: '@',
    destinyField: '@',
    destinyFieldId: '@'
  }
};


const DatetimeComponent = {
  controller: DatetimeController,
  templateUrl: "/partials/journeys/datetime.html",
  bindings: {
    fieldName: '@',
    fieldId: '@'
  }
};


const CalendarComponent = {
  controller: CalendarController,
  templateUrl: "/partials/journeys/calendar.html",
  bindings: {
    userId: '@'
  }
};


export {OriginDestinationSelectComponent, DatetimeComponent, CalendarComponent};

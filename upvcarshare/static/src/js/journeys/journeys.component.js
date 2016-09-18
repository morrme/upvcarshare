// Component for select origin and destination of a journey.
import {OriginDestinationSelectController, DatetimeController, CalendarController, CircleMapController}
  from './journeys.controller';


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
    value: '@',
    fieldName: '@',
    fieldId: '@',
    overrideValue: '<',
    onUpdate: '&'
  }
};


const CalendarComponent = {
  controller: CalendarController,
  templateUrl: "/partials/journeys/calendar.html",
  bindings: {
    userId: '@'
  }
};


const CircleMapComponent = {
  controller: CircleMapController,
  templateUrl: "/partials/journeys/circle_map.html",
  bindings: {
    radiusValue: '@',
    radiusField: '@',
    radiusFieldId: '@',
    positionValue: '@',
    positionField: '@',
    positionFieldId: '@'
  }
};

export {OriginDestinationSelectComponent, DatetimeComponent, CalendarComponent, CircleMapComponent};

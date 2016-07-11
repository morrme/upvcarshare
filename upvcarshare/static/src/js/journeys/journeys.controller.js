import moment from 'moment';


class OriginDestinationSelectController {

  constructor($scope, JourneyService) {
    this.$scope = $scope;
    this.journeyService = JourneyService;
  }

  $onInit() {
    this.residences = [];
    this.campus = [];

    this.originOptions = [];
    this.originSelected = null;
    this.originFieldValue = "";

    this.destinyOptions = [];
    this.destinySelected = null;
    this.destinyFieldValue = "";

    Promise.all(this.loadData()).then( () => {
      this.$scope.$apply( () => {
        this.buildOriginOptions();
      });
    });

  }

  // Load data
  loadData() {
    return [
      // Load residences
      this.journeyService.getResidences().then( response => {
        this.residences = response.results;
      }),
      // Load campus
      this.journeyService.getCampus().then( response => {
        this.campus = response.results;
      })
    ];
  }

  // Builds the list of available options for origin
  buildOriginOptions() {
    if (this.originSelected === null) {
      // If there is not origin, destination is disabled...
      this.originOptions = this.residences.concat(this.campus);
    }
  }

  changeOrigin() {
    if (this.campus.indexOf(this.originSelected) != -1) {
      this.originFieldValue = "campus:" + this.originSelected.id;
    } else if (this.residences.indexOf(this.originSelected) != -1) {
      this.originFieldValue = "residence:" + this.originSelected.id;
    }
    this.buildDestinyOptions();
  }

  changeDestiny() {
    if (this.campus.indexOf(this.destinySelected) != -1) {
      this.destinyFieldValue = "campus:" + this.destinySelected.id;
    } else if (this.residences.indexOf(this.destinySelected) != -1) {
      this.destinyFieldValue = "residence:" + this.destinySelected.id;
    }
  }

  // Builds the list of available options for destiny
  buildDestinyOptions() {
    if (this.campus.indexOf(this.originSelected) != -1) {
      // If there is selected a residence, only options for destiny are campus
      this.destinyOptions = this.residences;
    } else if (this.residences.indexOf(this.originSelected) != -1) {
      // If there is selected a residence, only options for destiny are residendes
      this.destinyOptions = this.campus;
    }
    if (this.destinyOptions.length > 0) {
      this.destinySelected = this.destinyOptions[0];
      this.changeDestiny();
    }
  }

}

OriginDestinationSelectController.$inject = ['$scope', 'JourneyService'];


class DatetimeController {

  constructor() {
    this.picker = {
      date: new Date(),
      open: false,
      dateOptions: {
        startingDay: 1
      },
      timeOptions: {
        showMeridian: false
      }
    };
  }

  openCalendar($event) {
    this.picker.open = true;
  }

}


class CalendarController {

  constructor($scope, JourneyService, uiCalendarConfig) {
    this.journeyService = JourneyService;
    this.$scope = $scope;
    this.uiCalendarConfig = uiCalendarConfig;
  }

  processDataEvent(dataEvent) {
    var event = {
      "title": dataEvent.title,
      "start": moment(dataEvent.start).toDate(),
      "end": moment(dataEvent.end).toDate(),
      "url": `/journeys/${dataEvent.id}/`
    };
    if (dataEvent.user.id == parseInt(this.userId)) {
      if (dataEvent.driver !== null) {
        this.journeysCreatedDriver.events.push(event);
      } else {
        this.journeysCreatedNoDriver.events.push(event);
      }
    } else {
      this.journeysJoined.events.push(event);
    }
  }

  // Load events
  loadEvents(url=null, mode=null) {
    this.loadingEvents = true;
    if (url === null) {
        this.journeyService.getJourneysJoined().then( (response) => {
        response.results.forEach((dataEvent) => {
          this.processDataEvent(dataEvent)
        });
        if (response.next !== null) {
          this.loadEvents(response.next, "joined");
        } else {
          this.loadingEvents = false;
          this.eventSources.push(this.journeysJoined);
        }
      });
      this.journeyService.getJourneysOwned().then( (response) => {
        response.results.forEach((dataEvent) => {
          this.processDataEvent(dataEvent)
        });
        if (response.next !== null) {
          this.loadEvents(response.next, "created");
        } else {
          this.loadingEvents = false;
          this.eventSources.push(this.journeysCreatedDriver);
          this.eventSources.push(this.journeysCreatedNoDriver);
        }
      });
    } else {
      this.journeyService.getByUrl(url).then( (response) => {
        response.results.forEach((dataEvent) => {
          this.processDataEvent(dataEvent)
        });
        if (response.next !== null) {
          this.loadEvents(response.next, mode);
        } else {
          this.loadingEvents = false;
          if (mode == "created"){
            this.eventSources.push(this.journeysCreatedDriver);
            this.eventSources.push(this.journeysCreatedNoDriver);
          }
          if (mode == "joined") this.eventSources.push(this.journeysJoined);
        }
      });
    }

  }

  // Load next events
  loadNextEvents(url) {

  }

  // Change view
  changeView(view, calendar) {
    this.uiCalendarConfig.calendars[calendar].fullCalendar('changeView', view);
  }

  $onInit() {
    this.loadingEvents = false;
    this.eventSources = [];
    this.journeysCreatedDriver = {
      color: '#99c300',
      textColor: '#fff',
      events: []
    };
    this.journeysCreatedNoDriver = {
      color: '#ec6409',
      textColor: '#fff',
      events: []
    };
    this.journeysJoined = {
        color: '#01a5cb',
        textColor: '#fff',
        events: []
      };

    // Calendar config object
    this.uiConfig = {
      calendar: {
        editable: false,
        defaultView: "agendaWeek",
        lang: "es",
        header:{
          left: 'title',
          center: '',
          right: 'today prev,next'
        }
      }
    };
    this.loadEvents();
  }
}
CalendarController.$inject = ['$scope', 'JourneyService', 'uiCalendarConfig'];

/**
 * Controller for the map widget with a circle, to select the position and
 * distance, to make queries or update fields.
 */
class CircleMapController {

  constructor($scope, uiGmapGoogleMapApi) {
    this.scope = $scope;
    this.uiGmapGoogleMapApi = uiGmapGoogleMapApi;
  }

  changeCenter(latitude, longitude) {
    this.map.center = {
      latitude: latitude,
      longitude: longitude
    };
    this.circle.center = {
      latitude: latitude,
      longitude: longitude
    };
  }

  hasInitialCenter() {
    return !(this.positionValue == null || this.positionValue == undefined || this.positionValue == "None");
  }

  hasInitialRadius() {
    return this.radiusValue !== null && this.radiusValue !== undefined && this.radiusValue !== "None";
  }

  getInitialCenter() {
    var re = /POINT \(([0-9\-\.]+) ([0-9\-\.]+)\)/;
    var values = this.positionValue.match(re);
    if (values.length == 3) {
      return {
        latitude: parseFloat(values[2]),
        longitude: parseFloat(values[1])
      };
    }
    return null
  }

  getInitialRadius() {
    return parseFloat(this.radiusValue);
  }

  initializeMap() {
    if (!this.hasInitialCenter()) {
      // Initial position from geolocation
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition( (position) => {
          this.scope.$apply( () => {
            this.changeCenter(position.coords.latitude, position.coords.longitude);
          });
        });
      }
    }
  }

  positionObjectToGis(latitude, longitude) {
    return `POINT (${longitude} ${latitude})`;
  }

  $onInit() {
    // Map configuration
    this.map = {
      zoom: 16,
      center: {
          latitude: 39.4703669,
          longitude: -0.3749849,
      },
      options: {
        disableDefaultUI: false
      }
    };
    // Circle configuration
    this.circle = {
      center: {
          latitude: 39.4703669,
          longitude: -0.3749849,
      },
      radius: 200,
      stroke: {
        color: '#99c300',
        weight: 2,
        opacity: 1
      },
      fill: {
          color: '#99c300',
          opacity: 0.5
      },
      geodesic: true,
      draggable: true,
      clickable: true,
      editable: true,
      visible: true,
      control: {},
      events: {
        center_changed: () => {
          var value = this.circle.center;
          this.pointString = this.positionObjectToGis(value.latitude, value.longitude);
        }
      }
    };
    // Search box configuration
    this.searchbox = {
      template: 'searchbox.tpl.html',
      events: {
        places_changed: (searchBox) => {
          var places = searchBox.getPlaces(),
              place = {};
          if (places.length > 0) {
            place = places[0];
            this.changeCenter(
              place.geometry.location.lat(),
              place.geometry.location.lng()
            );
          }
        }
      }
    };
    // Point string
    this.pointString = "";
    // Watch changes on circle center
    this.scope.$watch("$ctrl.circle.center", (value) => {
      if (value !== undefined) {
        this.pointString = this.positionObjectToGis(value.latitude, value.longitude);
      }
    });
    if (this.hasInitialCenter()) {
      this.map.center = this.getInitialCenter();
      this.circle.center = this.getInitialCenter();
    }
    if (this.hasInitialRadius()) {
      this.circle.radius = this.getInitialRadius();
    }
    // Load Google Maps
    this.uiGmapGoogleMapApi.then( (maps) => {
      this.maps = maps;
      this.initializeMap();
    });
  }
}
CircleMapController.$inject = ["$scope", "uiGmapGoogleMapApi"];

export {OriginDestinationSelectController, DatetimeController, CalendarController, CircleMapController};

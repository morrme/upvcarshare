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


export {OriginDestinationSelectController, DatetimeController, CalendarController};

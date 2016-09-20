// JourneyService to access services API.


class JourneyService {

  constructor($http) {
    this.$http = $http;
  }

  getResidences() {
    return this.$http.get("/api/v1/residences/")
      .then(response => response.data );
  }

  getCampus() {
    return this.$http.get("/api/v1/campus/")
      .then(response => response.data );
  }

  getJourneys() {
    return this.$http.get("/api/v1/journeys/")
      .then(response => response.data );
  }

  getJourneyRecurrence(journeyId) {
    return this.$http.get(`/api/v1/journeys/${journeyId}/recurrence/`)
      .then(response => response.data );
  }

  getJourneysOwned() {
    return this.$http.get("/api/v1/journeys/?owned=1")
      .then(response => response.data );
  }

  getJourneysJoined() {
    return this.$http.get("/api/v1/journeys/?joined=1")
      .then(response => response.data );
  }

  getByUrl(url) {
    return this.$http.get(url)
      .then(response => response.data );
  }

}

JourneyService.$inject = ['$http'];

export default JourneyService;

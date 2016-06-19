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
}

JourneyService.$inject = ['$http'];

export default JourneyService;

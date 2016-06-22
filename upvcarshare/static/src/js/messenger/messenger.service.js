// Class based service to access the API of messenger.
class MessengerService {

  constructor($http) {
    this.$http = $http;
  }

  // Gets the list of messages for a given journey
  getMessages(journey, latestId=null) {
    var url = `/api/v1/journeys/${journey}/messages/`;
    if (latestId != null) {
      url = `${url}?latest_id=${latestId}`;
    }
    return this.$http.get(url)
      .then(response => response.data );
  }

  // Use this method to paginate requests
  getFromUrl(url) {
    return this.$http.get(url)
      .then(response => response.data );
  }

  // Post a message
  postMessage(journey, content) {
    return this.$http.post(
      "/api/v1/messages/",
      {journey, content},
      {
        headers: {
          "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val()
        }
      }
    ).then(response => response.data );
  }

}

MessengerService.$inject = ['$http'];

export default MessengerService;

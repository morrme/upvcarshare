// Class based service to access the API of messenger.
class MessengerService {

  constructor($http) {
    this.$http = $http;
  }

  // Gets the list of messages for a given journey
  getMessages(journey) {
    return this.$http.get(`/api/v1/journeys/${journey}/messages/`)
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

export default MessengerService;

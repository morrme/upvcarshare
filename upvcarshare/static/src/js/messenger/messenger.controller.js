import moment from 'moment';
import 'moment/locale/es';


class MessengerController {

  constructor($scope,$element, MessengerService) {
    this.messengerService = MessengerService;
    this.$scope = $scope;
    this.$element = $element;
  }

  $onInit() {
    this.messages = [];
    this.newMessage = this.getNewMessage();
    this.savingMessage = false;
    this.loadingMessages = false;

    this.loadMessages();
  }

  // Launch initial messages
  loadMessages() {
    this.loadingMessages = true;
    this.messengerService.getMessages(this.journey).then( response => {
      this.messages = response.results;
      if (!response.next) {
        this.loadingMessages = false;
      } else {
        this.paginateMessages(response.next);
      }
    });
  }

  // Method to resolve pagination of messages
  paginateMessages(url) {
    this.messengerService.getFromUrl(url).then( response => {
      response.results.forEach( (value) => {
        this.messages.push(value);
      });
      if (!response.next) {
        this.loadingMessages = false;
      } else {
        this.paginateMessages(response.next);
      }
    });
  }

  // Creates a new message
  getNewMessage() {
    return {
      journey: this.journey,
      content: "",
      user: {
        id: this.userId,
        first_name: this.firstName,
        last_name: this.lastName
      },
      created: moment().toISOString()
    };
  }

  // Sends a message
  sendMessage({message}) {
    if (!message || this.loadingMessages || this.savingMessage) return;
    this.messages.push(message);
    this.savingMessage = true;
    message.status = "sending";
    this.messengerService.postMessage(message.journey, message.content).then( response => {
      this.savingMessage = false;
      message.id = response.id;
      message.status = "saved";
    }, response => {
      message.status = "error";
    });
    this.newMessage = this.getNewMessage();
  }

}
MessengerController.$inject = ['$scope', '$element', 'MessengerService'];


class MessageListController {

  constructor() {}

  showTimestamp(timeString) {
    moment.locale('es');
    return moment(timeString).calendar();
  }

}


class MessageFormController {

  constructor() {}

  // The $onChanges lifecycle hook makes a clone of the initial this.message
  // binding Object and reassigns it, which means the parent data is not
  // affected until we submit the form, alongside one-way data flow new
  // binding syntax '<'.
  $onChanges(changes) {
    if (changes.message) {
      this.message = Object.assign({}, this.message);
    }
  }

  // Pass the message to the messenger controller
  onSubmit() {
    if (!this.message.content) return;
    this.onSendMessage({
      $event: {
        message: this.message
      }
    });
  }

}


export {MessageFormController, MessageListController, MessengerController}

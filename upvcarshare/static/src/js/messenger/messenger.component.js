import {MessengerController, MessageListController, MessageFormController} from './messenger.controller'


// Component that encapsulate all messenger functionality
const MessengerComponent = {
  controller: MessengerController,
  templateUrl: "/partials/messenger/messenger.html",
  bindings: {
    journey: '@',
    firstName: '@',
    lastName: '@'
  }
};

// Component that shows a single message
const MessageListComponent = {
  controller: MessageListController,
  templateUrl: "/partials/messenger/message.list.html",
  bindings: {
    messages: '<'
  }
};

// Component to show a form to create messages
const MessageFormComponent = {
  controller: MessageFormController,
  templateUrl: "/partials/messenger/message.form.html",
  bindings: {
    message: '<',
    onSendMessage: '&'
  }
};


export {MessageListComponent, MessageFormComponent, MessengerComponent};

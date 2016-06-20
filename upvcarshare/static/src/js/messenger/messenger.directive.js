// Directive to change the color of the user
const MessageUserColor = ($cookies) => ({
  restrict: 'A',

  link($scope, $element, $attrs) {
    var userId = $attrs.userColor;
    var journeyId = $attrs.journey;
    var colors = [
      "#e74c3c",
      "#e67e22",
      "#f1c615",
      "#3498db",
      "#2ecc71",
      "#1abc9c",
      "#9b59b6",
      "#34495e"
    ];
    var usedColorsCookieKey = `used-colors-${journeyId}`;
    var userColorCookieKey = `user-color-${journeyId}-${userId}`;

    // Get used colors
    var usedColors = $cookies.get(usedColorsCookieKey);
    if (usedColors !== undefined) {
      var usedColorsList = [];
      usedColors.split(',').forEach( value => {
        "use strict";
        usedColorsList.push(value);
      });
      usedColors = usedColorsList;
    }
    else {
      usedColors = [];
    }

    // Get available colors
    var availableColors = [];
    colors.forEach( value => {
      "use strict";
      if (usedColors.indexOf(value) == -1) {
        availableColors.push(value);
      }
    });

    // Assign color
    var selectColor = $cookies.get(userColorCookieKey);
    if (!selectColor) {
      var randomIndex = Math.floor(Math.random() * (availableColors.length - 1));
      selectColor = availableColors[randomIndex];
      $cookies.put(userColorCookieKey, selectColor);
      usedColors.push(selectColor);
    }

    // Save used colors
    $cookies.put(usedColorsCookieKey, usedColors.join());

    // Change color
    $element.css("color", selectColor);
  }

});
MessageUserColor.$inject = ['$cookies'];

export default MessageUserColor;

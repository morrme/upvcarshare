const JourneyForm = () => ({
  restrict: 'A',
  link: (scope, element, attr) => {
    scope.iAmDriver = "False";
  }
});

export default JourneyForm;

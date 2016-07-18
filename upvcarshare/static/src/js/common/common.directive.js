const PreventSubmit = () => ({
  restrict: 'A',
  link: (scope, element, attr) => {
    element.keydown( (event) => {
      if (event.keyCode === 13) {
        event.preventDefault();
        return false;
      }
    });
  }
});

export default PreventSubmit;

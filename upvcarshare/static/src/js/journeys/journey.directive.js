import {JoinAllOneController} from './journeys.controller';

const JourneyForm = () => ({
  restrict: 'A',
  link: (scope, element, attr) => {
    scope.iAmDriver = "False";
  }
});

const JoinJourneyForm = ($uibModal) => ({
  restrict: 'A',
  link: (scope, element, attr) => {
    // Initial value for join to value to one. It could be 'one' or 'all'
    scope.joinToValue = null;

    // Function to open modal
    function openModal() {
      var modalInstance = $uibModal.open({
        animation: true,
        templateUrl: 'join-all-one.html',
        controller: JoinAllOneController
      });
      modalInstance.result.then( (selectedOption) => {
        scope.joinToValue = selectedOption;
        var field = element.find("[name='join_to']");
        field.val(selectedOption);
        element.submit();
      });
    }

    // Link on submit form
    element.submit(() => {
      if (scope.joinToValue == null) {
        openModal();
        return false;
      }
      return true;
    });

  }
});
JoinJourneyForm.$inject = ["$uibModal"];

export {JourneyForm, JoinJourneyForm};

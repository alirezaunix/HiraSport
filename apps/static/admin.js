document.addEventListener('DOMContentLoaded', function() {
    function toggleFields() {
        // Define the fields to show/hide based on the role
        var fieldsForEmployee = document.querySelectorAll('.field-employee_field');
        var fieldsForTrainer = document.querySelectorAll('.field-t_edu, .field-t_exp, .field-t_shortdesc,.field-sfield ,.field-classname,.field-phone1');
        var fieldsForStudent = document.querySelectorAll('.field-ncode,.field-scode,.field-insurancedate, .field-shistory, .field-hhistory,.field-sfield,.field-classname ,.field-phone1,.field-phone2,.field-address,.field-rsession,.field-discount');

        // Get the value of the selected role
        var selectedRole = document.querySelector('input[name="role"]:checked').value;

        // Show/hide fields based on the selected role
        function displayFields(fields, display) {
            fields.forEach(function(field) {
                field.style.display = display;
            });
        }

        // Hide all fields initially
        displayFields(fieldsForEmployee, 'none');
        displayFields(fieldsForTrainer, 'none');
        displayFields(fieldsForStudent, 'none');

        // Show fields based on the selected role
        if (selectedRole === 'employee') {
            displayFields(fieldsForEmployee, 'block');
        } else if (selectedRole === 'trainer') {
            displayFields(fieldsForTrainer, 'block');
        } else if (selectedRole === 'student') {
            displayFields(fieldsForStudent, 'block');
        }
    }

    // Attach the toggleFields function to the role radio buttons' change event
    var roleRadioButtons = document.querySelectorAll('input[name="role"]');
    roleRadioButtons.forEach(function(button) {
        button.addEventListener('change', toggleFields);
    });

    // Call toggleFields on page load to set the initial state
    toggleFields();
});

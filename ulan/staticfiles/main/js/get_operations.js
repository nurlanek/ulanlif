document.addEventListener('DOMContentLoaded', function() {
    var kroySelect = document.getElementById('kroy');
    var operationCodeSelect = document.getElementById('operation_code');
    var operationListSelect = document.getElementById('operation_list');

    if (kroySelect) {
        kroySelect.addEventListener('change', function() {
            var kroy_id = this.value;
            if (kroy_id) {
                fetch(`/get_operation_codes/?kroy_id=${kroy_id}`)
                    .then(response => response.json())
                    .then(data => {
                        operationCodeSelect.innerHTML = '<option value="">Select Operation Code</option>';
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item.id;
                            option.textContent = item.title;
                            operationCodeSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error:', error));
            } else {
                operationCodeSelect.innerHTML = '<option value="">Select Operation Code</option>';
            }
        });
    }

    if (operationCodeSelect) {
        operationCodeSelect.addEventListener('change', function() {
            var operation_code_id = this.value;
            if (operation_code_id) {
                fetch(`/get_operation_list/?operation_code_id=${operation_code_id}`)
                    .then(response => response.json())
                    .then(data => {
                        operationListSelect.innerHTML = '<option value="">Select Operation</option>';
                        data.forEach(item => {
                            let option = document.createElement('option');
                            option.value = item.id;
                            option.textContent = item.title;
                            operationListSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error:', error));
            } else {
                operationListSelect.innerHTML = '<option value="">Select Operation</option>';
            }
        });
    }
});

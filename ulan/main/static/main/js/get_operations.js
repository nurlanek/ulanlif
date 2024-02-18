document.getElementById("kroy-form").addEventListener("change", function() {
    var kroyNo = document.querySelector("[name='kroy_no']").value;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_operations/?kroy_no=" + kroyNo, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var operations = JSON.parse(xhr.responseText);
            var operationsSelect = document.getElementById("operations-select");

            operationsSelect.innerHTML = "";

            operations.forEach(function(operation) {
                var option = document.createElement("option");
                option.value = operation.name; // ID numarasını değer olarak ayarla
                option.textContent = operation.name;
                operationsSelect.appendChild(option);
            });
        }
    };
    xhr.send();
});

// Form gönderildiğinde, seçilen operasyonun ID numarasını "operations" alanına ekleyin
document.getElementById("kroy-form").addEventListener("submit", function(event) {
    var selectedOperationId = document.getElementById("operations-select").value;
    document.getElementById("operations").value = selectedOperationId;
});

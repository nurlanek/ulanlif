// printTable.js dosyası
function printTable() {
    var printContents = document.getElementById("table-container").innerHTML;
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = printContents;

    window.print();

    document.body.innerHTML = originalContents;
}

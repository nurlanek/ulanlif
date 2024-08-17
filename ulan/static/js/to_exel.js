function exportTableToExcel(tableID, filename = ''){
    var downloadLink;
    var dataType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8';
    var tableSelect = document.getElementById(tableID);

    var wb = XLSX.utils.table_to_book(tableSelect, {sheet: "Sheet1"});
    var wbout = XLSX.write(wb, {bookType:'xlsx', type: 'binary'});

    function s2ab(s) {
        var buf = new ArrayBuffer(s.length);
        var view = new Uint8Array(buf);
        for (var i=0; i<s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
        return buf;
    }

    var blob = new Blob([s2ab(wbout)], {type: dataType});

    if (navigator.msSaveBlob) {
        navigator.msSaveBlob(blob, filename);
    } else {
        var url = URL.createObjectURL(blob);
        downloadLink = document.createElement("a");
        downloadLink.href = url;
        downloadLink.download = filename;
        downloadLink.click();
        document.body.removeChild(downloadLink);
    }
}

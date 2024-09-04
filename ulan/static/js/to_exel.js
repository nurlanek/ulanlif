function exportTableToExcel(tableID, filename = 'report.xlsx') {
        // Tabloyu al
        var table = document.getElementById(tableID);
        var wb = XLSX.utils.table_to_book(table, { sheet: "Sheet1" });

        // Dosyayı oluştur ve indir
        XLSX.writeFile(wb, filename);
    }
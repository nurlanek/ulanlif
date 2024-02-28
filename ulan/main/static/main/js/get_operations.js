$(document).ready(function(){
    // Sayfa yüklendiğinde ve 'kroy-no' veya 'type-product' değiştiğinde verileri getir
    fetchOperations();

    $('#kroy-no, #type-product').change(function(){
        fetchOperations();
    });

    // 'operations' seçeneği değiştiğinde fiyatı güncelle
    $('#operations').change(function(){
        var selectedPrice = $(this).find(':selected').data('price');
        $('#price-display').text(selectedPrice);
        $('#price-input').val(selectedPrice); // Fiyatı input alanına yerleştir
    });

    function fetchOperations() {
        var kroy_no = $('#kroy-no').val();
        var product_type = $('#type-product').val();

        $.ajax({
            type: 'GET',
            url: '/get-operations/',
            data: {
                'kroy_no': kroy_no,
                'type_product': product_type
            },
            success: function(data){
                var operations = data;
                $('#operations').empty(); // Önceki seçenekleri temizle
                for(var i=0; i<operations.length; i++){
                    // Her bir operasyon için hem isim hem de fiyat bilgisini ekle
                    var price = operations[i].price !== null ? operations[i].price : 'Belirtilmemiş';
                    $('#operations').append('<option value="' + operations[i].name + '" data-price="' + price + '">' + operations[i].name + '</option>');
                }

                // 'operations' seçeneği değiştiğinde fiyatı güncelle
                var selectedPrice = $('#operations').find(':selected').data('price');
                $('#price-display').text(selectedPrice);
                $('#price-input').val(selectedPrice); // Fiyatı input alanına yerleştir
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});

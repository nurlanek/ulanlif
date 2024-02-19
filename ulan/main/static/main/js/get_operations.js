$(document).ready(function(){
    $('#kroy-no, #type-product').change(function(){
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
                    $('#operations').append('<option value="' + operations[i].name + '">' + operations[i].name + '</option>');
                }

                // AJAX başarılı olduğunda, 'operations' alanının değerini gizli bir alana ekle
                var selectedOperation = $('#operations').val();
                var selectedOperationPrice = operations.find(operation => operation.name === selectedOperation).price;
                $('#kroy-form').append('<input type="hidden" name="operations" value="' + selectedOperation + '">');
                $('#kroy-form').append('<input type="hidden" name="price" value="' + selectedOperationPrice + '">');

                // 'price-display' alanını güncelle
                $('#price-display').text(selectedOperationPrice);
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});

$(document).ready(function(){
    // Burada form alanlarını dinleyen ve gerekli işlemleri yapan JavaScript kodu olabilir

    $('#kroy-form').submit(function(event){
        // Formun varsayılan davranışını engelle
        event.preventDefault();

        // Form verilerini al
        var formData = $(this).serialize();

        // AJAX isteği gönder
        $.ajax({
            type: 'POST',
            url: '/masterdatauser/', // Formun gönderileceği URL'yi buraya ekleyin
            data: formData,
            success: function(data){
                // Başarılı bir şekilde JSON yanıt alındığında burası çalışır
                console.log(data); // JSON yanıtını konsola yazdır
                // Burada JSON yanıtını işleyebilir ve kullanıcı arayüzünde gösterebilirsiniz
            },
            error: function(xhr, errmsg, err){
                // AJAX isteği sırasında hata oluştuğunda burası çalışır
                console.log(xhr.status + ": " + xhr.responseText);
                // Hata mesajını kullanıcıya gösterebilirsiniz
            }
        });
    });
});
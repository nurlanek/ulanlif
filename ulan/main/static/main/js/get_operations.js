$(document).ready(function(){
    $('#submit-btn').click(function(event){
        event.preventDefault(); // Formun normal gönderimini engelle

        var kroy_no = $('#kroy-no').val();
        var product_type = $('#type-product').val();

        if (kroy_no && product_type) { // Kroy numarası ve ürün tipi dolu mu?
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

                    // Başarılı mesajını göster
                    $('#success-message').text('Başarıyla gönderildi.');

                    // Formu temizle
                    $('#kroy-no').val('');
                    $('#type-product').val('');
                },
                error: function(xhr, errmsg, err){
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        } else {
            alert("Lütfen Kroy numarasını ve ürün tipini seçin.");
        }
    });
});
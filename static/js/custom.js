let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
      
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    // getting the address components and assign them to the fields

    var geocoder=new google.maps.Geocoder()
    var address=document.getElementById('id_address').value

    geocoder.geocode({'address':address}, function(results,status){

        if(status==google.maps.GeocoderStatus.OK){
            var latitude= results[0].geometry.location.lat();
            var longitude= results[0].geometry.location.lng();

            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);


        }
    });

    for(var i=0;i<place.address_components.length;i++){
        for(var j=0;j<place.address_components[i].types.length;j++){


            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }

            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }
            
        }
    }

}


$(document).ready(function(){
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        
        food_id=$(this).attr('data-id');
        url=$(this).attr('data-url');

        data ={
               
        }
        $.ajax({
            type:'GET',
            url:url,
            data:data,
            success: function(response){
                if(response.status=='login_required'){
                  swal(response.message,'','info').then(function(){
                    window.location='/login';
                  }) 
                }
                else if(response.status=='Failed'){
                    swal(response.message,'','error')
                  }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    updateCart_totals(
                        response.cart_totals['subtotal'],
                        response.cart_totals['tax_dict'],
                        response.cart_totals['total']
                    )
                }


            }

        })

    })

    $('.del_from_cart').on('click',function(e){
        e.preventDefault();
        
        cartItem_id=$(this).attr('id');
        food_id=$(this).attr('data-id');
        url=$(this).attr('data-url');

        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                if(response.status=='login_required'){
                    swal(response.message,'','info').then(function(){
                      window.location='/login';
                    }) 
                  }
                  else if(response.status=='Failed'){
                      swal(response.message,'','error')
                    }
                  else{
                      $('#cart_counter').html(response.cart_counter['cart_count']);
                      $('#qty-'+food_id).html(response.qty);
                      if(window.location.pathname == '/marketplace/cart/'){
                        check_cartItem_empty(response.qty,cartItem_id);
                        check_cart_empty();
                        updateCart_totals(
                            response.cart_totals['subtotal'],
                            response.cart_totals['tax_dict'],
                            response.cart_totals['total']
                        )
                      }
                      
                  }

            }

        })


        

    })

    $('.delete_cartItem').on('click',function(e){
        e.preventDefault();
 
        cartItem_id=$(this).attr('data-id');
        url=$(this).attr('data-url');

        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                if(response.status=='Failed'){
                      swal(response.message,'','error')
                    }
                else{
                      $('#cart_counter').html(response.cart_counter['cart_count']);
                      swal(response.message,'','success')
                      check_cartItem_empty(0,cartItem_id);
                      check_cart_empty();
                      updateCart_totals(
                        response.cart_totals['subtotal'],
                        response.cart_totals['tax_dict'],
                        response.cart_totals['total']
                    )

                  }

            }

        })
    })

    //function to delete cartitem if quantity is 0
    function check_cartItem_empty(cartItem_qty,cartItem_id){
        
        if(cartItem_qty<=0){
            document.getElementById("cart-item-"+cartItem_id).remove()
        }
    }

    function check_cart_empty(){
        var cart_counter=document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0)
            document.getElementById("empty-cart").style.display ='block';
    }

    $('.item_qty').each(function(){
        var the_id =$(this).attr('id')
        var qty=$(this).attr('data-qty')
        $('#'+the_id).html(qty)     
    })

    //to update subtotal,tax,total
    function updateCart_totals(subtotal,tax_dict,total){
        if(window.location.pathname == '/marketplace/cart/'){
                $('#subtotal').html(subtotal)
                $('#total').html(total)

                for(key1 in tax_dict){
                    
                    for(key2 in tax_dict[key1]){
                     
                        $('#tax-'+key1).html(tax_dict[key1][key2])
                    }
                }
        }
    }


    $('.add_hour').on('click',function(e){
            e.preventDefault();

        var day=document.getElementById('id_day').value
        var from_hour=document.getElementById('id_from_hour').value
        var to_hour=document.getElementById('id_to_hour').value
        var is_closed=document.getElementById('id_is_closed').checked
        var csrf_token= $('input[name=csrfmiddlewaretoken]').val()
        var url=document.getElementById('add_hour_url').value

        if(is_closed){
            is_closed='True'
            condition="day!=''"
        }
        else{
            is_closed='False'
            condition="day!='' && from_hour!='' && to_hour!=''"
        }

        if(eval(condition)){
            $.ajax({
                type:'POST',
                url:url,
                data:{
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour':to_hour,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrf_token,
                },

                success:function(response){
                    if(response.status== 'success'){
                
                        if(response.is_closed=='True'){
                            html='<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="delete_hour" data-url="/restaurant/opening_hours/delete/'+response.id+'/">Remove</a></td></tr>'
                        }
                        else{
                            html='<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+'-'+response.to_hour+'</td><td><a href="#" class="delete_hour" data-url="/restaurant/opening_hours/delete/'+response.id+'/">Remove</a></td></tr>'
                        }

                        $(".opening_hours").append(html)
                        document.getElementById("opening_hours").reset();
                    }
                    else{
                        swal(response.message,'','error')
                    }
                }
            })
        }
        else{
            swal('Please fill the neccassary fields','','info')
        }
    });

    $(document).on('click','.delete_hour',function(e){
        e.preventDefault();
        
        url=$(this).attr('data-url');
        
        $.ajax({
            type:'GET',
            url:url,
            success:function(response){
                if(response.status=='success'){
                    document.getElementById('hour-'+response.id).remove()
                }
            }
    
    
            })
        })
        

   
});


















    

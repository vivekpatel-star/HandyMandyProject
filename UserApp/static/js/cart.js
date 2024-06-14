function positiven(cartId,productId,productPrice){
    //Add Cart Button Hide
    //Plus,Qty,Minus Button Visible
    cartId = parseInt(cartId)
    productId = parseInt(productId)
    productPrice = parseInt(productPrice)
    
    pr = "mainbtnn"+productId
    btn = document.getElementById(pr).innerText;
    btn = +(btn) + +1;
    document.getElementById(pr).innerText = btn
    console.log("increase quantity:",btn+" on product:",productId)

    // subtotal = document.getElementById("subtotal").value
    // document.getElementById("subtotal").value = parseInt(subtotal)+parseInt(productPrice)

    data = JSON.stringify({
        'cartId' : cartId,
        'qty': btn,
        'productId': productId,
        'productPrice':productPrice,
        'type': 'Update'
    })
    const xhr = new XMLHttpRequest();
    xhr.responseType = 'json'
    xhr.open('POST', 'http://127.0.0.1:8000/category/cart_user_data/', true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    xhr.send(data);
    // console.log("Positive Click "+productId)
}

function negativen(cartId,productId,productPrice){
    //Add Cart Button Hide
    //Plus,Qty,Minus Button Visible
    cartId = parseInt(cartId)
    productId = parseInt(productId)
    productPrice = parseInt(productPrice)
    // console.log(productId)
    pr = "mainbtnn"+productId
    // console.log(pr)
    btn = document.getElementById(pr).innerText;
    // console.log(btn)
    // mbtn = document.getElementById("mainusbtn")
    
    // subtotal = document.getElementById("subtotal").value
    // document.getElementById("subtotal").value = parseInt(subtotal)+parseInt(productPrice)
    
    btn = btn - 1;
    if (btn < 1) {
        console.log("Negative Count Remove "+btn)
        document.getElementById(pr).innerText = 'ADD TO CART';
        $(".plusbtnn"+productId).css("display", "none");
        $(".mainusbtnn"+productId).css("display", "none");
        data = JSON.stringify({
            'cartId' : cartId,
            'qty': btn,
            'productId': productId,
            'productPrice': productPrice,
            'type': 'Remove'
        })
        const xhr = new XMLHttpRequest();
        xhr.responseType = 'json'
        xhr.open('POST', 'http://127.0.0.1:8000/category/cart_user_data/', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
        xhr.send(data);
    } else {
        console.log("Negative Count Update "+btn)
        document.getElementById(pr).innerText = btn
        console.log("decrease quantity:",btn+" on product:",productId)
        
        data = JSON.stringify({
            'cartId' : cartId,
            'qty': btn,
            'productId': productId,
            'productPrice': productPrice,
            'type': 'Update'
        })
        const xhr = new XMLHttpRequest();
        xhr.responseType = 'json'
        xhr.open('POST', 'http://127.0.0.1:8000/category/cart_user_data/', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
        xhr.send(data);
    }
}
//console.log("Cart JS Call Without Any Function")
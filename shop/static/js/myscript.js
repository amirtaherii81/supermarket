$(document).ready(
    function() {
        var urlparams = new URLSearchParams(window.location.search);
        if (urlparams == "") {
            localStorage.clear();
            $("#filter_state").css("display", "none");
        } else {
            $("#filter_state").css("display", "inline-block");
        }
        $('input:checkbox').on('click', function() {
            var fav, favs = [];
            $('input:checkbox').each(function() {
                fav = { id: $(this).attr('id'), value: $(this).prop('checked') };
                favs.push(fav);
            });
            localStorage.setItem("favorites", JSON.stringify(favs));
        });
        var favorites = JSON.parse(localStorage.getItem('favorites'));
        for (var i = 0; i < favorites.length; i++) {
            $('#' + favorites[i].id).prop('checked', favorites[i].value);
        }
    }
);



//----------------------------------------------------------------
function showVal(x) {
    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    document.getElementById('sel_price').innerText = x;
}


//----------------------------------------------------------------
// تابع حذف پارامتر های خط آدرس
function removeURLParameter(url, parameter) {
    var urlparts = url.split('?');
    if (urlparts.length >= 2) {
        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;) {
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                pars.splice(i, 1);
            }
        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url;
}


//----------------------------------------------------------------
// تابع انخاب مرتب سازی محصولات
function select_sort() {
    var select_sort_value=$("#select_sort").val();
    var url=removeURLParameter(window.location.href, "sort_type");
    // window.location = url + "?sort_type=" + select_sort_value;
    if (url.indexOf('?') === -1) {
        window.location = url + "?sort_type=" + select_sort_value;
    } else {
        window.location = url + "&sort_type=" + select_sort_value;
    }
}




//----------------------------------------------------------------
function select_display(){
    var select_display_value = $('#select_display').val();
    var url = new URL(window.location.href);
    url.searchParams.set('display', select_display_value);
    window.location = url.toString();
}



//----------------------------------------------------------------
// Shop Cart
function status_of_shop_cart() {
    $.ajax({
        type: "GET",
        url: "/orders/status_of_shop_cart/",
        success: function(res) {
            $("#indicator__value").text(res);
        }
    });
}

// time of load
status_of_shop_cart();

//----------------------------------------------------------------
function add_to_shop_cart(product_id, qty) {
    if(qty === 0){
        qty=$("#product-quantity").val();
        alert(qty)
    }
    $.ajax({
        type:"GET",
        url:"/orders/add_to_shop_cart/",
        data:{
            product_id:product_id,
            qty:qty,
        } , 
        success: function(res) {
            alert("کالای مورد نظر شما به سبد خرید شما اضافه شد");
            $("#indicator__value").text(res);
            status_of_shop_cart();
        }
    });
}

//----------------------------------------------------------------
function delete_from_shop_cart(product_id) {
    $.ajax({
        type:"GET",
        url:"/orders/delete_from_shop_cart/",
        data:{
            product_id:product_id,
        } , 
        success: function(res) {
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
        }
    });
}

//----------------------------------------------------------------
function update_shop_cart() {
    var product_id_list=[]
    var qty_list=[]
    $("input[id^='qty_']").each(function(index) {
        product_id_list.push($(this).attr('id').slice(4))
        qty_list.push($(this).val())
    });
    $.ajax({
        type: "GET",
        url: "/orders/update_shop_cart/",
        data: {
            product_id_list:product_id_list,
            qty_list:qty_list
        },
        success: function(res) {
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
        }
    });
}

//----------------------------------------------------------------
function showCreateCommentForm(productId, commentId, slug) {
    $.ajax({
        type: "GET",
        url: "/csf/create_comment/" + slug,
        data: {
            productId: productId,
            commentId: commentId
        },
        success: function(res) {
            $("#btn_" + commentId).hide();
            $("#comment_form_" + commentId).html(res);
        }
    });
}

//----------------------------------------------------------------
function addScore(score, productId) {  
    var starRatings = document.querySelectorAll(".fa-star");  

    // غیر فعال کردن ستاره‌ها به محض کلیک برای امتیاز دهی  
    starRatings.forEach(element => {  
        element.classList.add("disable");  
    });  

    // حذف کلاس checked از همه ستاره‌ها  
    starRatings.forEach(element => {  
        element.classList.remove("checked");  
    });  

    // اضافه کردن کلاس checked به ستاره‌های ارزیابی شده  
    for (let i = 1; i <= score; i++) {  
        const element = document.getElementById("star_" + i);  
        if (element) {  
            element.classList.add("checked");  
        }  
    }  

    // ارسال امتیاز با AJAX  
    $.ajax({  
        type: "GET",  
        url: "/csf/add_score/",  
        data: {  
            productId: productId,  
            score: score,  
        },  
        success: function(new_avg_score) {  
            alert("امتیاز شما با موفقیت ثبت شد");  
            // می‌توانید اگر نیاز داشتید، میانگین امتیاز جدید را نیز بروزرسانی کنید  
            var avgScoreElement = document.getElementById("avg_score_" + productId);  
            if (avgScoreElement) {  
                avgScoreElement.innerText = new_avg_score;  
            }  
        },  
        error: function(xhr, status, error) {  
            console.error("خطایی رخ داد: " + error);  
            alert("خطایی در ثبت امتیاز رخ داد. لطفاً دوباره تلاش کنید.");  
        }  
    });  
}






//----------------------------------------------------------------
function addToFavorites(productId) {
    $.ajax({
        type: "GET",
        url: "/csf/add_to_favorite/",
        data: {
            productId: productId,
        },
        success: function(res) {
            alert(res);cd
        }
    });
}

//----------------------------------------------------------------
status_of_compare_list();

//----------------------------------------------------------------
function status_of_compare_list() {
    $.ajax({
        type: "GET",
        url: "/products/status_of_compare_list/",
        success: function(res) {
            if (Number(res) === 0) {
                $("#compare_count_icon").hide();
            } else {
                $("#compare_count_icon").show();
                $("#compare_count").text(res);
            }
        }
    });
}

//----------------------------------------------------------------
function addToCompareList(productId) {
    $.ajax({
        type: "GET",
        url: "/products/add_to_compare_list/",
        data: {
            productId: productId
            // productGroupId: productGroupId,
        },
        success: function(res) {
            alert(res);
            status_of_compare_list();
        }
    });
}

//----------------------------------------------------------------
function deleteFromCompareList(productId) {
    $.ajax({
        type: "GET",
        url: "/products/delete_from_compare_list/",
        data: {
            productId: productId,
        },
        success: function(res) {
            alert('حذف با موفقیت انجام شد');
            $("#compare_list").html(res);
            status_of_compare_list();
        }
    });
}

//----------------------------------------------------------------
// favorite products
function deleteFromFavoriteList(product_id) {
    $.ajax({
        type: "GET",
        url: "/csf/delete_favorite/",
        data: {
            product_id: product_id,
        },
        success: function(res) {
            // alert('کالا از لیست علاقه مندی ها با موفقیت حذف شد')
            $("#show_wishlist").html(res);
        }
    });
}

//----------------------------------------------------------------

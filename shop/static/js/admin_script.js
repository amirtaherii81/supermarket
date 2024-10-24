$(document).ready(function () {
    var listOfElements = $('select[id^="id_product_features-"][id$="-feature"]');
    $(listOfElements).on('change', function () {
        var f_id = $(this).val();
        var dd1 = $(this).attr('id');
        var dd2 = dd1.replace("-feature", "-filter_value");

        $.ajax({
            type: 'GET',
            url: "/products/ajax_admin/?feature_id=" + f_id,
            success: function (res) {
                cols = document.getElementById(dd2);
                cols.options.length = 0;
                for (var k in res) {
                    cols.options.add(new Option(k, res[k]));
                }
            }
        });
    });
});


$(document).ready(function () {
    $('#id_product_name').on('input', function () {
        const productName = $(this).val();
        const slug = createSlug(productName);
        $('#id_slug').val(slug);
    });
    function createSlug(text) {
        return text
            .toLowerCase()                      // Convert to lowercase
            .trim()                             // Remove extra spaces from start and end
            .replace(/[\s]+/g, '-')            // Replace spaces with '-'
            .replace(/[^\w\-آ-ی۰-۹]+/g, '')    // Remove invalid characters (allow Persian letters and numbers)
            .replace(/\-\-+/g, '-')            // Replace '- -' with '-'
            .replace(/^-+|-+$/g, '');          // Remove '-' from start and end
    }
});

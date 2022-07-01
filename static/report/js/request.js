
class Request {


    post (url, data, callback) {
        $.post(url, data, function (data, status) {
            callback(data, status);
        });
        // $.ajax({
        //     type: "POST",
        //     url: url,
        //     headers: {
        //       "Access-Control-Allow-Origin":"*"
        //     },
        //     dataType:"json",
        //     data: data,
        //     success: function (ajaxdata) {
        //         callback(ajaxdata);
        //     }
        // });

    }



};
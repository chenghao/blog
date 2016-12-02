/**
 * Created by chenghao on 16-12-2.
 */

var serverUrl = "/";

function getPrefixPath(url) {
    return serverUrl + url;
}

function customHref(url) {
    location.href = getPrefixPath(url);
}

function ajaxReq(url, callback, param, method, async, error){
	$.ajax({
        url: getPrefixPath(url) + "?t=" + (new Date()).valueOf(),
        data: !param ? {} : param,
        type: !method ? "get" : method,
        dataType: "json",
		async: async == undefined ? true : async,
        success: function (data) {
            if (callback) {
                callback(data);
            }
        },
        error: function(){
            if(error){
                error();
            }else{
                layer.msg("系统异常", {icon: 5, time: 3000})
            }
        }
    })
}
/* Common utils */
/*-------------------------STRINGS---------------------------------*/
//string.format
//用法："{0} is dead, but {1} is alive! {0} {2}".format("ASP", "ASP.NET")
String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
        return typeof args[number] != 'undefined' ? args[number] : match;
    });
};

/* Advertisments framework */

var advertisments = [["郑洁快看", "http://baidu.com", "2013/12/24", "双线不卡", "畅通无阻", "12345678", "服务器IP"]];

var load_9pk_ads = function(){
    // args for AD_tempalte {0:name, 1:ad_url, 2:open_date, 3:link, 4:comment, 5:kf_qq, 6:server_ip}
    var AD_template='<tr bgcolor=\"#FFFF98\" onmouseover=javascript:this.bgColor=\'#FFFFFF\' ' 
        + 'onmouseout=javascript:this.bgColor=\'#FFFF98\'><TD width=120> '
        + '<a href="{1}" target="_blank"><font color=#000000>'
        + '{0}</font></a></TD><TD width=101>'
        + '<a href="{1}" target="_blank">{6}</a></TD>'
        + '<TD class=font_R width=150>{2}开放</TD>' 
        + '<TD align=center width=80>{3}</TD><TD>{4}-<font color=#ff0000>推荐</font></TD>'
        + '<TD width=120>客服QQ:{5}</TD><TD align=center width=56>'
        + '<a href="{1}" target="_blank">点击查看</a></TD></tr>';
    
    var $top_table=$($("table.tableBorder1")[0]);
    for(var i=0;i<advertisments.length;i++){
        var ad_args = advertisments[advertisments.length - i - 1];
        var ad_string = AD_template.format(ad_args[0], ad_args[1], ad_args[2], ad_args[3], ad_args[4], ad_args[5], ad_args[6]);
        $top_table.find("tr:eq(1)").before(ad_string);
    }
};

var load_handlers = {"9pk.118sh.com" : load_9pk_ads};

var load_ads = function(){
    var host = window.location.host;
    var handler = load_handlers[host];
    if(handler !== undefined){
        handler();
    }
};

$(document).ready(function(){
    load_ads();
});
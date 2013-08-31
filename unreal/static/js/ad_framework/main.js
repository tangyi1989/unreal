
/* --------------------------- Advertisement framework --------------------- */
var load_type1 = function(){
    // args for AD_tempalte {0:name, 1:ad_url, 2:open_date, 3:link, 4:comment, 5:kf_qq, 6:server_ip}
    $("table.tableBorder1").each(function(){
        var $template_record = $(this).find('tr:eq(1)').clone();
        
        for(var i=0;i<global_ads.length;i++){
            var ad_args = global_ads[global_ads.length - i - 1];
            var $ad_record = $template_record.clone();

            // server name
            var $server_name = $ad_record.find('td:eq(0)');
            $server_name.find('a').attr('href', ad_args[1]);
            $server_name.find('a').html(ad_args[0]);

            // server_ip
            var $server_ip = $ad_record.find('td:eq(1)');
            $server_ip.find('a').attr('href', ad_args[1]);
            $server_ip.find('a').html(ad_args[6]);

            // do not modify open_date
            
            // link
            var $link = $ad_record.find('td:eq(3)');
            $link.html(ad_args[3]);

            // version 
            var $version = $ad_record.find('td:eq(4)');
            $version.html(ad_args[4] + '-' + $version.find('font')[0].outerHTML);

            // kf_qq
            var $kf_qq = $ad_record.find('td:eq(5)');
            $kf_qq.html('客服QQ:'+ad_args[5]);

            // url
            var $url = $ad_record.find('td:eq(6)');
            $url.find('a').attr('href', ad_args[1]);

            $(this).find("tr:eq(1)").before($ad_record);
        }
    });
};

var load_handlers = {"9pk.118sh.com" : load_type1};

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
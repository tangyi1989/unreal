/* load ads for each website */

var load_handlers = {"9pk.118sh.com" : load_9pk_ads};

function load_9pk_ads(){
    var test_ad='<tr bgcolor=\"#FFFF98\" onmouseover=javascript:this.bgColor=\'#FFFFFF\' onmouseout=javascript:this.bgColor=\'#FFFF98\'><TD width=120> <a href=http://sk01.zhmcc.com target="_blank"><font color=#000000>╰╊轻变一区╊╯</font></a></TD><TD width=101><a href=http://sk01.zhmcc.com target="_blank">散人骨灰必选</a></TD><TD class=font_R width=150>8月/25日/12点开放</TD><TD align=center width=80>唐万万</TD><TD>─(全服只卖会员.装备全靠自己打)──-<font color=#ff0000>推荐</font></TD><TD width=120>客服QQ:长久稳定</TD><TD align=center width=56><a href=http://sk01.zhmcc.com target="_blank">点击查看</a></TD></tr>';
    var $top_table=$($("table.tableBorder1")[0]);
    $top_table.find("tr:eq(1)").before(test_ad);
}

function load_ads(){
    var host = window.location.host;
    var handler = load_handlers[host];
    if(handler !== undefined){
        handler();
    }
}

$(document).ready(function(){
    load_ads();
});
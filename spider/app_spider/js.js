Array.prototype.in_array = function (e) { for (i = 0; i < this.length; i++) { if (this[i] == e) return true; } return false; }
var Cookie = { get: function (name) { var value = '', matchs; if (matchs = document.cookie.match("(?:^| )" + name + "(?:(?:=([^;]*))|;|$)")) value = matchs[1] ? unescape(matchs[1]) : ""; return value }, set: function (name, value, expire, domain) { expire = expire || 30 * 24 * 3600 * 1000; var date = new Date(), cookie = ""; date.setTime(date.getTime() + expire); cookie = name + "=" + escape(value) + ";expires=" + date.toGMTString() + ";path=/;"; domain && (cookie += "domain=" + domain + ";"); document.cookie = cookie }, del: function (name, domain) { Cookie.set(name, '', -1, domain) } };



function HTMLDeCode(str) {
    var s = "";
    if (str.length == 0) return "";
    s = str.replace(/&amp;/g, "&");
    s = s.replace(/&lt;/g, "<");
    s = s.replace(/&gt;/g, ">");
    s = s.replace(/&nbsp;/g, " ");
    s = s.replace(/'/g, "\'");
    s = s.replace(/&quot;/g, "\"");
    s = s.replace(/<br>/g, "\n");
    return s;
}
var _GET = (function () {
    var url = document.getElementsByTagName("script")[document.getElementsByTagName("script").length - 1].src;
    // var url = window.document.location.href.toString();
    var u = url.split("?");
    if (typeof (u[1]) == "string") {
        u = u[1].split("&");
        var get = {};
        for (var i in u) {
            var j = u[i].split("=");
            get[j[0]] = j[1];
        }
        return get;
    } else {
        return {};
    }
})();

if (typeof AddressList === "undefined") { var AddressList = {}; }

function getUrl() {
    var Address, TypeID, SoftLinkID;

    Address = _GET["Address"];

    TypeID = _GET["TypeID"];
    SoftLinkID = _GET["TypeID"];
    SoftID = _GET["SoftID"];

    Address = decodeURIComponent(Address)

    if (Address.indexOf("http:") >= 0 || Address.indexOf("ftp:") >= 0 || Address.indexOf("https:") >= 0) {
        document.write("<li><a href='" + Address + "' target='_blank'>直接点击下载 </a></li>");
        return true;
    }

    var sList = (eval("AddressList.siteId_" + TypeID));

    var DownLoadName = sList.split("||")[0];
    var DownLoadURL = sList.split("||")[1];
    var DownLoadNameList = DownLoadName.split(",");
    var DownLoadURLList = DownLoadURL.split(",");
    var DownTitle, DownAlt, DownURL
    for (var n = 0; n < DownLoadNameList.length; n++) {

        DownURL = DownLoadURLList[n]
        //DownURL   = GetDownAddress(DownURL)

        DownURL = DownURL + Address


        if (DownLoadNameList[n].indexOf("#") >= 0) {
            DownTitle = DownLoadNameList[n].split("#")(0)
            DownAlt = DownLoadNameList[n].split("#")(1)
        } else {
            DownTitle = DownLoadNameList[n];
            DownAlt = DownLoadNameList[n];
        }
        document.write("<li class=\"address_like\"><a href=" + DownURL + " target=\"_blank\" onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">" + HTMLDeCode(DownTitle) + "</a></li>");
    }
}


var rootid = 0;
var nodownput = [13, 16, 19, 20, 21, 23, 24];//不显示下载器的大类id

//是否显示广告
if (typeof (_pageinfo) == "undefined") {
    rootid = 0;
} else {
    rootid = _pageinfo.rootId;
}
if (isNaN(rootid)) {
    rootid = 0;
}

//document.title +=1
function getUrl2() {
    var Address, TypeID, SoftLinkID;
    Address = _downInfo.Address;
    TypeID = _downInfo.TypeID;
    SoftLinkID = _downInfo.SoftLinkID;
    SoftID = _downInfo.SoftID;


    var downTitle = $("h1").text();
    downTitle = downTitle.split(/(\s|\()/)[0];
    downTitle = downTitle.substring(0, 20);
    downTitle = downTitle.replace(/[\s|\-|\"|\_|&]+/g, "");//去掉回车换行

    var ysDownUrl;






    var mydownLoad = new Array();

    mydownLoad.push("http://c5.97you.net/download/" + downTitle + "_31@" + SoftID + ".exe");   //日月
    mydownLoad.push("http://down.xiazai2.net/?/" + SoftID + "/cr173/" + downTitle + ".exe");   //音速

    mydownLoad.push("http://url.tduou.com/down/" + downTitle + "@225_" + SoftID + ".exe"); //马安山

    var adsNum = 0;
    var ysDownUrl = mydownLoad[2];



    ysDownUrl = "http://url.tduou.com/down/" + downTitle + "@225_" + SoftID + ".exe";

    // ysDownUrl = "http://cr173.down.123ch.cn/download/"+downTitle+"_31@" + SoftID +".exe"


    //取得软件名，此处按需更
    var xzq_softname = downTitle;
    // 设置渠道ID
    var xzq_channelID = "131";
    // 取得软件ID，此处按需修改
    var xzq_softID = SoftID;
    //定义根域名列表
    var baseDomains = ['xc.ahyessoft.com', 'xc.08an.com'];
    //产生随机数
    var i = Math.floor(Math.random() * baseDomains.length);
    //根据随机数，取数组中的元素
    var randomDomain = baseDomains[i];
    //parseInt中的，是取从Fri Jan 01 2016 00:00:00 GMT+0800 (CST)到目前的小时数
    //ysDownUrl = 'http://' + parseInt((Date.parse(new Date()) / 1000 - 1451577600) / 3600) + '.' + randomDomain + '/down/' + xzq_softname + '@' + xzq_channelID + '_' + xzq_softID + '.exe';


    //ysDownUrl = 'http://cr173.dun.gsxzq.com/download/' + xzq_softname + '_' + xzq_channelID + '@' + xzq_softID + '.exe';

    //ysDownUrl = 'http://xc.mieseng.com/down/' + xzq_softname + '@' + xzq_channelID + '_' + xzq_softID + '.exe';

    //2019-8-23
    ysDownUrl = 'http://down.6lugq4fy.com/cx/22/1/' + xzq_softname + '_' + xzq_channelID + '_' + xzq_softID + '.exe';

    //下载器地址结束




    //远程下载添加判断

    // 用Unicode编码是因为edge浏览器重复引用js编码会不对
    if ((Address.indexOf("http:") >= 0 || Address.indexOf("ftp:") >= 0 || Address.indexOf("https:") >= 0) && (Address.indexOf(".zip") >= 0 || Address.indexOf(".rar") >= 0 || Address.indexOf(".exe") >= 0 || Address.indexOf(".7z") >= 0) && !nodownput.in_array(rootid)) {

        document.write("<h3  data='viewAds' class='f-gsh3'>\u9700\u4f18\u5148\u4e0b\u8f7d\u9ad8\u901f\u4e0b\u8f7d\u5668:</h3> ");
        document.write("<li class=\"address_like downurl\" data='viewAds'><a href='javascript:;'>\u7535\u4fe1\u9ad8\u901f\u4e0b\u8f7d</a></li>");
        document.write("<li class=\"address_like downurl\" data='viewAds'><a href='javascript:;'>\u7535\u4fe1\u9ad8\u901f\u4e0b\u8f7d</a></li>");
        document.write("<li class=\"address_like downurl\" data='viewAds'><a href='javascript:;'>\u8054\u901a\u9ad8\u901f\u4e0b\u8f7d</a></li>");
        document.write("<li class=\"address_like downurl\" data='viewAds'><a href='javascript:;'>\u8054\u901a\u9ad8\u901f\u4e0b\u8f7d </a></li>");
        document.write("<h3 class='f-gsh3 m-addline'>\u666e\u901a\u4e0b\u8f7d\u5730\u5740 : </h3>");
        document.write("<li class=\"address_like f-other-url\"><a href='" + Address + "' target='_blank' onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">\u7535\u4fe1\u8fdc\u7a0b\u4e0b\u8f7d</a></li>");
        document.write("<li class=\"address_like f-other-url\"><a href='" + Address + "' target='_blank' onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">\u8054\u901a\u8fdc\u7a0b\u4e0b\u8f7d</a></li>");

        document.write("<li class=\"address_like f-other-url\"><a href='" + Address + "' target='_blank' onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">\u7535\u4fe1\u8fdc\u7a0b\u4e0b\u8f7d</a></li>");
        document.write("<li class=\"address_like f-other-url\"><a href='" + Address + "' target='_blank' onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">\u8054\u901a\u8fdc\u7a0b\u4e0b\u8f7d</a></li>");
        $(".downurl").click(function () {
            $(this).find("a").attr("href", ysDownUrl);
        });
        return true;
    }

    if ((Address.indexOf("http:") >= 0 || Address.indexOf("ftp:") >= 0 || Address.indexOf("https:") >= 0) && (TypeID == '0' || TypeID == '-1')) {

        document.write("<li class=\"address_like f-other-url\"><a href='" + Address + "' target='_blank' onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">\u7535\u4fe1\u8fdc\u7a0b\u4e0b\u8f7d</a></li>");
        document.write("<li class=\"address_like f-other-url\"><a href='" + Address + "' target='_blank' onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">\u8054\u901a\u8fdc\u7a0b\u4e0b\u8f7d</a></li>");

        document.write("<li class=\"address_like f-other-url\"><a href='" + Address + "' target='_blank' onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">\u7535\u4fe1\u8fdc\u7a0b\u4e0b\u8f7d</a></li>");
        document.write("<li class=\"address_like f-other-url\"><a href='" + Address + "' target='_blank' onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">\u8054\u901a\u8fdc\u7a0b\u4e0b\u8f7d</a></li>");
        $(function ($) {
            $('.ban-360').hide();
        });
        return true;
    }



    var sList = (eval("AddressList.siteId_" + TypeID));
    var DownLoadName = sList.split("||")[0];
    var DownLoadURL = sList.split("||")[1];
    var DownLoadNameList = DownLoadName.split(",");
    var DownLoadURLList = DownLoadURL.split(",");
    var DownTitle, DownAlt, DownURL
    //   console.log(DownLoadNameList.length)
    for (var n = 0; n < DownLoadNameList.length; n++) {

        DownURL = DownLoadURLList[n]

        //DownURL   = GetDownAddress(DownURL)
        if (String(DownURL) != "undefined") {

            if (DownURL.indexOf("__") > 0) {
                DownURL = DownURL.replace(/\__/g, Address)
            } else {
                DownURL = DownURL + Address
            }
        }
        var re = /(com|net|cn)\/\//g; // 创建正则表达式模式
        if (String(DownURL) != "undefined") {
            DownURL = DownURL.replace(re, "$1/");
        }
        if (DownLoadNameList[n].indexOf("#") >= 0) {
            DownTitle = DownLoadNameList[n].split("#")(0)
            DownAlt = DownLoadNameList[n].split("#")(1)
        } else {
            DownTitle = DownLoadNameList[n];
            DownAlt = DownLoadNameList[n];
        }

        var fname = $("h1").html();
        var fver = "";
        var fsize = $(".info li").eq(0).html();
        fsize = fsize || $("#gmcfg li").eq(2).html();
        if (fsize.indexOf("软件大小") > 0) {
            fsize = fsize.replace("软件大小:", "")
        }
        var iconurl = "http://www.cr173.com/skin/logo.jpg"

        if (_downInfo.TypeID != "39") {//判断不为商务包则执行 



            if (n == 0 && !nodownput.in_array(rootid) && _pageinfo.categroyId != "208") {





                // console.log(province)

                document.write("<h3  data='viewAds' class='f-gsh3'>\u9700\u4f18\u5148\u4e0b\u8f7d\u9ad8\u901f\u4e0b\u8f7d\u5668:</h3> ");
                document.write("<li class=\"address_like downurl\" data='viewAds'><a href='javascript:;'>\u7535\u4fe1\u9ad8\u901f\u4e0b\u8f7d</a></li>");
                document.write("<li class=\"address_like downurl\" data='viewAds'><a href='javascript:;'>\u7535\u4fe1\u9ad8\u901f\u4e0b\u8f7d</a></li>");
                document.write("<li class=\"address_like downurl\" data='viewAds'><a href='javascript:;'>\u8054\u901a\u9ad8\u901f\u4e0b\u8f7d</a></li>");
                document.write("<li class=\"address_like downurl\" data='viewAds1'><a href='javascript:;'>\u8054\u901a\u9ad8\u901f\u4e0b\u8f7d </a> </li> ");
                document.write('</li>'); document.write('<br/>');
                document.write("</li><h3 data='viewAds' class='f-gsh3 m-addline'>\u666e\u901a\u4e0b\u8f7d\u5730\u5740: </h3>");



                $(".downurl").click(function () {
                    $(this).find("a").attr("href", ysDownUrl);
                });

                /*
                $(".downurl").click(function(){	 
                    getAddress(); //重新获取一下下载地址
                    $(this).find("a").attr("href",ysDownUrl);
            
                });
                */
                // var exeurl= "http://tj.243ty.com/api.php?sid=4&id="+ SoftID;

                // document.write("<li class=\"address_like\"  data='viewAds'><a href='"+exeurl+"'><font color=red>自解压版</font>下载</a></li>");
                // document.write("<li class=\"address_like\"  data='viewAds'><a href='"+exeurl+"'><font color=red>自解压版</font>下载</a></li>");

            }



            if (n == 0 && nodownput.in_array(rootid)) { //如果是安卓资源就下载电脑版

                var moAddress = "http://mo.L5645.net/mo/setup.cr173." + SoftID + ".exe"

                // document.write("<h3 style='margin:5px 0 -5px 0; font-size:12px; background: none; background:none;color:#ccc' data='viewAds'>电脑版下载</h3> ");
                //  document.write("<li class=\"address_like downurl\" data='viewAds'><a href='"+moAddress+"'><b>PC版<font color=red>联通</font>下载</b></a></li>");
                // document.write("<li class=\"address_like downurl\" data='viewAds'><a href='"+moAddress+"'><b>PC版<font color=red>电信</font>下载</b></a></li>");
                // document.write("<h3 style='margin:0 0 -5px 0 ; font-size:12px; background: none; background:none;color:#ccc'  data='viewAds'>其他下载地址</h3>");
                // 去掉安卓的下载器。

            }


        }
        document.write("<li class=\"address_like f-other-url\" ><a href=\"" + DownURL + "\"  onclick=\"softCount(" + SoftID + "," + SoftLinkID + ")\">" + HTMLDeCode(DownTitle) + "</a></li>");
    }
    // var softdown = [];
    //     softdown[3] = "";
    //alert(DownLoadURL)


    //document.title +=2
}


function checkRate(nubmer) {
    var re = /^[0-9]+.?[0-9]*$/;   //判断字符串是否为数字     //判断正整数 /^[1-9]+[0-9]*]*$/  

    if (!re.test(nubmer)) {
        return false;
    } else {
        return true;
    }
}




if (typeof _downInfo === "undefined") {
    getUrl()
}
else {
    getUrl2()
}
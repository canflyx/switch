;

function checkIp(ip) {
    var exp=/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    var reg = ip.match(exp);
    if(reg==null){
        return false;
    } else {
        return true;
    }
}
var mon_edit_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".wrap_account_set .save").click( function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

             let ipaddr_target = $(".wrap_account_set textarea[name=ipaddr]");
             ipaddr=ipaddr_target.val();

            var adlist=ipaddr.split(/[(\r\n\s)\r\n\s]|,!，+/);
            adlist.forEach((item,index)=>{
                if(!item){
                    adlist.splice(index,1);
                    }
                })
            var isTrue=adlist.every(function (ip) {
                return checkIp(ip)

            })
             if (!isTrue ){
                common_ops.alert("IP输入不正确",ipaddr_target);
                return false;
            }




            btn_target.addClass("disabled");
            var data={
                ipaddr:JSON.stringify(adlist),
                note:$(".wrap_account_set input[name=note]").val(),

            }
            $.ajax({
                url:common_ops.buildUrl("/mon/set"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function(res){
                    console.log(res);
					btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/mon/") ;
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });
        } );
    }
};




$(document).ready( function(){
    mon_edit_ops.init();
} );
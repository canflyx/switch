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
var swip_edit_ops = {
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
            var login_name_target = $(".wrap_account_set input[name=login_name]");
            login_name=login_name_target.val()
            var login_pwd_target = $(".wrap_account_set input[name=login_pwd]");
            login_pwd=login_pwd_target.val()

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

             if (login_name.length<3 ){
                common_ops.alert("请输入符合规范的登陆名",login_name_target);
                return false;
            }
            if (login_pwd.length<2 ){
                common_ops.alert("请输入正常的密码",login_pwd_target);
                return false;
            }


            btn_target.addClass("disabled");
            var data={
                ipaddr:JSON.stringify(adlist),
                login_name:login_name,
                login_pwd:login_pwd,
                note:$(".wrap_account_set input[name=note]").val(),
                id:$(".wrap_account_set input[name=id]").val(),
                iscore:$(".wrap_account_set [name=iscore]:checked").val()
            }
            $.ajax({
                url:common_ops.buildUrl("/switch/set"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function(res){
                    console.log(res);
					btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/switch/") ;
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });
        } );
    }
};



$(document).ready( function(){
    swip_edit_ops.init();
} );
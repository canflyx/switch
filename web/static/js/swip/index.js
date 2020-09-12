;
var sw_index_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;


        $(".remove").click( function(){
            that.ops( "remove",$(this).attr("data") );
        } );

        $("#allAndNotAll").click(function() {
			if (this.checked){
		        $("input[name='selectFlag']:checkbox").prop("checked", true);
		    } else {
		        $("input[name='selectFlag']:checkbox").prop("checked", false);
		    }
		});
       // $("#getValue").click(function(){
         $(".wrap_search .scan").click(function(){
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }
            var valArr = new Array;
            $("#list input[name='selectFlag']").each(function(i){
                if($(this).prop("checked")){
                    valArr[i]=$(this).val();
                }
            });
             if (valArr.length<1){
                common_ops.alert("没有选择需要扫描的交换机");
                return;
            }
             btn_target.addClass("disabled")
            var data={
                id:JSON.stringify(valArr),
            };
            $.ajax({
                url: common_ops.buildUrl("/switch/scan"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/switch/");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        })




    },

    ops:function( act,id ){
        var callback = {
            'ok':function(){
                $.ajax({
                    url:common_ops.buildUrl( "/switch/ops" ),
                    type:'POST',
                    data:{
                        act:act,
                        id:id
                    },
                    dataType:'json',
                    success:function( res ){
                        var callback = null;
                        if( res.code == 200 ){
                            callback = function(){
                                window.location.href = window.location.href;
                            }
                        }
                        common_ops.alert( res.msg,callback );
                    }
                });
            },
            'cancel':null
        };
        common_ops.confirm( ( act == "remove" ? "确定删除？":"确定恢复？" ), callback );
    }

};

$(document).ready( function(){
    sw_index_ops.init();
} );
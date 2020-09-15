;
var account_index_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;
        $(".warp_cron .start").click(function(){
              // $(".warp_cron").submit();
            var times=$("#crontime").val();
            that.cron( "start",times );
        });
        $(".warp_cron .stop").click(function(){
            that.cron( "stop");
        });

        $(".remove").click( function(){
            that.ops( "remove",$(this).attr("data") );
        } );

    },
    ops:function( act,id ){
        var callback = {
            'ok':function(){
                $.ajax({
                    url:common_ops.buildUrl( "/mon/ops" ),
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
    },
    cron:function( act, times){
         $.ajax({
            url:"/mon/cron",
            type:'POST',
            data:{
                act:act,
                time:times
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
     }
};

$(document).ready( function(){
    account_index_ops.init();
} );
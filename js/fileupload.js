// JavaScript File Upload
function FileUpload(elm_id){

    this.init = function(elm_id){
        if( $("#" + elm_id).size() == 0 ){
            return;
        }
    };

    this.judge_vocaloid_element = function(file_name){
        var tmp = file_name.split(".");
        var t_length = tmp.length;
        var file_type = tmp[t_length - 1];
        if( file_type == "vsq"  || file_type == "VSQ" ||
            file_type == "vsqx" || file_type == "VSQX") return true;
        return false;
    };

    this.del = function(){
        var files_info = document.getElementById('files_info');
        for(var i = 0; i < files_info.childNodes.length; ++i)
            files_info.removeChild(files_info.childNodes[i]);
    };

    this.hand_del = function(){
        var files_info = document.getElementById('files_info');
        for(var i = 0; i < files_info.childNodes.length; ++i)
            files_info.removeChild(files_info.childNodes[i]);
        $("#reset").click();
    };

    this.vocaloid_selected = function(file_name){
        var files_info = document.getElementById('files_info');

        var info_child = document.createElement('div');
        info_child.className = 'file_info';

        var img = document.createElement('img');
        img.setAttribute('src', 'images/howtouse.png');
        img.setAttribute('width', '80px');
        img.setAttribute('height', '80px');

        var span = document.createElement('span');
        span.className = 'file_title';

        var text = document.createTextNode(file_name);
        span.appendChild(text);

        var input = document.createElement('input');
        input.type = 'button';	input.value = '削除';
        input.setAttribute('id', 'del');
        input.setAttribute('onClick', 'vocarus.hand_del()');
        span.appendChild(input);

        files_info.appendChild(info_child);
        info_child.appendChild(img);
        info_child.appendChild(span);
    };

    this.init(elm_id);
};

var vocarus = new FileUpload('service');

$(function(){
    $("#upload_form").change(function(){
        var file_name = $('form input[name="file"]').val();
        //var file_name = $('form input[name="parts"]').val();

        if(vocarus.judge_vocaloid_element(file_name)){
            vocarus.del();
            vocarus.vocaloid_selected(file_name);
        }else{
            alert('ファイルが正しくありません。もう一度選択してください。');
        }

    });

});

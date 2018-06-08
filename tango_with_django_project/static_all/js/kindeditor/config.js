KindEditor.ready(function(K) {
    window.editor = K.create('#id_content',{

        width:'800px',
        height:'200px',
        uploadJson: '/admin/uploads/kindeditor',
    });
});
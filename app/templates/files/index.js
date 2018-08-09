updateMenu('#files');

var new_node_id = '';

var display_modal = function(obj){
    var parent_name = obj['text'];
    var node_id = obj['data']['nodeId']
    $("#node_id").val(node_id);
    $("#parent_name").val(parent_name);
    $("#basic").modal('show');
}

var update_node_server = function(node_id, node_name, action) {
    var url = '';
    if (action === "rename") {
        url = '{{ url_for('files.update_folder') }}';
        method = 'PUT';
        message = 'The folder was renamed sucessfully.';
    }
    if (action === "create") {
        url = '{{ url_for('files.create_folder') }}';
        method = 'POST';
        message = 'The folder was created sucessfully.';
    }

    name = node_name ? node_name : 'New node';
    $.ajax({
        url: url,
        dataType: 'json',
        type: method,
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({"name": name, "node_id": node_id}, null, '\t'),
        success: function( data, textStatus, jQxhr ){
            if (data['new_node_id']) {
                new_node_id = data['new_node_id']
            }
            if ([200, 201].includes(data['status_code'])) {
                window.location.href = data["redirect_url"];
            };
        },
        error: function( jqXhr, textStatus, errorThrown ){
            console.log(textStatus);
            console.log(jqXhr.status);
        }
    });
};

var update_node = function(e, data, action) {

    if ($('#' + data.node['id']).data('node-id')) {
        node_id = $('#' + data.node['id']).data('node-id');
    }else if (action === "create") {
        node_id = $('#' + data.node['parent']).data('node-id');
    }else{
        node_id = new_node_id;
    }

    update_node_server(node_id, data.text, action);
};

var UITree = function () {

    var context_menu = function(node) {
        console.log(node);
        var tree = $('#shared_by_me_tree').jstree(true);

        // The default set of all items
        var items = {
            "create": {
                "separator_before": true,
                "separator_after": true,
                "label": "Create folder here",
                "action": function (obj) {
                    display_modal(node);
                }
            },
            "rename": {
                "separator_before": true,
                "separator_after": true,
                "label": "Rename",
                "action": function (obj) {
                    tree.edit(node);
                }
            }
        };

        if (node['type'] == 'file') {
            delete items.create
        }


        return items;
    }

    var handleTree = function (id) {

        $('#'+id).jstree({
            "core" : {
                "themes" : {
                    "responsive": false
                },
                "multiple" : false,
                "check_callback" : true
            },
            "types" : {
                "folder" : {
                    "icon" : "fa fa-folder icon-state-info icon-lg"
                },
                "file" : {
                    "icon" : "fa fa-file icon-state-info icon-lg"
                }
            },
            "contextmenu": {items: context_menu},
            "plugins": ["types", "contextmenu"]
        });
    }

    $('#shared_by_me_tree').on('rename_node.jstree', function(e, data){
        update_node(e, data, 'rename');
    }).on('create_node.jstree', function (e, data) {
        update_node(e, data, 'create');
    });

    return {
        //main function to initiate the module
        init: function (id) {
            handleTree(id);
        }
    };

}();

if (App.isAngularJsApp() === false) {
    jQuery(document).ready(function() {
       UITree.init('shared_by_me_tree');
       UITree.init('shared_by_others_tree');
    });
};
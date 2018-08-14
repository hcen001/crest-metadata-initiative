updateMenu('#files');

$SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

var no_metadata = function() {
    $('#metadata-loading-info').hide();
    $('#tab-links').hide();
    $('#tab-content').hide();
    $('#additional-tab-links').hide();
    $('#additional-tab-content').hide();
    $('#additional-metadata').hide();
};

var activate_tab = function(tab, content){
    $(tab).fadeIn(1000, function(){
        var active_tab_id = $(content).find("div.active").attr("id");
        $(tab).find("a[href='#"+active_tab_id+"']").parent().addClass("active");
    });
    $(tab).fadeIn(1000);
    $(content).fadeIn(1000);
};

var display_modal = function(obj){
    var parent_name = obj['text'];
    var node_id = obj['data']['nodeId']
    $("#node_id").val(node_id);
    $("#parent_name").val(parent_name);
    $("#basic").modal('show');
};

var update_node_server = function(node_id, node_name, action) {
    var url = '';
    if (action === "rename") {
        url = '{{ url_for('files.update_folder') }}';
        method = 'PUT';
        message = 'The item was renamed sucessfully.';
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
            window.location.href = data["redirect_url"];
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

var update_metadata= function(metadata) {
    var meta = metadata.data;
    $('#title').text(meta.title);
    $('#shortname').text(meta.shortname);
    $('#abstract').text(meta.abstract ? meta.abstract : 'N/A');
    $('#begin_date').text(meta.start_date);
    $('#end_date').text(meta.end_date ? meta.end_date : 'N/A');
    $('#status').text(meta.status);
    $('#description').text(meta.geographic_location.description ? meta.geographic_location.description : 'N/A');
    $('#north').text(meta.geographic_location.northbound ? meta.geographic_location.northbound : 'N/A');
    $('#south').text(meta.geographic_location.southbound ? meta.geographic_location.southbound : 'N/A');
    $('#west').text(meta.geographic_location.westbound ? meta.geographic_location.westbound : 'N/A');
    $('#east').text(meta.geographic_location.eastbound ? meta.geographic_location.eastbound : 'N/A');
    if (meta.keywords) {
        meta.keywords.forEach(function(element){
            $('#keywords').append('<span class="label label-default">'+element+'</span> &nbsp;');
        });
    };
    $('#methods').text(meta.methods ? meta.methods : 'N/A');
    $('#comments').text(meta.comments ? meta.methods : 'N/A');
    if (meta.investigators) {
        meta.investigators.forEach(function(element){
            var tr = $('<tr></tr>');
            tr.append('<td>'+element.first_name+'</td>');
            tr.append(element.middle_initial ? '<td>'+element.middle_initial+'</td>' : '<td>N/A</td>');
            tr.append('<td>'+element.last_name+'</td>');
            tr.append(element.organization ? '<td>'+element.organization+'</td>' : '<td>N/A</td>');
            tr.append(element.email ? '<td>'+element.email+'</td>' : '<td>N/A</td>');
            tr.append(element.orcid_id ? '<td>'+element.orcid_id+'</td>' : '<td>N/A</td>');
            $('#investigators_tbl > tbody').append(tr);
        });
    };
    if (meta.personnel) {
        meta.personnel.forEach(function(element){
            var tr = $('<tr></tr>');
            tr.append('<td>'+element.first_name+'</td>');
            tr.append(element.middle_initial ? '<td>'+element.middle_initial+'</td>' : '<td>N/A</td>');
            tr.append('<td>'+element.last_name+'</td>');
            tr.append(element.organization ? '<td>'+element.organization+'</td>' : '<td>N/A</td>');
            tr.append(element.email ? '<td>'+element.email+'</td>' : '<td>N/A</td>');
            tr.append(element.orcid_id ? '<td>'+element.orcid_id+'</td>' : '<td>N/A</td>');
            tr.append(element.role ? '<td>'+element.role+'</td>' : '<td>N/A</td>');
            $('#personnel_tbl > tbody').append(tr);
        });
    };
    if (meta.funding) {
        meta.funding.forEach(function(element){
            var tr = $('<tr></tr>');
            tr.append('<td>'+element.first_name+'</td>');
            tr.append(element.middle_initial ? '<td>'+element.middle_initial+'</td>' : '<td>N/A</td>');
            tr.append('<td>'+element.last_name+'</td>');
            tr.append(element.orcid_id ? '<td>'+element.orcid_id+'</td>' : '<td>N/A</td>');
            tr.append(element.title_of_grant ? '<td>'+element.title_of_grant+'</td>' : '<td>N/A</td>');
            tr.append(element.funding_agency ? '<td>'+element.funding_agency+'</td>' : '<td>N/A</td>');
            tr.append(element.funding_id ? '<td>'+element.funding_id+'</td>' : '<td>N/A</td>');
            $('#funding_tbl > tbody').append(tr);
        });
    };
    if (meta.datatable) {
        meta.datatable.forEach(function(element){
            var tr = $('<tr></tr>');
            tr.append(element.column_name ? '<td>'+element.column_name+'</td>' : '<td>N/A</td>');
            tr.append(element.description ? '<td>'+element.description+'</td>' : '<td>N/A</td>');
            tr.append(element.explanation ? '<td>'+element.explanation+'</td>' : '<td>N/A</td>');
            tr.append(element.empty_code ? '<td>'+element.empty_code+'</td>' : '<td>N/A</td>');
            $('#datatable_tbl > tbody').append(tr);
        });
    };
    $('#metadata-loading-info').fadeOut(1000, function () {
        activate_tab('#tab-links', '#tab-content');
        activate_tab('#additional-tab-links', '#additional-tab-content');
        $('#additional-metadata').show();
    });
};

var load_metadata = function(metadata_id) {
    $.ajax({
        type: 'GET',
        url: $SCRIPT_ROOT + '/files/metadata',
        data: {
            metadata_id: metadata_id
        },
        success: function(data) {
            update_metadata(data);
        },
        error: function(error) {
            console.log(error);
        }
    });
};

var clean_metadata = function() {
    $('#title').empty();
    $('#shortname').empty();
    $('#abstract').empty();
    $('#keywords').empty();
    $('#methods').empty();
    $('#comments').empty();
    $('#begin_date').empty();
    $('#end_date').empty();
    $('#status').empty();
    $('#north').empty();
    $('#south').empty();
    $('#west').empty();
    $('#east').empty();
    $('#description').empty();
    $('#investigators_tbl > tbody').empty();
    $('#personnel_tbl > tbody').empty();
    $('#funding_tbl > tbody').empty();
    $('#datatable_tbl > tbody').empty();
};

var UITree = function () {

    var context_menu = function(node) {

        var tree = $('#shared_files_tree').jstree(true);

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
            },
            "upload": {
                "separator_before": true,
                "separator_after": true,
                "label": "Upload file here",
                "action": function (obj) {
                    console.log(node);
                }
            }
        };

        if (node['type'] == 'file') {
            delete items.create;
            delete items.upload;
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

    $('#shared_files_tree').on('rename_node.jstree', function(e, data){
        update_node(e, data, 'rename');
    }).on('create_node.jstree', function (e, data) {
        update_node(e, data, 'create');
    });

    $('#shared_files_tree').on('select_node.jstree', function(e, data) {
        var node_id = data.node.data.nodeId;
        if (data.node.type == "file") {
            $('#caption').hide();
            clean_metadata();
            var selected = $('#' + data.selected);
            if ( selected.data("metadata-id") ) {
                var metadata_id = selected.data("metadata-id");
                $('#no-metadata-info').hide();
                if (!$('#tab-content').is(':visible')) {
                    $('#metadata-loading-info').show();
                };
                load_metadata(metadata_id);
            }else{
                $('#no-metadata-info').show();
                $('#no-metadata-info').find('a').attr('href', $SCRIPT_ROOT + '/files/edit' + '?metadata_id=' + node_id);
                no_metadata();
            };
        }else{
            $('#metadata-loading-info').hide();
            $('#no-metadata-info').hide();
            no_metadata();
            $('#caption').show();
        };
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
       UITree.init('shared_files_tree');
    });
};
updateMenu('#files');

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
    $('#comments').text(meta.comments ? meta.comments : 'N/A');
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
    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
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

    var handleSample1 = function () {

        $('#tree').jstree({
            "core" : {
                "themes" : {
                    "responsive": false
                }
            },
            "types" : {
                "folder" : {
                    "icon" : "fa fa-folder icon-state-info icon-lg"
                },
                "file" : {
                    "icon" : "fa fa-file icon-state-info icon-lg"
                }
            },
            "plugins": ["types"]
        });

        // handle link clicks in tree nodes(support target="_blank" as well)
        $('#tree').on('select_node.jstree', function(e, data) {
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
                    no_metadata();
                };
            }else{
                $('#metadata-loading-info').hide();
                $('#no-metadata-info').hide();
                $('#metadata-info').hide();
                $('#additional-metadata').hide();
                $('#caption').show();
            };
        });
    }

    return {
        //main function to initiate the module
        init: function () {
            handleSample1();
        }
    };

}();

if (App.isAngularJsApp() === false) {
    jQuery(document).ready(function() {
       UITree.init();
    });
}
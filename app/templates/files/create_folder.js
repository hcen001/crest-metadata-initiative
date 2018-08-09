updateMenu('#files');

var UITree = function () {

    var handleSample1 = function () {

        $('#tree').jstree({
            "core" : {
                "themes" : {
                    "responsive": false
                }
            },
            "types" : {
                "default" : {
                    "icon" : "fa fa-folder icon-state-info icon-lg"
                },
                "file" : {
                    "icon" : "fa fa-file icon-state-info icon-lg"
                }
            },
            "plugins": ["types"]
        });

        // handle link clicks in tree nodes(support target="_blank" as well)
        $('#tree').on('select_node.jstree', function(e,data) {
            var link = $('#' + data.selected).find('a');
            if (link.attr("href") != "#" && link.attr("href") != "javascript:;" && link.attr("href") != "") {
                if (link.attr("target") == "_blank") {
                    link.attr("href").target = "_blank";
                }
                document.location.href = link.attr("href");
                return false;
            }
        });
    }

    $('#tree').on('select_node.jstree', function(e, data) {
        // console.log(data.selected);
        var node_id = $('#' + data.selected).data('node-id');
        $('#node_id').val(node_id);
    });

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
};
updateMenu('#files');

var FormWizard = function () {

    return {
        //main function to initiate the module
        init: function () {
            if (!jQuery().bootstrapWizard) {
                return;
            }

            var form = $('#submit_form');
            var error = $('.alert-danger', form);
            var success = $('.alert-success', form);

            form.validate({
                doNotHideMessage: true, //this option enables to show the error/success messages on tab switch.
                errorElement: 'span', //default input error message container
                errorClass: 'help-block help-block-error', // default input error message class
                focusInvalid: false, // do not focus the last invalid input
                rules: {
                },

                errorPlacement: function (error, element) { // render error placement for each input type
                    if (element.hasClass("select2")) {
                        error.insertAfter(element.next());
                    } else if (element.attr("name") == "file") {
                        error.insertAfter(element.parent().parent());
                    } else if (element.parent().hasClass("date-picker")){
                        error.insertAfter(element.parent());
                    } else {
                        error.insertAfter(element); // for other inputs, just perform default behavior
                    }
                },

                invalidHandler: function (event, validator) { //display error alert on form submit
                    success.hide();
                    error.show();
                    App.scrollTo(error, -200);
                },

                highlight: function (element) { // hightlight error inputs
                    $(element).closest('.form-group').removeClass('has-success').addClass('has-error'); // set error class to the control group
                },

                unhighlight: function (element) { // revert the change done by hightlight
                    $(element).closest('.form-group').removeClass('has-error'); // set error class to the control group
                },

                success: function (label) {
                    if (label.attr("for") == "file" || label.attr("for") == "payment[]") { // for checkboxes and radio buttons, no need to show OK icon
                        label.closest('.form-group').removeClass('has-error').addClass('has-success');
                        label.remove(); // remove error label here
                    } else { // display success icon for other inputs
                        label
                            .addClass('valid') // mark the current input as valid and display OK icon
                        .closest('.form-group').removeClass('has-error').addClass('has-success'); // set success class to the control group
                    }
                },

                submitHandler: function (form) {
                    success.show();
                    error.hide();
                    form.submit();
                    //add here some ajax code to submit your form or just call form.submit() if you want to submit the form without ajax
                }

            });

            var displayConfirm = function() {
                $('#tab2 .form-control-static', form).each(function(){
                    var tables = ["investigators", "personnel", "funding", "datatable"];
                    var table = $(this).attr("data-display");
                    if ( tables.includes(table) ) {
                        var tbl = $(this).find("table > tbody");
                        var items = $('#'+table).repeaterVal();
                        if (table == "investigators") {
                            items['investigators'].forEach(function(element){
                                var tr = $('<tr></tr>');
                                tr.append('<td>'+element.first_name+'</td>');
                                tr.append(element.middle_initial ? '<td>'+element.middle_initial+'</td>' : '<td>N/A</td>');
                                tr.append('<td>'+element.last_name+'</td>');
                                tr.append(element.organization ? '<td>'+element.organization+'</td>' : '<td>N/A</td>');
                                tr.append(element.email ? '<td>'+element.email+'</td>' : '<td>N/A</td>');
                                tr.append(element.orcid_id ? '<td>'+element.orcid_id+'</td>' : '<td>N/A</td>');
                                tbl.append(tr);
                            });
                        };
                        if (table == "personnel") {
                            items['personnel'].forEach(function(element){
                                var tr = $('<tr></tr>');
                                tr.append('<td>'+element.first_name+'</td>');
                                tr.append(element.middle_initial ? '<td>'+element.middle_initial+'</td>' : '<td>N/A</td>');
                                tr.append('<td>'+element.last_name+'</td>');
                                tr.append(element.organization ? '<td>'+element.organization+'</td>' : '<td>N/A</td>');
                                tr.append(element.email ? '<td>'+element.email+'</td>' : '<td>N/A</td>');
                                tr.append(element.orcid_id ? '<td>'+element.orcid_id+'</td>' : '<td>N/A</td>');
                                tr.append(element.role ? '<td>'+element.role+'</td>' : '<td>N/A</td>');
                                tbl.append(tr);
                            });
                        };
                        if (table == "funding") {
                            items['funding'].forEach(function(element){
                                var tr = $('<tr></tr>');
                                tr.append('<td>'+element.first_name+'</td>');
                                tr.append(element.middle_initial ? '<td>'+element.middle_initial+'</td>' : '<td>N/A</td>');
                                tr.append('<td>'+element.last_name+'</td>');
                                tr.append(element.orcid_id ? '<td>'+element.orcid_id+'</td>' : '<td>N/A</td>');
                                tr.append(element.title_of_grant ? '<td>'+element.title_of_grant+'</td>' : '<td>N/A</td>');
                                tr.append(element.funding_agency ? '<td>'+element.funding_agency+'</td>' : '<td>N/A</td>');
                                tr.append(element.funding_id ? '<td>'+element.funding_id+'</td>' : '<td>N/A</td>');
                                tbl.append(tr);
                            });
                        };
                        if (table == "datatable") {
                            items['datatable'].forEach(function(element){
                                var tr = $('<tr></tr>');
                                tr.append(element.column_name ? '<td>'+element.column_name+'</td>' : '<td>N/A</td>');
                                tr.append(element.description ? '<td>'+element.description+'</td>' : '<td>N/A</td>');
                                tr.append(element.explanation ? '<td>'+element.explanation+'</td>' : '<td>N/A</td>');
                                tr.append(element.empty_code ? '<td>'+element.empty_code+'</td>' : '<td>N/A</td>');
                                tbl.append(tr);
                            });
                        };
                    }
                    var input = $('[name="'+$(this).attr("data-display")+'"]', form);
                    if (input.is(":text") || input.is("textarea")) {
                        if ($(this).attr("data-display") == "additional_keywords") {
                            var additional_keywords = $("#additional_keywords").tagsinput('items');
                            additional_keywords.forEach(function(element){
                                $('#keywords_info').append('<span class="label label-default">'+element+'</span> &nbsp;');
                            });
                            return;
                        };
                        $(this).html(input.val());
                    } else if (input.is("select")) {
                        if ($(this).attr("data-display") == "keywords") {
                            var keywords = $('#'+$(this).attr("data-display")).select2('data');
                            keywords.forEach(function(element){
                                $('#keywords_info').append('<span class="label label-default">'+element.text+'</span> &nbsp;');
                            });
                        };
                        if ($(this).attr("data-display") == "status") {
                            var selected_status = $('#'+$(this).attr("data-display")).select2('data');
                            $(this).html(selected_status[0].text);
                        };
                    }
                });
            }

            var handleTitle = function(tab, navigation, index) {
                var total = navigation.find('li').length;
                var current = index + 1;
                // set wizard title
                $('.step-title', $('#upload_wizard')).text('Step ' + (index + 1) + ' of ' + total);
                // set done steps
                jQuery('li', $('#upload_wizard')).removeClass("done");
                var li_list = navigation.find('li');
                for (var i = 0; i < index; i++) {
                    jQuery(li_list[i]).addClass("done");
                }

                if (current == 1) {
                    $('#upload_wizard').find('.button-previous').hide();
                } else {
                    $('#upload_wizard').find('.button-previous').show();
                }

                if (current >= total) {
                    $('#upload_wizard').find('.button-next').hide();
                    $('#upload_wizard').find('.button-submit').show();
                    displayConfirm();
                } else {
                    $('#upload_wizard').find('.button-next').show();
                    $('#upload_wizard').find('.button-submit').hide();
                }
                App.scrollTo($('.page-title'));
            }

            // default form wizard
            $('#upload_wizard').bootstrapWizard({
                'nextSelector': '.button-next',
                'previousSelector': '.button-previous',
                onTabClick: function (tab, navigation, index, clickedIndex) {
                    return false;

                    success.hide();
                    error.hide();
                    if (form.valid() == false) {
                        return false;
                    }

                    handleTitle(tab, navigation, clickedIndex);
                },
                onNext: function (tab, navigation, index) {
                    success.hide();
                    error.hide();

                    if (form.valid() == false) {
                        return false;
                    }

                    handleTitle(tab, navigation, index);
                },
                onPrevious: function (tab, navigation, index) {
                    success.hide();
                    error.hide();

                    handleTitle(tab, navigation, index);
                },
                onTabShow: function (tab, navigation, index) {
                    var total = navigation.find('li').length;
                    var current = index + 1;
                    var $percent = (current / total) * 100;
                    $('#upload_wizard').find('.progress-bar').css({
                        width: $percent + '%'
                    });
                }
            });

            $('#upload_wizard').find('.button-previous').hide();
            $('#upload_wizard .button-submit').click(function () {
                $(form).submit();
            }).hide();

            //apply validation on select2 dropdown value change, this only needed for chosen dropdown integration.
            $('.select2', form).change(function () {
                form.validate().element($(this)); //revalidate the chosen dropdown value and show error or success message for the input
            });

        }

    };

}();

var FormRepeater = function () {

    return {
        //main function to initiate the module
        init: function () {
            $('.mt-repeater').each(function(){
                $(this).repeater({
                    show: function () {
                        $(this).slideDown();
                    },

                    hide: function (deleteElement) {
                        if(confirm('Are you sure you want to delete this element?')) {
                            $(this).slideUp(deleteElement);
                        }
                    },

                    ready: function (setIndexes) {

                    }

                });
                {% if data is defined %}
                    if ($(this).attr('id') == 'investigators' && investigators !== undefined) {
                        $(this).repeater().setList({{ data['investigators'] }});
                    };
                    if ($(this).attr('id') == 'personnel') {
                        $(this).repeater().setList({{ data['personnel'] }});
                    };
                    if ($(this).attr('id') == 'funding') {
                        $(this).repeater().setList({{ data['funding'] }});
                    };
                    if ($(this).attr('id') == 'datatable') {
                        $(this).repeater().setList({{ data['datatable'] }});
                    };
                {% endif %}
            });
        },

        populate: function(data) {
            $()
        }

    };

}();

var handleSelect2 = function () {
    // Set the "bootstrap" theme as the default theme for all Select2
    // widgets.
    //
    // @see https://github.com/select2/select2/issues/2927
    $.fn.select2.defaults.set("theme", "bootstrap");

    $("#status").select2({
        allowClear: true,
        placeholder: "Select project's status",
        width: null
    });

    $("#keywords").select2({
        placeholder: "Select keywords",
        allowClear: true,
        width: null
    });

    // copy Bootstrap validation states to Select2 dropdown
    //
    // add .has-waring, .has-error, .has-succes to the Select2 dropdown
    // (was #select2-drop in Select2 v3.x, in Select2 v4 can be selected via
    // body > .select2-container) if _any_ of the opened Select2's parents
    // has one of these forementioned classes (YUCK! ;-))
    $(".select2").on("select2:open", function() {
        if ($(this).parents("[class*='has-']").length) {
            var classNames = $(this).parents("[class*='has-']")[0].className.split(/\s+/);

            for (var i = 0; i < classNames.length; ++i) {
                if (classNames[i].match("has-")) {
                    $("body > .select2-container").addClass(classNames[i]);
                }
            }
        }
    });
}

var ComponentsDateTimePickers = function () {

    var handleDatePickers = function () {

        if (jQuery().datepicker) {
            $('#start_date, #end_date').datepicker({
                rtl: App.isRTL(),
                orientation: "left",
                autoclose: true
            }).on('changeDate', function(ev){
                if (ev.target.id == "start_date") {
                    $("#end_date").val("");
                    $("#end_date").prop("disabled", false);
                    $("#end_date").datepicker("setStartDate", ev.target.value)
                }
                $(this).valid();
            });;
            //$('body').removeClass("modal-open"); // fix bug when inline picker is used in modal
        }

        $("#end_date").prop("disabled", true);
    }

    return {
        //main function to initiate the module
        init: function () {
            handleDatePickers();
        }
    };

}();

if (App.isAngularJsApp() === false) {
    jQuery(document).ready(function() {
       ComponentsDateTimePickers.init();
       FormWizard.init();
       FormRepeater.init();
       handleSelect2();
    });
};

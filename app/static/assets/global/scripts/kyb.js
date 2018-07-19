var updateMenu = function(menuId, subMenuId) {
    $(menuId).children().append('<span class="selected"></span>')
    $(menuId).addClass('active open')
    $('.nav-item').not(menuId).removeClass('start active open')
    $('.nav-item').not(menuId).children().find('.selected').remove()

    if (subMenuId !== "") {
        $(subMenuId).children().append('<span class="selected"></span>')
        $(subMenuId).addClass('active open')
    };
}
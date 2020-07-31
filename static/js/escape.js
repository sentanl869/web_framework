let HTMLEscaped = function (title) {
    let content = '';
    if (title.length === 0) {
        return content;
    } else {
        content = title.replace(/&/g, '&amp;');
        content = content.replace(/</g, '&lt;');
        content = content.replace(/>/g, '&gt;');
        content = content.replace(/ /g, '&nbsp;');
    }

    return content;
};
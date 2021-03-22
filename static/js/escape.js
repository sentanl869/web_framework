let HTMLEscaped = (title) => {
    let content = ''
    if (title.length === 0) {
        return content
    } else {
        content = title.replace(/&/g, '&amp;')
        content = content.replace(/</g, '&lt;')
        content = content.replace(/>/g, '&gt;')
        content = content.replace(/ /g, '&nbsp;')
        content = content.replace(/"/g, '&quot;')
        content = content.replace(/'/g, '&#x27;')
    }
    return content
}
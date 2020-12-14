function debounce(func, wait = 150, early = false) {
    let timeout;
    return function (...args) {
        const context = this;
        const isEarlyEnable = !timeout && early;
        const executor = function () {
            timeout = null;
            !early && func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(executor, wait);
        isEarlyEnable && func.apply(context, args);
    };
}

function split_from_to_end(str, delim) {
    return str.slice(str.indexOf(delim) + delim.length);
}

export {debounce, split_from_to_end};
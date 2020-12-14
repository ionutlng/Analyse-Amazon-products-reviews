import {debounce, split_from_to_end} from './utils.js';

function autocomplete(inp, arr) {
    function addActive(autocomplete_list) {
        if (!autocomplete_list) return false;
            removeActive(autocomplete_list);
        if (currentFocus >= autocomplete_list.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (autocomplete_list.length - 1);
        autocomplete_list[currentFocus].classList.add("autocomplete-active");
    };

    function removeActive(autocomplete_list) {
        for (var i = 0; i < autocomplete_list.length; i++) {
            autocomplete_list[i].classList.remove("autocomplete-active");
        }
    };

    function closeAllLists(element) {
        var autocomplete_items = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < autocomplete_items.length; i++) {
            if (element != autocomplete_items[i] && element != inp) {
                autocomplete_items[i].parentNode.removeChild(autocomplete_items[i]);
            }
        }
    };

    let currentFocus;
    let suggestion_div, element_div, i, val = inp.value;

    closeAllLists();
    if (!val) { return false; }
    currentFocus = -1;

    suggestion_div = document.createElement("DIV");
    suggestion_div.setAttribute("id", inp.id + "autocomplete-list");
    suggestion_div.setAttribute("class", "autocomplete-items");

    inp.parentNode.appendChild(suggestion_div);

    for (i = 0; i < arr.length; i++) {
        element_div = document.createElement("DIV");
        element_div.innerHTML = split_from_to_end(arr[i], ',');
        element_div.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
        element_div.addEventListener("click", function (e) {
            const elem = this.getElementsByTagName("input");
            inp.value = split_from_to_end(elem[0].value,',');
            inp.setAttribute("custom_tag", elem[0].value.split(',',1));
            closeAllLists();
            document.getElementById('search_btn').click();
        });
        suggestion_div.appendChild(element_div);
    }

    inp.addEventListener("keydown", function (event) {
        var autocomplete_list = document.getElementById(this.id + "autocomplete-list");
        if (autocomplete_list) autocomplete_list = autocomplete_list.getElementsByTagName("div");
        if (event.keyCode == 40) {
            currentFocus++;
            addActive(autocomplete_list);
        } else if (event.keyCode == 38) {
            currentFocus--;
            addActive(autocomplete_list);
        } else if (event.keyCode == 13) {
            if (currentFocus > -1) {
                if (autocomplete_list) {
                    autocomplete_list[currentFocus].click();
                    document.getElementById('search_btn').click();
                }
            }
        }
    });

    document.addEventListener("click", function (event) {
        closeAllLists(event.target);
    });
};

function autocomplete_listener(event){
    let target_element = event.target;
    let input = target_element.value;
    if (input.trim() != '') {
        input = input.replace(/ /gi, "_");
        let api_url = `${window.location.origin}/get/items/${input}/`;
        fetch(api_url)
            .then(r => r.json())
            .then(t => autocomplete(target_element, t))
            .catch(e => console.log(e));
    }
}

function add_autocomplete_listener(element) {
    element.addEventListener("input", debounce(function (e) {
        autocomplete_listener(e);
    }));
}

add_autocomplete_listener(document.getElementById('item_search'))
function build_item_detail_table(fetched_table){
    let table = document.getElementById("item_details");
    table.innerHTML = fetched_table;
}

function get_item() {
    const input = document.getElementById('item_search');
    if (input.hasAttribute('custom_tag')){
        fetch(`${window.location.origin}/items/${input.getAttribute('custom_tag')}`)
            .then(r => r.text())
            .then(t => build_item_detail_table(t))
            .catch(e => console.log(e))
    }
}
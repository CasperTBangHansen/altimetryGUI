var products;

async function getData(resolution_name, product_name, start_date, end_date) {
    const URL = `https://orange-island-0aafb1f03.2.azurestaticapps.net/api/GetData?resolution_name=${resolution_name}&product_name=${product_name}&start_date=${start_date}&end_date=${end_date}`;
    // Process data from api
    await fetch(URL)
    .then(response => {
        if (response.status == 200) {
            return response;
        }
        throw new Error(response);
    })
    .then(products => {
        if(products['status'] === "success" && products['type'] === "both"){
            return products['file'];
        }
        throw new Error(products);
    }).then(file => {
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(file);
        link.download = "AltimetryGridding.zip";
        link.click();
    })
    .catch(err => {});
}

async function get_products() {
    const URL ='https://orange-island-0aafb1f03.2.azurestaticapps.net/api/GetProducts?resolution=true';
    // Process data from api
    return await fetch(URL)
    .then(response => {
        if (response.status == 200) {
            return response.json();
        }
        throw new Error(response);
    })
    .then(products => {
        if(products['status'] === "success" && products['type'] === "both"){
            let data = {};
            products['products'].forEach(function (item, index) {
                if (item['product_name'] in data){
                    data['product_name'].append(item);
                } else {
                    data[item['product_name']] = [item]
                }
            });
            return data;
        }
        throw new Error(products);
    })
    .catch(err => {});
}

function make_product_dropdowns(){
    if (Object.keys(products).length == 0){
        return;
    }
    var dropdown = document.querySelector('#product-dropdown');
    let elements = [];
    for (let key in products) {
        let a = document.createElement("a");
        a.href = "#";
        a.onclick = function() { make_resolution(key); };
        a.className = "dropdown-a";
        a.textContent = key;
        elements.push(a)
    };
    dropdown.replaceChildren(...elements)
}

function format_resolution(resolution){
    var div = document.createElement("div");
    div.className = "dropdown-set-attrs"
    var p_title = document.createElement("p")
    var p_time = document.createElement("p")
    var p_lon = document.createElement("p")
    var p_lat = document.createElement("p")
    p_title.textContent = resolution["resolution_name"];
    p_title.style.fontWeight = 900;
    p_time.textContent =  `Time resolution: ${resolution["time_days"]}`;
    p_lon.textContent =  `Longitude resolution: ${resolution["x"]}`;
    p_lat.textContent =  `Latitude resolution: ${resolution["y"]}`;
    div.replaceChildren(p_title, p_time, p_lon, p_lat);
    return div;
}
function make_resolution(product){
    var dropdown = document.querySelector('#product-dropdown-label');
    document.querySelector('#product-dropdown-input').checked = false;
    dropdown.textContent = product;
    dropdown.dataset.product = product;

    if (Object.keys(products).length == 0){
        return;
    }
    var dropdown = document.querySelector('#resolution-dropdown');
    let elements_a = [];
    for (let key in products[product]) {
        let resolution = products[product][key];
        let a = document.createElement("a");
        a.append(format_resolution(resolution));
        a.href = "#";
        a.className = "dropdown-a";
        a.onclick = function() { set_resolution(resolution["resolution_name"]);};
        elements_a.push(a)
    };
    dropdown.replaceChildren(...elements_a)
}
function set_resolution(resolution){
    document.querySelector('#resolution-dropdown-input').checked = false;
    var resolution_label = document.querySelector('#resolution-dropdown-label');
    resolution_label.textContent = resolution;
    resolution_label.dataset.resolution = resolution;
    check_download_button();
}

function check_download_button(){
    // Check all values have been set
    var download_button = document.querySelector(".download_button");
    if (!document.querySelector('#product-dropdown-label').dataset.product){
        download_button.style.display = "none";
        return;
    }
    if (!document.querySelector('#resolution-dropdown-label').dataset.resolution){
        download_button.style.display = "none";
        return;
    }
    if (!document.querySelector('#start-date div a').dataset.date){
        download_button.style.display = "none";
        return;
    }
    if (!document.querySelector('#end-date div a').dataset.date){
        download_button.style.display = "none";
        return;
    }
    download_button.style.display = "";
    download_button.onclick = download;
}

function download(){
    var prod = document.querySelector('#product-dropdown-label').dataset.product;
    var res = document.querySelector('#resolution-dropdown-label').dataset.resolution;
    var start_date = document.querySelector('#start-date div a').dataset.date;
    var end_date = document.querySelector('#end-date div a').dataset.date;
    start_date = '2004-06-10'
    end_date = '2004-06-12'
    getData(res, prod, start_date, end_date);
}



async function setup(){
    products = await get_products();
    make_product_dropdowns(products);
}
setup();
eel.expose(say_hello_js);               // Expose this function to Python

function say_hello_js(x) {
    console.log("Hello from JS " + x);
}

/*var el = document.getElementById('tabmenu');
        var instance = M.Tabs.init(el);*/


// document.getElementById("filepicker").addEventListener("change", function (event) {
//     //let output = document.getElementById("listing");
//     let files = event.target.files;
//     console.log(files.result);
//     console.log(files.URL);
//     console.log(event.target.webkitRelativePath);
//     var tmppath = URL.createObjectURL(event.target.files[0]);
//     console.log(tmppath);
//     /*window.requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;
//     console.log(window.requestFileSystem);
//     window.directoryEntry = window.directoryEntry || window.webkitDirectoryEntry;
//     console.log(window.directoryEntry);*/

//     for (let i = 0; i < files.length; i++) {
//         console.log(files[i].webkitRelativePath);
//         /*let item = document.createElement("li");
//         item.innerHTML = files[i].webkitRelativePath;
//         output.appendChild(item);*/
//     };
// }, false);


async function pick_file() {
    let folder = document.getElementById('input-box').value;
    let file_div = document.getElementById('file-name');

    // Call into Python so we can access the file system
    let random_filename = await eel.pick_file(folder)();
    file_div.innerHTML = random_filename;
}

// document.addEventListener('DOMContentLoaded', function () {
//     var elems = document.querySelectorAll('.modal');
//     var instances = M.Modal.init(elems, options);
// });


async function getFolder(id) {
    var path = await eel.btn_dir_path()();
    if (path) {
        //console.log(dosya_path);
        document.getElementById(id).value = path;
    }
}

async function read_invoices(folder, zip, type) {
    var data = await eel.read_invoices(folder, zip, type)();

    //console.log(data.errors.length);
    //console.log(data.result.length);

    if (data.result.length != 0 && data.result != undefined) {

        badage_res = document.getElementById('badage_res');
        badage_res.innerHTML = data.result.length - 1;

        const txt_a1 = document.getElementById('textarea1');
        set_lines_textarea(txt_a1, data.result);

    }


    badage_err = document.getElementById('badage_err');
    badage_err.innerHTML = data.errors.length;
    const txt_a2 = document.getElementById('textarea2');

    if (data.errors.length != 0 && data.errors != undefined) {
        set_lines_textarea(txt_a2, data.errors);
    }
    else {
        txt_a2.value = "";
    }

    show_loader('preload',false);
    show_exp_list('expandible_list',true);


}

function set_lines_textarea(el, data) {
    el.value = "";
    for (entry of data) {
        el.value += entry + '\r\n';
    }
}



// document.getElementById("btnRanPick").onclick = function () {
//     pick_file();
// };

function show_exp_list(id, value) {
    exp_list = document.getElementById(id);

    if (value) {
        exp_list.classList.remove('hide');
    }
    else {
        exp_list.classList.add('hide');
    }

}



function isEmpty(el) {
    var field = el.value;
    return (field == null || field == "");
}



function show_loader(id, value) {
    var loading = document.getElementById(id);
    var hiddenClass = 'hide'
    if (value) {
        loading.classList.remove(hiddenClass);
    }
    else {
        loading.classList.add(hiddenClass);
    }

}


async function save_csv_file(content) {

    var file_path = await eel.dialog_save_csv()();
    if (file_path) {
        //console.log(file_path);
        await eel.save_text_file(file_path, content)();
    }
}
    

function init_components(){

    document.getElementById("btnRead").onclick = function () {

        show_exp_list('expandible_list',false);
    
        var path = document.getElementById('input-box');
        var zip = document.getElementById('chkZip').checked;
        var type = document.getElementById('selType');
    
        if (isEmpty(path)) {
            path.classList.add('invalid');
            path.focus();
            return false;
        } else {
            path.classList.remove('invalid')
        }
    
        show_loader('preload',true);
    
        if (isEmpty(type)) {
            type.value = 'P';
        }
    
        /*console.log(path.value);
        console.log(zip);
        console.log(type.value);*/
    
        read_invoices(path.value, zip, type.value)
    
        // let random_filename = await eel.read_invoices(folder, zip, type)();
        // file_div.innerHTML = random_filename;
    };

    document.getElementById('btnPath').addEventListener('click', function () {
        getFolder('input-box');
    });

    document.getElementById("btnSave").onclick = function () {
        content = document.getElementById('textarea1');
        save_csv_file(content.value);
    }


    document.getElementById('btn_sort_input').addEventListener('click', function(){
        getFolder('input-sort-box');
    });

    document.getElementById('btn_sort_output').addEventListener('click', function(){
        getFolder('output-sort-box');
    });


    document.getElementById('btn_sort_action').addEventListener('click', function(){
        classify_invoices();
    });

    // var elem = document.querySelector('.collapsible.expandable');
    // var instance = M.Collapsible.init(elem, {
    //     accordion: true
    // });
    

}

async function classify_invoices() {

    show_exp_list('expandible_list1',false);

    source = document.getElementById('input-sort-box');
    target = document.getElementById('output-sort-box');
    var zip = document.getElementById('chkZip1').checked;


    if(validate_empty_path(source)){
        return true;  
    }
    if(validate_empty_path(target)){
        return true;  
    }

    if(source.value.normalize() === target.value.normalize()){
        source.value = '';
        target.value = '';
        alert('Source and Target fields must to have a different paths');
        return true;
    }

    //console.log(source.value);
    //console.log(target.value);

    
    show_loader('preload2', true);
    
    var data = await eel.classify_invoices(source.value, target.value, zip)();

    //console.log(data.errors.length);
    //console.log(data.result.length);

    badage_res = document.getElementById('badage_res1');
    badage_res.innerHTML = data.result.length;

    if (data.result.length != 0 && data.result != undefined) {

        const txt_a3 = document.getElementById('textarea3');
        set_lines_textarea(txt_a3, data.result);

    }

    badage_err = document.getElementById('badage_err1');
    badage_err.innerHTML = data.errors.length;
    const txt_a4 = document.getElementById('textarea4');

    if (data.errors.length != 0 && data.errors != undefined) {
        set_lines_textarea(txt_a4, data.errors);
    }
    else {
        txt_a4.value = "";
    }

    show_loader('preload2', false);
    show_exp_list('expandible_list1',true);
}

function validate_empty_path(el){
    
    if (isEmpty(el)) {
        el.classList.add('invalid');
        el.focus();
        return true;
    } else {
        el.classList.remove('invalid');
    }
}

init_components();

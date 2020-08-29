function getChildNumber(node) {
    return Array.prototype.indexOf.call(node.parentNode.children, node);
}

function createUsersTable(users, changed, to_delete) {
    let table = document.querySelector('.users>table>tbody');
    for (let i = 0; i < users.length; ++i) {
        let row = document.createElement('tr');
        let username = document.createElement('td');
        let author = document.createElement('td');
        let admin = document.createElement('td');
        username.innerText = users[i]['username'];

        let author_checkbox = document.createElement('input');
        author_checkbox['type'] = 'checkbox';
        author_checkbox['className'] = 'author_checkbox';
        author_checkbox.checked = users[i]['is_author'];
        author_checkbox.onclick = (e) => {
            if (changed[i]['author']) {
                delete changed[i].author;
            } else {
                changed[i]['author'] = !users[i]['is_author'];
            }
        };
        author.appendChild(author_checkbox);

        let admin_checkbox = document.createElement('input');
        admin_checkbox['type'] = 'checkbox';
        admin_checkbox['className'] = 'admin_checkbox';
        admin_checkbox.checked = users[i]['is_admin'];
        admin_checkbox.onclick = (e) => {
            if (changed[i]['admin']) {
                delete changed[i].author;
            } else {
                changed[i]['admin'] = !users[i]['is_admin'];
            }
        };
        admin.appendChild(admin_checkbox);


        row.appendChild(username);
        row.appendChild(author);
        row.appendChild(admin);

        table.appendChild(row);
    }
}

function ajax_post(url, data, callback) {
    let xhr = new XMLHttpRequest();
    xhr.onload = () => {
        if (xhr.status == 200) {
            let data = {};
            try {
                data = JSON.parse(xhr.responseText);
            } catch(e) {
                console.log(e.message + " in " + xhr.responseText);
                return;
            }
            callback(data);
        }
    };
    let formData = new FormData();
    for (let key in data) {
        formData.append(key,data[key]);
    }
    xhr.open("POST", url, true);
    xhr.send(formData);
}

function updateUsersTable(changed,to_delete) {
    let commit = document.querySelector(".users>input[type='button']");
    let data = {
        'changed':JSON.stringify(changed)
    };
    commit.onclick = (e) => {
        ajax_post('/api/update_users', data, () => {
            console.log('updated')
        });
    };
}

function makeMenu() {
    let menu = document.querySelector('.admin_menu>ul');
    let current = document.querySelector('.admin_menu .current')
    menu.childNodes.forEach((item, i) => {
        item.onclick = (e) => {
            if (item.className == "current") {
                return;
            }
            item.className = "current";
            let curNumber = getChildNumber(current);
            let curSection = document.querySelector('.admin_wrapper').children[curNumber + 1];
            curSection.classList.toggle('hidden');
            console.log(curSection);
            console.log(curSection.classList);
            console.log(curSection.className);
            let newNumber = getChildNumber(e.target);
            let newSection = document.querySelector('.admin_wrapper').children[newNumber + 1];
            newSection.classList.toggle('hidden');
            current.className = "";
            current = item;
        };
    });
}

function ajax(url, callback) {
    let xhr = new XMLHttpRequest();
    xhr.onload = () => {
        if (xhr.status == 200) {
            let data = {};
            try {
                data = JSON.parse(xhr.responseText);
            } catch(e) {
                console.log(e.message + " in " + xhr.responseText);
                return;
            }
            callback(data);
        }
    };
    xhr.open("GET", url, true);
    xhr.send();
}

function descriptionChange() {
    let desc_field = document.getElementsByName('desc')[0];
    ajax_post('/api/update_desc', {'text':desc_field.value}, (e) => {desc_field.value = "";});
}


let users = [{
        'username': 'admin',
        'is_author': true,
        'is_admin': true,
    },
    {
        'username': 'anton',
        'is_author': true,
        'is_admin': false,
    },
    {
        'username': 'BrokenTimer',
        'is_author': false,
        'is_admin': false,
    },
];
let changed = [];
let to_delete = [];
window.onload = () => {
    ajax("/api/get_users", (data) => {
        users = data;
        for (let i = 0; i<users.length;++i) {
            changed.push({});
        }
        createUsersTable(users,changed,to_delete);
    });

    updateUsersTable(changed,to_delete);

    makeMenu();

    document.querySelector('input[value="Сохранить"]').onclick = descriptionChange;
};
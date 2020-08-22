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
        let ban = document.createElement('td');
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

        let ban_button = document.createElement('input');
        ban_button['type'] = 'button';
        ban_button['value'] = 'Забанить';
        ban_button['className'] = 'ban_button';
        ban_button.onclick = (e) => {
            if (to_delete.includes(i)) {
                to_delete = to_delete.filter((v) => {
                    return v != i
                });
                e.target['className'] = 'banButton';
                e.target['value'] = 'Забанить';
                return;
            }
            to_delete.push(i);
            e.target['className'] += ' banned';
            e.target['value'] = 'Забанен';
        };
        ban.appendChild(ban_button);

        row.appendChild(username);
        row.appendChild(author);
        row.appendChild(admin);
        row.appendChild(ban);

        table.appendChild(row);
    }
}

function ajax_post(url, changed, callback) {
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
    formData.append('changed', JSON.stringify(changed));
    xhr.open("POST", url, true);
    xhr.send(formData);
}

function updateUsersTable(changed,to_delete) {
    let commit = document.querySelector(".users>input[type='button']");
    commit.onclick = (e) => {
        ajax_post('/api/update_users', changed, () => {
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
};
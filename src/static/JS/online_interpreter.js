let visible = false;

document.getElementsByClassName('code-button')[0].onclick = function(event) {
    let terminal = document.getElementsByClassName('terminal')[0];
    let run_button = document.getElementsByClassName('code-run-button')[0];   
    let terminal_icon = document.getElementsByClassName('terminal-icon')[0];
    // если терминал невидим, то показываем
    // если терминал видим, то скрываем 
    if (visible) {
        terminal.style.display = 'none';
        run_button.style.display = 'none';
        terminal_icon.style.display = 'none';
        visible = false;
    } else {
        terminal.style.display = 'block';
        run_button.style.display = 'block';
        terminal_icon.style.display = 'block';
        visible = true;
    }
}

// отправляем код на сервер где он выполнится и пришлет нам поток вывода и ошибок
document.getElementsByClassName('code-run-button')[0].onclick = function(event) {
    let terminal = document.getElementsByClassName('terminal')[0];
    let formData = new FormData(document.forms.textform);
    let data = JSON.stringify(Object.fromEntries(formData));
    terminal.textContent = 'Загрузка...';
    fetch('/execute_code/', {
        method: 'POST',
        headers: {
        'X-CSRFToken': csrfCookie // Установка CSRF-токена в заголовок
        },
        body: data
    })
    .then(response => response.json())
    .then(data => {
        terminal.textContent = data.stdout + '\n' + data.stderr;
    })
}

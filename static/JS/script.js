const datePicker = document.getElementById('datePicker');
const today = new Date();
const tomorrow = new Date(today);
const default_date = new Date();
tomorrow.setDate(tomorrow.getDate() + 1); // Завтрашний день
const maxDate = new Date(tomorrow);
maxDate.setDate(maxDate.getDate() + 19); // 14 дней после завтрашнего дня
default_date.setDate(default_date.getDate() + 6)

datePicker.min = tomorrow.toISOString().split('T')[0];
datePicker.max = maxDate.toISOString().split('T')[0];
datePicker.value = default_date.toISOString().split('T')[0];


function closeMessageBox() {
    var messageBox = document.getElementById('messageBox');
    messageBox.style.display = 'none';
}

var textarea = document.querySelector('textarea');

function autoResize() {
  textarea.style.height = '59vh';
  textarea.style.height = textarea.scrollHeight + 'px';
}

if (textarea.attachEvent) {
  textarea.attachEvent('oninput', autoResize); // Для устаревших версий браузеров
} else {
  textarea.addEventListener('input', autoResize);
}

// функция получение csrf токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('submitBtn');
    const loadingBar = document.getElementById('loadingBar');
    const progress = document.getElementById('progress');
    const resultText = document.getElementById('resultText');
    const loadingText = document.getElementById('loadingText');
    const textarea = document.getElementById('text-input')
    const resultLink = document.getElementById('resultLink')
    const messageText = document.getElementById('messageText')

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы

        submitBtn.style.display = 'none'; // Скрываем кнопку
        loadingBar.style.display = 'block'; // Показываем полосу загрузки

        let object = {};
        let formData = new FormData(document.forms.textform);
    
        formData.forEach(function(value, key){
            object[key] = value;
        });

        let data = JSON.stringify(object);

        let progressValue = 0;
        const interval = setInterval(function() {
            if (progressValue < 90) {
                progressValue += 5;
                progress.style.width = progressValue + '%';
            } else {
                clearInterval(interval);
            }
        }, 100); // Имитация загрузки

        // Отправка данных формы на сервер
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: data
        })
        .then(response => response.json())
        .then(data => {
            clearInterval(interval);
                  
            progress.style.width = 100+'%';
            
            let timeoutId
            timeoutId = setTimeout(() => {
                resultText.textContent = 'Ссылка готова: '; 
                resultLink.textContent = data.link;
                messageText.textContent = 'Ссылка готова:\n' + data.link;
                datePicker.value = default_date.toISOString().split('T')[0];
                textarea.value = '';
                resultText.style.display = 'block';
                loadingText.style.display = 'none';
            }, 200)
            
        })
        .catch(error => {
            loadingText.textContent = 'Ошибка загрузки, попробуйте ещё раз.';
            loadingBar.style.display = 'none';
            resultText.style.display = 'block';
            resultText.textContent = 'Ошибка загрузки, попробуйте ещё раз.';
            console.error('Ошибка:', error);
        });
    });
});


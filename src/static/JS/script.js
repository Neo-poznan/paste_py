// переменные для поля ввода даты
const datePicker = document.getElementById('datePicker');
const today = new Date();
const tomorrow = new Date(today);
const default_date = new Date();
const maxDate = new Date(tomorrow);

tomorrow.setDate(tomorrow.getDate() + 1); // Завтрашний день
maxDate.setDate(maxDate.getDate() + 60); // 14 дней после завтрашнего дня
default_date.setDate(default_date.getDate() + 30)

// установим минимум и максимум для поля ввода даты
datePicker.min = tomorrow.toISOString().split('T')[0];
datePicker.max = maxDate.toISOString().split('T')[0];
datePicker.value = default_date.toISOString().split('T')[0];

// закрытие сообщения
function closeMessageBox() {
    var messageBox = document.getElementById('messageBox');
    messageBox.style.display = 'none';
}

// автоматическое изменение размера поля
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

// отправка формы и имитация загрузки
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('submitBtn');
    const loadingBar = document.getElementById('loadingBar');
    const loadingContainer = loadingBar.parentElement;
    const progress = document.getElementById('progress');
    const resultText = document.getElementById('resultText');
    const loadingText = document.getElementById('loadingText');
    const textarea = document.getElementById('text-input')
    const resultLink = document.getElementById('resultLink')
    const messageText = document.getElementById('messageText')

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы

        submitBtn.style.display = 'none'; // Скрываем кнопку
        resultText.textContent = ''; 
        resultText.style.display = 'none'; // Скрываем текст результата
        loadingContainer.style.display = 'block'; // Показываем контейнер загрузки
        loadingBar.style.display = 'block'; // Показываем полосу загрузки

        let object = {};
        let formData = new FormData(document.forms.textform);
    
        formData.forEach(function(value, key){
            object[key] = value;
        });

        let data = JSON.stringify(object);
        let progressValue = 0;
        // Имитация загрузки
        const interval = setInterval(function() {
            if (progressValue < 90) {
                progressValue += 5;
                progress.style.width = progressValue + '%';
            } else {
                clearInterval(interval);
            }
        }, 100); 

        // Отправка данных формы на сервер
        fetch('', {
            method: 'POST',
            headers: {
            'X-CSRFToken': csrfCookie // Установка CSRF-токена в заголовок
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
                resultLink.href = data.link;
                messageText.textContent = 'Ссылка готова:\n' + data.link;
                datePicker.value = default_date.toISOString().split('T')[0];
                textarea.value = '';
                resultText.style.display = 'block';
                loadingText.style.display = 'none';
            }, 200)
            
        })
        .catch(error => {
            setTimeout(() => {
                loadingContainer.style.display = 'block';
                loadingBar.style.display = 'none';
                resultText.style.display = 'block';
                resultText.textContent = 'Ошибка загрузки, попробуйте ещё раз.';
                console.error('Ошибка:', error);
                submitBtn.style.display = 'block';
            }, 500);
        });
    });
});


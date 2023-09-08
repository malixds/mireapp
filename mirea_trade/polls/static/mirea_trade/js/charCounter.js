document.addEventListener("DOMContentLoaded", function() {
    const inputElement = document.getElementById("MyTextArea");
    const charCountElement = document.getElementById("charCount");
    const maxCharCount = 100; // Максимальное количество символов
  
    // Функция для обновления счетчика символов
    function updateCharCount() {
        const textLength = inputElement.value.length;
        charCountElement.firstElementChild.innerText = textLength;
    }
  
    // Обработка события ввода текста
    inputElement.addEventListener("input", updateCharCount);
  
    // Вызываем функцию при загрузке страницы, чтобы отобразить начальное значение счетчика
    updateCharCount();
});


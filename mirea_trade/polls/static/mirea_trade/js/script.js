$(function () {
  $('.js-example-basic-multiple').select2();
});

// console.log('JavaScript код загружен');
function showModal() {
  $('#success-modal').show();
}

function closeModal() {
  $('#success-modal').hide();
}


const stars = document.querySelectorAll('.star');
const selectedRating = document.getElementById('selected-rating');

stars.forEach((star) => {
  star.addEventListener('click', () => {
    const rating = parseInt(star.getAttribute('data-rating'));
    selectedRating.innerText = rating;

    // Здесь можно отправить оценку на сервер
    // Например, с использованием AJAX-запроса

    // Также, можно добавить логику для предотвращения повторной оценки
    // например, скрывать звезды после выбора оценки
    stars.forEach((s) => {
      s.classList.remove('active');
    });

    star.classList.add('active');
  });
});
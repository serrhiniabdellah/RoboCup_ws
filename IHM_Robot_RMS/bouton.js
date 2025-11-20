document.addEventListener('DOMContentLoaded', function() {
  const button = document.getElementById('toggleButton');
  button.addEventListener('click', function() {
    button.classList.toggle('active');
  });
});

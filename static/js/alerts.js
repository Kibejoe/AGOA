document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById('message');
  
    if (message) {
      message.style.transition = 'opacity 1s ease';
  
      setTimeout(function () {
        message.style.opacity = '0';
  
        message.addEventListener('transitionend', () => {
          message.remove();
        });
      }, 5000);
    }
  });
 
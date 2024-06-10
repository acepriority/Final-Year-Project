document.addEventListener('DOMContentLoaded', function() {
    const rejectButton = document.getElementById('reject-btn');
    const reasonGroup = document.querySelector('.reason-group');
    const reasonTextarea = reasonGroup.querySelector('textarea');
    let timer;

    rejectButton.addEventListener('click', function() {
        if (reasonGroup.style.display === 'none' || reasonGroup.style.display === '') {
            reasonGroup.style.display = 'flex';
            startTimer();
        } else {
            reasonGroup.style.display = 'none';
            clearTimer();
        }
    });

    reasonTextarea.addEventListener('input', function() {
        clearTimer();
    });

    function startTimer() {
        timer = setTimeout(function() {
            if (!reasonTextarea.value.trim()) {
                reasonGroup.style.display = 'none';
            }
        }, 20000); 
    }

    function clearTimer() {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
    }
});

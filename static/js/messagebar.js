document.addEventListener('DOMContentLoaded', () => {
    var notification = document.getElementById('notification');
        if (notification) {
            setTimeout(function() {
                notification.style.opacity = '0';
                setTimeout(function() {
                    notification.style.display = 'none';
                }, 500); // Delay to match the fade-out duration
            }, 3000); // Display time in milliseconds
        }
});
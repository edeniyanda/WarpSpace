document.addEventListener('DOMContentLoaded', () => {
    // Handle like button clicks
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.dataset.id;
            fetch(`/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`like-count-${postId}`).textContent = data.likes;
            });
        });
    });

    // Handle repost button clicks
    document.querySelectorAll('.repost-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.dataset.id;
            fetch(`/repost/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`repost-count-${postId}`).textContent = data.reposts;
            });
        });
    });
    // Like button functionality
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.dataset.id;
            fetch(`/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(response => response.json())
            .then(data => {
                const likeCountElement = document.getElementById(`like-count-${postId}`);
                likeCountElement.textContent = data.likes;

                // Toggle the liked class
                this.classList.toggle('liked');
            });
        });
    });

    // Repost button functionality
    document.querySelectorAll('.repost-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.dataset.id;
            fetch(`/repost/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(response => response.json())
            .then(data => {
                const repostCountElement = document.getElementById(`repost-count-${postId}`);
                repostCountElement.textContent = data.reposts;

                // Toggle the reposted class
                this.classList.toggle('reposted');
            });
        });
    });
    
});
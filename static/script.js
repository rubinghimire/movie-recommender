// Function to make an AJAX request to the backend and display recommendations
function getRecommendations() {
    const movieInput = document.getElementById('movieInput');
    const recommendationsDiv = document.getElementById('recommendations');

    // Get the user input (movie title)
    const movieTitle = movieInput.value.trim();

    // Check if the input is empty
    if (!movieTitle) {
        alert('Please enter a movie title.');
        return;
    }

    // Make an AJAX request to the backend (replace 'backend_url' with your actual backend URL)
    fetch('backend_url/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ movie_title: movieTitle })
    })
    .then(response => response.json())
    .then(data => {
        // Display recommendations in the recommendationsDiv
        recommendationsDiv.innerHTML = '';
        data.recommendations.forEach((recommendation, index) => {
            const recommendationDiv = document.createElement('div');
            recommendationDiv.innerText = `${index + 1}. ${recommendation}`;
            recommendationsDiv.appendChild(recommendationDiv);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
// Function to make an AJAX request to the backend and display recommendations
function getRecommendations() {
    console.log('Function called');
    const movieInput = document.getElementById('movieInput');
    const searchBox = document.querySelector('.search-box');
    const recommendationsDiv = document.getElementById('recommendations');
    const button = document.querySelector('.search-box button');

    // Get the user input (movie title)
    const movieTitle = movieInput.value.trim();

    // Create and append a loading message element
    const loadingMessage = document.createElement('h4');
    loadingMessage.innerText = 'Please wait for the server\'s response.';
    searchBox.appendChild(loadingMessage);

    // Check if the input is empty
    if (!movieTitle) {
        alert('Please enter a movie title.');
        loadingMessage.remove(); // Remove the loading message
        return;
    }

    // Make an AJAX request to the backend (replace URL with your actual backend URL)
    fetch(`https://movie-recommender-z51m.onrender.com/recommend/${movieTitle}`)
        .then(response => response.json())
        .then(data => {
            // Remove the loading message
            loadingMessage.remove();

            // Display recommendations in the recommendationsDiv
            recommendationsDiv.innerHTML = '';
            data.recommendations.forEach((recommendation, index) => {
                const recommendationDiv = document.createElement('div');
                recommendationDiv.innerText = `${index + 1}. ${recommendation}`;
                recommendationsDiv.appendChild(recommendationDiv);
            });
        })
        .catch(error => {
            // Update the loading message with the error
            loadingMessage.innerText = 'Error: ' + error;
        });
}

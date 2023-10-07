// Function to make an AJAX request to the backend and display recommendations
function getRecommendations() {
    console.log('Function called');
    const movieInput = document.getElementById('movieInput');
    const message = document.querySelector('.message');
    const recommendationsDiv = document.getElementById('recommendations');

    // Get the user input (movie title)
    const movieTitle = movieInput.value.trim();
    // Ask user to wait
    message.innerText = 'Please wait for the server\'s response.';

    // Check if the input is empty
    if (!movieTitle) {
        alert('Please enter a movie title.');
        message.innerText = ""; // Remove the message
        return;
    }

    // Make an AJAX request to the backend (replace URL with your actual backend URL)
    fetch(`https://movie-recommender-z51m.onrender.com/recommend/${movieTitle}`)
        .then(response => response.json())
        .then(data => {
            // Erase the message
            message.innerText = "";

            // Display recommendations in the recommendationsDiv
            recommendationsDiv.innerHTML = '';
            data.recommendations.forEach((recommendation, index) => {
                const recommendationDiv = document.createElement('div');
                recommendationDiv.innerText = `${index + 1}. ${recommendation}`;
                recommendationsDiv.appendChild(recommendationDiv);
            });
        })
        .catch(error => {
            // Update the message with the error
            message.innerText = 'Error: ' + error;
        });
}

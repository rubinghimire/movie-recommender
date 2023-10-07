// Function to make an AJAX request to the backend and display recommendations
function getRecommendations() {
    console.log('Function called');
    const movieInput = document.getElementById('movieInput');
    const button = document.getElementsByTagName('button')[0];
    const recommendationsDiv = document.getElementById('recommendations');

    // Get the user input (movie title)
    const movieTitle = movieInput.value.trim();

    // Append message for user
    const element = "<h4>Please wait for the server's response.</h4>";
    button.insertAdjacentHTML("afterend", element);

    // Check if the input is empty
    if (!movieTitle) {
        alert('Please enter a movie title.');
        return;
    }

    // Make an AJAX request to the backend (replace URL with your actual backend URL)
    fetch(`https://movie-recommender-z51m.onrender.com/recommend/${movieTitle}`)
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
        element.remove();
}
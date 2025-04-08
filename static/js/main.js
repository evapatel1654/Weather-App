document.addEventListener('DOMContentLoaded', function() {
    const weatherForm = document.getElementById('weather-form');
    const weatherResults = document.getElementById('weather-results');
    const errorMessage = document.getElementById('error-message');
    const infoButton = document.getElementById('info-button');

    // Get current location on page load
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const coords = `${position.coords.latitude},${position.coords.longitude}`;
            document.getElementById('location').value = coords;
            fetchWeather(coords);
        });
    }

    weatherForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const location = document.getElementById('location').value;
        fetchWeather(location);
    });

    async function fetchWeather(location) {
        try {
            showLoading();
            const response = await fetch('/weather', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `location=${encodeURIComponent(location)}`
            });

            if (!response.ok) {
                throw new Error('Weather data not available');
            }

            const data = await response.json();
            displayWeather(data);
            hideError();
        } catch (error) {
            showError(error.message);
        } finally {
            hideLoading();
        }
    }

    function displayWeather(data) {
        const weatherInfo = document.querySelector('.weather-info');
        const forecastInfo = document.querySelector('.forecast-info');

        // Display current weather
        weatherInfo.innerHTML = `
            <div class="weather-card p-4">
                <div class="d-flex align-items-center">
                    <img src="http://openweathermap.org/img/w/${data.icon}.png" 
                         alt="Weather icon" 
                         class="weather-icon">
                    <div class="ms-3">
                        <div class="temperature">${Math.round(data.temperature)}°C</div>
                        <div class="conditions">${data.description}</div>
                        <div class="details mt-2">
                            <div>Feels like: ${Math.round(data.feels_like)}°C</div>
                            <div>Humidity: ${data.humidity}%</div>
                            <div>Wind: ${data.wind_speed} m/s</div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Display forecast
        if (data.forecast) {
            forecastInfo.innerHTML = data.forecast.map(day => `
                <div class="forecast-day">
                    <div class="date">${day.date}</div>
                    <img src="http://openweathermap.org/img/w/${day.icon}.png" 
                         alt="Weather icon" 
                         class="weather-icon">
                    <div class="temp">${Math.round(day.temperature)}°C</div>
                    <div class="desc">${day.description}</div>
                </div>
            `).join('');
        }

        weatherResults.classList.remove('d-none');
    }

    function showLoading() {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `;
        weatherForm.appendChild(spinner);
    }

    function hideLoading() {
        const spinner = document.querySelector('.loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('d-none');
    }

    function hideError() {
        errorMessage.classList.add('d-none');
    }

    // Info button modal
    infoButton.addEventListener('click', function() {
        const modal = new bootstrap.Modal(document.createElement('div'));
        modal.element.innerHTML = `
            <div class="modal-dialog info-modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">About PM Accelerator</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>This weather app is part of the PM Accelerator program.</p>
                        <p>Visit our <a href="https://www.linkedin.com/company/pm-accelerator" 
                                      target="_blank">LinkedIn</a> for more information.</p>
                    </div>
                </div>
            </div>
        `;
        modal.show();
    });
});

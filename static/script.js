// Function to display job listings
function displayJobListings(jobListings) {
    const jobList = document.getElementById('job-list');
    jobList.innerHTML = ''; // Clear previous listings
    jobListings.forEach(job => {
        const jobItem = document.createElement('div');
        jobItem.classList.add('job-item');
        jobItem.innerHTML = `<h3>${job.title}</h3><p>${job.company} - ${job.location}</p>`;
        jobList.appendChild(jobItem);
    });
}

// Function to display messages
function displayMessages(messages) {
    const messageList = document.getElementById('message-list');
    messageList.innerHTML = ''; // Clear previous messages
    messages.forEach(message => {
        const messageItem = document.createElement('div');
        messageItem.classList.add('message-item');
        messageItem.innerHTML = `<strong>${message.from}:</strong> ${message.content}`;
        messageList.appendChild(messageItem);
    });
}

// Fetch job listings from the Flask API
fetch('/api/jobs')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => displayJobListings(data))
    .catch(error => console.error('Error fetching job listings:', error));

// Fetch messages from the Flask API
fetch('/api/messages')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => displayMessages(data))
    .catch(error => console.error('Error fetching messages:', error));
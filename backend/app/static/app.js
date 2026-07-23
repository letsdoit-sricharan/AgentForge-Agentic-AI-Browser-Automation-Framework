document.getElementById('booking-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submit-btn');
    const badge = document.getElementById('status-badge');
    const requestIdSpan = document.getElementById('request-id');
    const logsPre = document.getElementById('execution-logs');
    const resultContainer = document.getElementById('result-container');
    const resultData = document.getElementById('result-data');

    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    data.ticket_count = parseInt(data.ticket_count, 10);

    try {
        const response = await fetch('/api/bookings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        const requestId = result.request_id;
        
        requestIdSpan.textContent = requestId;
        badge.className = 'badge queued';
        badge.textContent = 'QUEUED';
        logsPre.textContent = 'Request submitted. Waiting for execution to start...\n';
        resultContainer.classList.add('hidden');

        // Start polling
        pollStatus(requestId);
    } catch (error) {
        console.error('Error submitting booking:', error);
        badge.className = 'badge failed';
        badge.textContent = 'ERROR';
        logsPre.textContent = `Submission Error: ${error.message}`;
        submitBtn.disabled = false;
        submitBtn.textContent = 'Run Workflow';
    }
});

async function pollStatus(requestId) {
    const badge = document.getElementById('status-badge');
    const logsPre = document.getElementById('execution-logs');
    const submitBtn = document.getElementById('submit-btn');
    const resultContainer = document.getElementById('result-container');
    const resultData = document.getElementById('result-data');

    let isPolling = true;

    while (isPolling) {
        try {
            const response = await fetch(`/api/bookings/${requestId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const status = data.status;

            badge.textContent = status;
            badge.className = `badge ${status.toLowerCase()}`;

            if (status === 'RUNNING') {
                // In a real app with WebSockets we'd stream logs. 
                // For polling, we just append a heartbeat.
                logsPre.textContent += '.';
            }

            if (status === 'COMPLETED' || status === 'FAILED') {
                isPolling = false;
                submitBtn.disabled = false;
                submitBtn.textContent = 'Run Workflow';
                
                logsPre.textContent += `\nExecution finished with status: ${status}`;
                
                resultContainer.classList.remove('hidden');
                
                if (status === 'COMPLETED') {
                    resultData.textContent = JSON.stringify(data.result, null, 2);
                } else {
                    resultData.textContent = JSON.stringify(data.errors, null, 2);
                    resultData.style.color = 'var(--error)';
                }
            }
        } catch (error) {
            console.error('Polling error:', error);
            isPolling = false;
            submitBtn.disabled = false;
            submitBtn.textContent = 'Run Workflow';
            logsPre.textContent += `\nPolling Error: ${error.message}`;
        }

        if (isPolling) {
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }
}

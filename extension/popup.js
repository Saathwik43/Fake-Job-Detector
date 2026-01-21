const analyzeTextBtn = document.getElementById('analyzeTextBtn');
const analyzePageBtn = document.getElementById('analyzePageBtn');
const jobInput = document.getElementById('jobDescriptionInput');
const resultDiv = document.getElementById('result');
const loadingDiv = document.getElementById('loading');

const analyzeJob = async (text) => {
  if (!text || text.trim().length === 0) {
    alert('Please enter some text to analyze.');
    return;
  }

  // Reset UI
  resultDiv.style.display = 'none';
  loadingDiv.style.display = 'flex';
  analyzeTextBtn.disabled = true;
  analyzePageBtn.disabled = true;

  try {
    // Call API
    // Ensure the backend is running on localhost:5000
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: text })
    });

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    loadingDiv.style.display = 'none';
    resultDiv.style.display = 'block';

    if (data.is_fraud) {
      resultDiv.className = 'fraud';
      resultDiv.innerHTML = `
        <div class="score-label">Trust Score</div>
        <div class="score-value">${data.trust_score}%</div>
        <div class="verdict">⚠️ Potential Risks Detected</div>
      `;
    } else {
      resultDiv.className = 'safe';
      resultDiv.innerHTML = `
        <div class="score-label">Trust Score</div>
        <div class="score-value">${data.trust_score}%</div>
        <div class="verdict">✅ Likely Legitimate</div>
      `;
    }

  } catch (error) {
    loadingDiv.style.display = 'none';
    resultDiv.style.display = 'block';
    resultDiv.className = '';
    resultDiv.style.backgroundColor = '#fae3a5'; // Warning yellow
    resultDiv.style.color = '#856404';
    resultDiv.innerHTML = `Error: ${error.message}`;
  } finally {
    analyzeTextBtn.disabled = false;
    analyzePageBtn.disabled = false;
  }
};

analyzeTextBtn.addEventListener('click', () => {
  const text = jobInput.value;
  analyzeJob(text);
});

analyzePageBtn.addEventListener('click', async () => {
  loadingDiv.style.display = 'flex'; // Show loading while extracting
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    const extractionResult = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: () => {
        // Simple extraction logic - gets all visible text
        // In a real scenario, this could be improved to target specific job description containers
        return document.body.innerText;
      }
    });

    const text = extractionResult[0].result;
    
    if (text) {
      jobInput.value = text; // Populate the textarea
      analyzeJob(text);
    } else {
      loadingDiv.style.display = 'none';
      alert('Could not extract text from this page.');
    }
  } catch (err) {
    loadingDiv.style.display = 'none';
    console.error(err);
    alert('Failed to extract text from page: ' + err.message);
  }
});

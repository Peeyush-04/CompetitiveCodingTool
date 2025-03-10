document.addEventListener('DOMContentLoaded', () => {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    // Check if the current page is a Codeforces problem page
    if (tabs[0].url.includes("codeforces.com")) {
      chrome.scripting.executeScript({
        target: {tabId: tabs[0].id},
        function: analyzeProblems
      }, (results) => {
        if (chrome.runtime.lastError || !results || !results[0]) {
          console.error('Error: Could not analyze problems.', chrome.runtime.lastError);
          return;
        }
        const problems = results[0].result;
        fetch('http://localhost:5000/receive_problems', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(problems)
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          console.log(data.message);
        })
        .catch(error => {
          console.error('Error: Failed to fetch -', error.message);
        });
      });
    }
  });
});

function analyzeProblems() {
  const problems = [];
  const problemDivs = document.querySelectorAll('div.problem-statement');
  
  problemDivs.forEach(div => {
    const titleElement = div.querySelector('div.title');
    if (!titleElement) return;
    const title = titleElement.textContent.trim();
    const letter = title.split('.')[0]; // e.g., "A" from "A. Problem Name"

    const samples = [];
    const inputs = div.querySelectorAll('div.input pre');
    const outputs = div.querySelectorAll('div.output pre');
    
    inputs.forEach((input, index) => {
      const sampleIn = Array.from(input.childNodes)
        .map(node => node.textContent.trim())
        .filter(text => text.length > 0)
        .join('\n');
      const sampleOut = outputs[index]
        ? Array.from(outputs[index].childNodes)
            .map(node => node.textContent.trim())
            .filter(text => text.length > 0)
            .join('\n')
        : '';
      samples.push([sampleIn, sampleOut]);
    });

    problems.push({ letter, samples });
  });

  return problems;
}
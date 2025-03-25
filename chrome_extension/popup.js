document.addEventListener('DOMContentLoaded', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    let url = tabs[0].url;
    console.log("Active URL:", url);
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: analyzePageFull,
      args: [url]
    }, (results) => {
      if (chrome.runtime.lastError) {
        console.error("Scripting error:", chrome.runtime.lastError.message);
        return;
      }
      if (!results || results.length === 0) {
        console.error("No results from content script");
        return;
      }
      const problemsData = results[0].result;
      console.log("Extracted problems data:", problemsData);
      fetch('http://localhost:5000/receive_problems', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(problemsData)
      })
      .then(response => {
        if (!response.ok) { throw new Error('Network response was not ok'); }
        return response.json();
      })
      .then(data => {
        console.log(data.message);
      })
      .catch(error => {
        console.error('Error: Failed to fetch -', error.message);
      });
    });
  });
});

// Self-contained extraction function that runs in the context of the active tab
function analyzePageFull(url) {
  // Helper functions defined inside so they are available in the page context
  function extractContestId(url) {
    let m = url.match(/contest\/(\d+)/);
    return m ? m[1] : "Unknown";
  }
  function extractContestIdAtcoder(url) {
    let m = url.match(/contests\/([^\/]+)/);
    return m ? m[1] : "Unknown";
  }
  function analyzeCodeforcesProblems() {
    const problems = [];
    let problemDivs = document.querySelectorAll('div.problem-statement');
    if (!problemDivs || problemDivs.length === 0) {
      problemDivs = document.querySelectorAll('div.problemindexholder');
    }
    if (problemDivs && problemDivs.length > 0) {
      problemDivs.forEach(div => {
        const titleElement = div.querySelector('.title');
        if (!titleElement) return;
        let title = titleElement.textContent.trim();
        let letter = title.split('.')[0].trim();
        if (!letter) letter = "A";
        const samples = [];
        let inputElements = div.querySelectorAll('.input pre');
        let outputElements = div.querySelectorAll('.output pre');
        if (inputElements.length === 0) {
          const sampleTest = div.querySelector('.sample-test');
          if (sampleTest) {
            inputElements = sampleTest.querySelectorAll('.input pre');
            outputElements = sampleTest.querySelectorAll('.output pre');
          }
        }
        inputElements.forEach((input, index) => {
          const sampleIn = Array.from(input.childNodes)
            .map(node => node.textContent.trim())
            .filter(text => text.length > 0)
            .join('\n');
          const sampleOut = outputElements[index]
            ? Array.from(outputElements[index].childNodes)
                .map(node => node.textContent.trim())
                .filter(text => text.length > 0)
                .join('\n')
            : '';
          samples.push([sampleIn, sampleOut]);
        });
        if (samples.length > 0) {
          problems.push({ letter, samples });
        }
      });
    }
    return problems;
  }
  function analyzeCodeforcesOverview() {
    const problems = [];
    let table = document.querySelector("table.problems") || document.getElementsByClassName("problems")[0];
    if (!table) {
      console.warn("No problems table found on Codeforces overview page.");
      return problems;
    }
    const rows = table.querySelectorAll("tr");
    if (rows.length <= 1) {
      console.warn("No problem rows found in the problems table.");
      return problems;
    }
    for (let i = 1; i < rows.length; i++) {
      const cells = rows[i].querySelectorAll("td");
      if (cells.length < 2) continue;
      const letter = cells[0].innerText.trim();
      problems.push({ letter, samples: [] });
    }
    return problems;
  }
  function analyzeAtcoderProblems() {
    const problems = [];
    let taskSections = document.querySelectorAll('section.task');
    if (taskSections && taskSections.length > 0) {
      taskSections.forEach(task => {
        let idAttr = task.getAttribute('id');
        let letter = "A";
        if (idAttr) {
          let m = idAttr.match(/_(.+)/);
          if (m) {
            letter = m[1].toUpperCase();
          }
        }
        const samples = [];
        const sampleTestDiv = task.querySelector("div.sample-test");
        if (sampleTestDiv) {
          const inputs = sampleTestDiv.querySelectorAll("div.input pre");
          const outputs = sampleTestDiv.querySelectorAll("div.output pre");
          inputs.forEach((input, index) => {
            const sampleIn = input.innerText.trim();
            const sampleOut = outputs[index] ? outputs[index].innerText.trim() : "";
            samples.push([sampleIn, sampleOut]);
          });
        }
        problems.push({ letter, samples });
      });
    } else {
      const letter = "A";
      const samples = [];
      const sampleTestDiv = document.querySelector("div.sample-test");
      if (sampleTestDiv) {
        const inputs = sampleTestDiv.querySelectorAll("div.input pre");
        const outputs = sampleTestDiv.querySelectorAll("div.output pre");
        inputs.forEach((input, index) => {
          const sampleIn = input.innerText.trim();
          const sampleOut = outputs[index] ? outputs[index].innerText.trim() : "";
          samples.push([sampleIn, sampleOut]);
        });
      } else {
        console.warn("AtCoder: No sample-test container found.");
      }
      problems.push({ letter, samples });
    }
    return problems;
  }
  
  // Build the problems data object
  const problemsData = {};
  if (url.includes("codeforces.com")) {
    problemsData.platform = "Codeforces";
    problemsData.contestId = extractContestId(url);
    let problems = analyzeCodeforcesProblems();
    if (problems.length === 0 && url.includes("/problems")) {
      console.log("Using overview extraction for Codeforces.");
      problems = analyzeCodeforcesOverview();
    }
    problemsData.problems = problems;
  } else if (url.includes("atcoder.jp")) {
    problemsData.platform = "AtCoder";
    problemsData.contestId = extractContestIdAtcoder(url);
    problemsData.problems = analyzeAtcoderProblems();
  } else {
    console.error("Unsupported platform");
    return {};
  }
  return problemsData;
}

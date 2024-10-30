const flagMap = {
    'English': 'https://flagcdn.com/us.svg',
    'Malayalam': 'https://flagcdn.com/in.svg',
    'Hindi': 'https://flagcdn.com/in.svg',
    'Tamil': 'https://flagcdn.com/in.svg',
    'Kannada': 'https://flagcdn.com/in.svg', 
    'French': 'https://flagcdn.com/fr.svg',
    'Spanish': 'https://flagcdn.com/es.svg',
    'Portuguese': 'https://flagcdn.com/pt.svg',
    'Italian': 'https://flagcdn.com/it.svg',
    'Russian': 'https://flagcdn.com/ru.svg',
    'Swedish': 'https://flagcdn.com/se.svg',
    'Dutch': 'https://flagcdn.com/nl.svg',
    'Arabic': 'https://flagcdn.com/sa.svg',
    'Turkish': 'https://flagcdn.com/tr.svg',
    'German': 'https://flagcdn.com/de.svg',
    'Danish': 'https://flagcdn.com/dk.svg',
    'Greek': 'https://flagcdn.com/gr.svg',
};

async function detectLanguage() {
    const text = document.getElementById("textInput").value;
    const resultDiv = document.getElementById("result");
    
    resultDiv.innerHTML = '';

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        if (data.language) {
            const flagUrl = flagMap[data.language];
            resultDiv.innerHTML = `<strong>Predicted Language:</strong> ${data.language}`;
            if (flagUrl) {
                resultDiv.innerHTML += `<img id="flag" src="${flagUrl}" alt="${data.language} flag">`;
            }
        } else {
            resultDiv.innerHTML = `<div id="error"><strong>Error:</strong> ${data.error}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div id="error"><strong>Error:</strong> ${error.message}</div>`;
    }
}
document.addEventListener("DOMContentLoaded", () => {
    const fetchTextBtn = document.getElementById("fetch-text-btn");
    const generateContentBtn = document.getElementById("generate-content-btn");

    fetchTextBtn.addEventListener("click", async () => {
        const textRef = document.getElementById("text-ref").value;
        const textOutput = document.getElementById("text-output");

        if (!textRef) {
            textOutput.innerHTML = "<p>Please enter a Sefaria reference.</p>";
            return;
        }

        try {
            const response = await fetch(`/api/text?ref=${textRef}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            textOutput.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        } catch (error) {
            textOutput.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    });

    generateContentBtn.addEventListener("click", async () => {
        const contentType = document.getElementById("content-type").value;
        const generationRef = document.getElementById("generation-ref").value;
        const generatedContentOutput = document.getElementById("generated-content-output");

        if (!generationRef) {
            generatedContentOutput.innerHTML = "<p>Please enter a reference or theme.</p>";
            return;
        }

        try {
            const response = await fetch(`/api/generate?type=${contentType}&ref=${generationRef}`);
            const data = await response.json();
            generatedContentOutput.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        } catch (error) {
            generatedContentOutput.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    });
});


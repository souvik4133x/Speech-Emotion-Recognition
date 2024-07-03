document.getElementById('uploadButton').addEventListener('click', () => {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://127.0.0.1:5000/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('result').innerText = `Prediction: ${data}`;
        })
        .catch(error => {
            document.getElementById('result').innerText = 'Error uploading file';
        });
    } else {
        document.getElementById('result').innerText = 'Please select a file first';
    }
});

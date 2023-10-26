document.getElementById('imageInput').addEventListener('change', function (e) {
    const imagePreview = document.getElementById('imagePreview');
    imagePreview.style.display = 'block';
    const progress = document.getElementById('progress');
    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = '0%';

    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        imagePreview.src = e.target.result;
        // Enable the "Detect Weeds" button
        document.getElementById('detectButton').disabled = false;
    };

    reader.onprogress = function (e) {
        if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            progressBar.style.width = percentComplete + '%';
        }
    };

    reader.readAsDataURL(file);
});

function detectWeeds() {
    const imagePreview = document.getElementById('imagePreview');
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    canvas.width = imagePreview.width;
    canvas.height = imagePreview.height;
    context.drawImage(imagePreview, 0, 0, canvas.width, canvas.height);

    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    let weedCount = 0;

    // Simple brightness threshold for weed detection
    for (let i = 0; i < data.length; i += 4) {
        const brightness = (data[i] + data[i + 1] + data[i + 2]) / 3;

        if (brightness < 100) {
            // Assuming low brightness represents weeds
            weedCount++;
        }
    }

    const result = document.getElementById('result');
    result.textContent = `Weed Count: ${weedCount}`;
}

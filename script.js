const musicUpload = document.getElementById('musicUpload');
const songList = document.getElementById('songList');
const audioPlayer = document.getElementById('audioPlayer');
const uploadButton = document.getElementById('uploadButton');

// Fetch and display the list of songs on page load
fetch('/songs')
    .then(response => response.json())
    .then(songs => {
        songs.forEach(song => {
            addSongToList(song);
        });
    });

uploadButton.addEventListener('click', () => {
    const files = musicUpload.files;

    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.filename) {
                    addSongToList({ name: data.filename.split('.')[0], filename: data.filename });
                }
            })
            .catch(error => console.error('Error:', error));
    }
});
function addSongToList(song) {
    const listItem = document.createElement('li');
    listItem.textContent = song.name;
    listItem.addEventListener('click', () => playSong(song.filename));
    songList.appendChild(listItem);
}

function playSong(filename) {
    audioPlayer.src = `/uploads/${filename}`;
    audioPlayer.play();
}
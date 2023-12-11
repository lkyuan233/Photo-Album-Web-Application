function addphoto() {
    var files = document.getElementById("photoupload").files;
    if (!files.length) {
        return alert("Please choose a file to upload first.");
    }
    var file = files[0];
    console.log(file)
    const requestOptions = {
    method: 'PUT',
    headers: { 'Content-Type': file.type },
    body: file
    };
    fetch(`https://j7mqjuuhnd.execute-api.us-east-1.amazonaws.com/beta/photos/${file.name}`,
        requestOptions
    ).then((response) => {
            console.log(response)
        }
    )
}

function searchphoto() {
    var input = document.getElementById("photosearch").value
    if (!input || input.size == 0) {
        return alert("Presponse.data.body.substr(1, response.data.body.length - 2)lease input search condition.");
    }
    document.getElementById('photos').removeChild(document.getElementById('photos').firstChild);
    sdk.searchGet({'q':input}, {} ,{}).then(
        (response) => {
            let img = new Image();
            img.src = response.data.body.substr(1, response.data.body.length - 2)
            document.getElementById('photos').appendChild(img);
            console.log(response)
        }
    )
}
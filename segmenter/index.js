
var images = [];


const file_input = document.getElementById("file_input");
file_input.addEventListener("change", () => {
	images = file_input.files;
}, false);
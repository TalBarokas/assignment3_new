function getUser() {
  var id = document.getElementById("frontend_id").value;
  fetch('https://reqres.in/api/users/' + id.toString())
    .then(result => result.json())
    .then((output) => {
      const myJSON = JSON.stringify(output);
      document.getElementById("userdata").innerHTML = myJSON;
    }).catch(err => console.error(err));
  document.getElementById("userdata").innerHTML = "Cant Find User";
}
const isUserLoggedIn = localStorage.getItem("isLoggedIn");
if (!isUserLoggedIn) {
  window.location.href = "/admin/login.html";
}

const form = document.getElementById("user-update");
const username = document.getElementById("username");
const profession = document.getElementById("profession");
const facebook = document.getElementById("facebook");
const twitter = document.getElementById("twitter");
const instagram = document.getElementById("instagram");
const linkedin = document.getElementById("linkedin");
const github = document.getElementById("github");
const cv = document.getElementById("cv");
const profilePic = document.getElementById("profile-pic"); // Corrected variable name
const shortDescription = document.getElementById("short-description");
const detailedDescription = document.getElementById(
  "detailed_description"
);

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const formData = new FormData();

  // Append non-empty fields to the FormData object
  if (username.value.trim() !== "")
    formData.append("name", username.value);
  if (profession.value.trim() !== "")
    formData.append("profession", profession.value);
  if (facebook.value.trim() !== "")
    formData.append("facebook", facebook.value);
  if (twitter.value.trim() !== "")
    formData.append("twitter", twitter.value);
  if (instagram.value.trim() !== "")
    formData.append("instagram", instagram.value);
  if (linkedin.value.trim() !== "")
    formData.append("linkedin", linkedin.value);
  if (github.value.trim() !== "") formData.append("github", github.value);
  if (cv.files.length > 0) formData.append("cv", cv.files[0]);
  if (profilePic.files.length > 0)
    formData.append("profile", profilePic.files[0]);
  if (shortDescription.value.trim() !== "")
    formData.append("description", shortDescription.value);
  if (detailedDescription.value.trim() !== "")
    formData.append("detailed_description", detailedDescription.value);

  fetch("http://192.168.100.194:5000/user_details/11", {
    method: "PATCH",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error(error);
    });
});

const documentsForm = document.getElementById("documents");

documentsForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const formData = new FormData();
  if (cv.files.length > 0) formData.append("cv", cv.files[0]);
  if (profilePic.files.length > 0)
    formData.append("profile", profilePic.files[0]);

  fetch("http://192.168.100.194:5000/user_profile/11", {
    method: "PATCH",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error(error);
    });
});
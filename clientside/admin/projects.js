const isUserLoggedIn = localStorage.getItem("isLoggedIn");
if (!isUserLoggedIn) {
  window.location.href = "/clientside/admin/login.html";
}
document.addEventListener("DOMContentLoaded", function() {
    const baseUrl = 'http://127.0.0.1:5000';
    const projectList = document.getElementById('project-list');
    const projectModal = document.getElementById('projectModal');
    const closeProjectModal = document.querySelector('#projectModal .close');
    const addProjectButton = document.getElementById('addProjectButton');
    const modalTitle = document.getElementById('modalTitle');
    const projectForm = document.getElementById('projectForm');
    const submitButton = document.getElementById('submitButton');
    let currentProject = null; // To store the currently selected project

    // Function to fetch projects
    function fetchProjects() {
        fetch(`${baseUrl}/projects`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                projectList.innerHTML = ''; // Clear existing projects

                data.forEach(project => {
                    const projectBox = document.createElement('div');
                    projectBox.classList.add('portfolio-box');

                    const img = document.createElement('img');
                    img.src = `${baseUrl}/static/images/${project.images}`; // Assuming the image URL is stored in the 'images' property
                    img.alt = 'Project Image';
                    projectBox.appendChild(img);

                    const projectLayer = document.createElement('div');
                    projectLayer.classList.add('portfolio-layer');

                    const projectName = document.createElement('h4');
                    projectName.textContent = project.name; // Assuming the project name is stored in the 'name' property
                    projectLayer.appendChild(projectName);

                    const projectDescription = document.createElement('p');
                    projectDescription.textContent = project.short_description; // Assuming the project description is stored in the 'short_description' property
                    projectLayer.appendChild(projectDescription);

                    const link = document.createElement('a');
                    link.href = project.project_link; // Assuming the external link is stored in the 'project_link' property
                    link.innerHTML = '<i class="bx bx-link-external"></i>';
                    projectLayer.appendChild(link);

                    // Add update and delete buttons
                    const updateButton = document.createElement('button');
                    updateButton.textContent = 'Update';
                    updateButton.addEventListener('click', () => openProjectModal(project, 'Update'));
                    projectLayer.appendChild(updateButton);

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.addEventListener('click', () => deleteProject(project.id));
                    projectLayer.appendChild(deleteButton);

                    projectBox.appendChild(projectLayer);
                    projectList.appendChild(projectBox);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while fetching projects data.");
            });
    }

    // Function to open project modal for adding or updating project
    function openProjectModal(project, action) {
        currentProject = project; // Set the current project
        modalTitle.textContent = `${action} Project`;

        // Reset form fields
        projectForm.reset();

        // Set form fields if project is provided (for update)
        if (project) {
            document.getElementById('projectNameInput').value = project.name;
            document.getElementById('projectDescriptionInput').value = project.short_description;
            document.getElementById('projectLinkInput').value = project.project_link;
            // Set the image value here
        }

        // Show modal
        projectModal.style.display = 'block';

        // Change submit button text based on action
        submitButton.textContent = action;
    }

    // Close project modal when close button is clicked
    closeProjectModal.addEventListener('click', function() {
        projectModal.style.display = 'none';
    });

    // Close project modal when user clicks outside of it
    window.addEventListener('click', function(event) {
        if (event.target === projectModal) {
            projectModal.style.display = 'none';
        }
    });

    // Event listener for project form submission
    projectForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const projectName = document.getElementById('projectNameInput').value;
        const projectDescription = document.getElementById('projectDescriptionInput').value;
        const projectLink = document.getElementById('projectLinkInput').value;
        const projectImage = document.getElementById('projectImageInput').files[0]; // Get the file object

        const projectData = new FormData();
        projectData.append('name', projectName);
        projectData.append('short_description', projectDescription);
        projectData.append('project_link', projectLink);
        projectData.append('images', projectImage); // Append the image file to the FormData

        // Check if it's an update or add action
        if (currentProject) {
            // Update project
            const url = `${baseUrl}/projects/${currentProject.id}`;

            fetch(url, {
                method: 'PATCH',
                body: projectData, // Use FormData directly as the body
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                fetchProjects(); // Refresh projects after updating
                projectModal.style.display = 'none'; // Close modal
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while updating the project.");
            });
        } else {
            // Add new project
            const url = `${baseUrl}/project`;

            fetch(url, {
                method: 'POST',
                body: projectData, // Use FormData directly as the body
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                fetchProjects(); // Refresh projects after adding
                projectModal.style.display = 'none'; // Close modal
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while adding the project.");
            });
        }
    });

    // Function to delete a project
    function deleteProject(projectId) {
        fetch(`${baseUrl}/projects/${projectId}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            fetchProjects(); // Refresh projects after deleting
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while deleting the project.");
        });
    }

    // Fetch projects on page load
    fetchProjects();

    // Event listener for add project button
    addProjectButton.addEventListener('click', function() {
        openProjectModal(null, 'Add');
    });
});
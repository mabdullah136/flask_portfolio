const isUserLoggedIn = localStorage.getItem("isLoggedIn");
if (!isUserLoggedIn) {
  window.location.href = "/admin/login.html";
}

document.addEventListener("DOMContentLoaded", function() {
    const base = 'http://127.0.0.1:5000';
    const defaultIconClass = 'bx-x';
    const serviceList = document.getElementById('service-list');
    const updateServiceModal = document.getElementById('updateServiceModal');
    const closeUpdateServiceModal = document.querySelector('#updateServiceModal .close');
    let currentService; // Variable to store the currently selected service

    // Function to fetch services
    function fetchServices() {
        fetch(`${base}/services`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                serviceList.innerHTML = ''; // Clear existing services

                data.forEach(service => {
                    const servicesBox = document.createElement('div');
                    servicesBox.classList.add('service-box');

                    const serviceName = document.createElement('h3');
                    serviceName.textContent = service.title;
                    servicesBox.appendChild(serviceName);

                    const serviceDescription = document.createElement('p');
                    serviceDescription.textContent = service.description;
                    servicesBox.appendChild(serviceDescription);

                    const readMoreLink = document.createElement('a');
                    readMoreLink.href = service.link;
                    readMoreLink.textContent = 'Read More';
                    readMoreLink.classList.add('btn');
                    servicesBox.appendChild(readMoreLink);

                    // Add update and delete buttons
                    const updateButton = document.createElement('button');
                    updateButton.textContent = 'Update';
                    updateButton.addEventListener('click', () => openUpdateServiceModal(service));
                    servicesBox.appendChild(updateButton);

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.addEventListener('click', () => deleteService(service.id));
                    servicesBox.appendChild(deleteButton);

                    serviceList.appendChild(servicesBox);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while fetching services data.");
            });
    }

    // Function to open update service modal
    function openUpdateServiceModal(service) {
        currentService = service; // Store the currently selected service
        const updatedServiceNameInput = document.getElementById('updatedServiceNameInput');
        const updatedServiceDescriptionInput = document.getElementById('updatedServiceDescriptionInput');
        const updatedServiceLinkInput = document.getElementById('updatedServiceLinkInput');

        // Populate modal inputs with current service details
        updatedServiceNameInput.value = service.title;
        updatedServiceDescriptionInput.value = service.description;
        updatedServiceLinkInput.value = service.link;

        // Show modal
        updateServiceModal.style.display = 'block';
    }

    // Close modal when close button is clicked
    closeUpdateServiceModal.addEventListener('click', function() {
        updateServiceModal.style.display = 'none';
    });

    // Close modal when user clicks outside of it
    window.addEventListener('click', function(event) {
        if (event.target === updateServiceModal) {
            updateServiceModal.style.display = 'none';
        }
    });

    // Function to update a service
    document.getElementById('updateServiceForm').addEventListener('submit', function(event) {
        event.preventDefault();

        // Get updated service details
        const updatedServiceId = currentService.id; // Get the ID of the currently selected service
        const updatedServiceName = document.getElementById('updatedServiceNameInput').value;
        const updatedServiceDescription = document.getElementById('updatedServiceDescriptionInput').value;
        const updatedServiceLink = document.getElementById('updatedServiceLinkInput').value;

        fetch(`${base}/services/${updatedServiceId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: updatedServiceName,
                description: updatedServiceDescription,
                link: updatedServiceLink
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            fetchServices(); // Refresh services after updating
            updateServiceModal.style.display = 'none'; // Close modal
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while updating the service.");
        });
    });

    // Function to add a new service
    document.getElementById('addServiceForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const serviceName = document.getElementById('serviceNameInput').value;
        console.log(serviceName);
        const serviceDescription = document.getElementById('serviceDescriptionInput').value;
        const serviceLink = document.getElementById('serviceLinkInput').value;

        const body = {
            description: serviceDescription,
            title: serviceName,
            link: serviceLink
        };
        console.log(body);
        fetch(`${base}/service`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            fetchServices(); // Refresh services after adding
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while adding the service.");
        });
    });

    // Function to delete a service
    function deleteService(serviceId) {
        fetch(`${base}/services/${serviceId}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            fetchServices(); // Refresh services after deleting
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while deleting the service.");
        });
    }

    // Fetch services on page load
    fetchServices();
});
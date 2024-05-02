const baseUrl = 'http://127.0.0.1:5000';


// toggle icon navbar
let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');

}

// scroll section active link

let sections = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header nav a');
let currentActiveLink;

window.addEventListener('scroll', () => {
  sections.forEach(sec => {
    let top = window.pageYOffset;
    let offset = sec.offsetTop - 150;
    let height = sec.offsetHeight;
    let id = sec.getAttribute('id');

    if (top >= offset && top < offset + height) {
      let newActiveLink = document.querySelector("header nav a[href*='" + id + "']");
      if (newActiveLink !== currentActiveLink) {
        if (currentActiveLink) {
          currentActiveLink.classList.remove('active');
        }
        newActiveLink.classList.add('active');
        currentActiveLink = newActiveLink;
      }
    }
  });
  
    // sticky navbar
    let header = document.querySelector('header');
    header.classList.toggle('sticky',window.scrollY > 100);

    // remove toggle icon and navbar when click navbar link (scroll)
    
    menuIcon.classList.remove('bx-x');
    navbar.classList.remove('active');

});




// scroll reveal
ScrollReveal({
    // reset: true,
    distance: '80px',
    duration: 2000,
    delay:200
});

ScrollReveal().reveal('.home-content, .heading',{origin: 'top'});
ScrollReveal().reveal('.home-img, .services-container, .portfolio-box, .contact-form',{origin: 'bottom'});
ScrollReveal().reveal('.home-content h1, .about-img',{origin: 'left'});
ScrollReveal().reveal('.home-content p, .about-content',{origin: 'right'});

// // typed JS
// const typed = new Typed('.multiple-text', {
//     strings: ['Mobile Developer', 'Frontend Developer','Freelancer'],
//     typeSpeed: 100,
//     backSpeed: 0,
//     backDelay: 1000,
//     loop: true
// });


// fetch(`${baseUrl}/user_detail`)
// .then(response => response.json())
// .then(data => {
//     console.log(data.json());
//     let user = data.data;
//     // document.querySelector('.name').textContent = user.name;
//     // document.querySelector('.email').textContent = user.email;
//     // document.querySelector('.phone').textContent = user.phone;
//     // document.querySelector('.address').textContent = user.address;
//     // document.querySelector('.about-content').textContent = user.about;
//     // document.querySelector('.about-img').src = user.image;
//     // document.querySelector('.portfolio-img').src = user.image;
//     // document.querySelector('.portfolio-title').textContent = user.name;
//     // document.querySelector('.portfolio-desc').textContent = user.about;
//     // document.querySelector('.portfolio-link').href = user.portfolio;
// }
// )
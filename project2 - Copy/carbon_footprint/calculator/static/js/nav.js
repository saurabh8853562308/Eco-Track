// Navigation Active Link Handler
document.addEventListener('DOMContentLoaded', function() {
    // Get the current URL path
    const currentPath = window.location.pathname;
    
    // Get all navigation links (excluding auth links and logout link)
    const navLinks = document.querySelectorAll('.nav-link:not(.auth-link):not(.logout-link)');
    
    // Remove active class from all links
    navLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Map URL paths to nav link text for matching
    const pathMap = {
        '/': 'home',
        '/home/': 'home',
        '/calculator/': 'calculator',
        '/tips/': 'tips',
        '/about/': 'about'
    };
    
    // Determine which link should be active based on current path
    let activeLinkText = 'home'; // default to home
    
    if (currentPath === '/' || currentPath === '/home/') {
        activeLinkText = 'home';
    } else if (currentPath.includes('/calculator/')) {
        activeLinkText = 'calculator';
    } else if (currentPath.includes('/tips/')) {
        activeLinkText = 'tips';
    } else if (currentPath.includes('/about/')) {
        activeLinkText = 'about';
    }
    
    // Find and activate the appropriate link
    navLinks.forEach(link => {
        const linkText = link.textContent.trim().toLowerCase();
        if (linkText === activeLinkText) {
            link.classList.add('active');
        }
    });
});

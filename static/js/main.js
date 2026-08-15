document.addEventListener('DOMContentLoaded', () => {
    // Mobile Navigation Toggle
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = hamburger.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // Sticky Navbar shadow on scroll
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Intersection Observer for scroll animations
    const faders = document.querySelectorAll('.fade-in');
    
    const appearOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const appearOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('visible');
                
                // If it's a stat counter, trigger the animation
                if (entry.target.classList.contains('stat-item') || entry.target.querySelector('.stat-number')) {
                    const counter = entry.target.querySelector('.stat-number');
                    if (counter && counter.getAttribute('data-target') && !counter.classList.contains('counted')) {
                        animateCounter(counter);
                        counter.classList.add('counted');
                    }
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, appearOptions);

    faders.forEach(fader => {
        appearOnScroll.observe(fader);
    });

    // Stats Counter Animation
    function animateCounter(counter) {
        const target = +counter.getAttribute('data-target');
        const duration = 2000; // ms
        const increment = target / (duration / 16); // 60fps
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.innerText = Math.ceil(current) + '+';
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target + '+';
            }
        };
        updateCounter();
    }

    // ═══════════════ THEME TOGGLE ═══════════════
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('sphn-theme') || 'dark';
    
    // Apply saved theme on load
    if (savedTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        if (themeToggle) themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const icon = themeToggle.querySelector('i');
            
            if (currentTheme === 'light') {
                // Switch to dark
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('sphn-theme', 'dark');
                icon.style.transform = 'rotate(360deg)';
                setTimeout(() => {
                    icon.className = 'fas fa-moon';
                    icon.style.transform = '';
                }, 200);
            } else {
                // Switch to light
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('sphn-theme', 'light');
                icon.style.transform = 'rotate(360deg)';
                setTimeout(() => {
                    icon.className = 'fas fa-sun';
                    icon.style.transform = '';
                }, 200);
            }
        });
    }
});

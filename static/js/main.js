document.addEventListener('DOMContentLoaded', () => {

    // LOADER
    const loader = document.getElementById('loader');

    window.addEventListener('load', () => {
        setTimeout(() => {
            if (loader) loader.classList.add('is-hidden');
            document.body.classList.add('is-loaded');
        }, 600);
    });

    if (document.readyState === 'complete') {
        setTimeout(() => {
            if (loader) loader.classList.add('is-hidden');
            document.body.classList.add('is-loaded');
        }, 300);
    }

    // CUSTOM CURSOR
    const cursor = document.querySelector('.cursor');
    const cursorDot = document.querySelector('.cursor__dot');
    const cursorCircle = document.querySelector('.cursor__circle');

    if (window.innerWidth > 1024 && cursor && cursorDot && cursorCircle) {
        let mx = 0, my = 0;
        let dx = 0, dy = 0;
        let cx = 0, cy = 0;

        document.addEventListener('mousemove', (e) => {
            mx = e.clientX;
            my = e.clientY;
        }, { passive: true });

        function tick() {
            dx += (mx - dx) * 0.3;
            dy += (my - dy) * 0.3;
            cursorDot.style.left = dx + 'px';
            cursorDot.style.top = dy + 'px';

            cx += (mx - cx) * 0.12;
            cy += (my - cy) * 0.12;
            cursorCircle.style.left = cx + 'px';
            cursorCircle.style.top = cy + 'px';

            requestAnimationFrame(tick);
        }
        tick();

        document.querySelectorAll('a, button, .story-card, .archive-item, .magazine-cover').forEach(el => {
            el.addEventListener('mouseenter', () => cursor.classList.add('cursor--hover'));
            el.addEventListener('mouseleave', () => cursor.classList.remove('cursor--hover'));
        });

        document.addEventListener('mouseleave', () => { cursor.style.opacity = '0'; });
        document.addEventListener('mouseenter', () => { cursor.style.opacity = '1'; });
    }

    // MINIMAL GSAP FULLSCREEN MENU
    const nav = document.getElementById('nav');
    const navToggle = document.getElementById('navToggle');
    const menu = document.getElementById('menu');
    const menuClose = document.getElementById('menuClose');
    const menuItems = document.querySelectorAll('[data-menu-item]');

    let menuOpen = false;

    // Toggle Menu
    if (navToggle && menu) {
        navToggle.addEventListener('click', openMenu);

        if (menuClose) {
            menuClose.addEventListener('click', closeMenu);
        }

        // Close on menu item click
        menuItems.forEach(item => {
            item.addEventListener('click', (e) => {
                const href = item.getAttribute('href');
                if (href && href.startsWith('#')) {
                    e.preventDefault();
                    closeMenu();
                    setTimeout(() => {
                        const target = document.querySelector(href);
                        if (target) {
                            const offset = 80;
                            const targetPosition = target.offsetTop - offset;
                            window.scrollTo({
                                top: targetPosition,
                                behavior: 'smooth'
                            });
                        }
                    }, 800);
                }
            });
        });

        // Close on ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && menuOpen) closeMenu();
        });
    }

    function openMenu() {
        if (menuOpen) return;

        menuOpen = true;
        menu.classList.add('is-active');
        navToggle.classList.add('active');
        document.body.style.overflow = 'hidden';

        if (typeof gsap !== 'undefined') {
            const tl = gsap.timeline();

            tl.to('.menu__bg', {
                scaleY: 1,
                duration: 0.6,
                ease: 'power3.inOut'
            })
                .to('.menu__header', {
                    opacity: 1,
                    duration: 0.4,
                    ease: 'power2.out'
                }, '-=0.3')
                .to('.menu__link-text', {
                    y: 0,
                    opacity: 1,
                    duration: 0.6,
                    stagger: 0.08,
                    ease: 'power3.out'
                }, '-=0.2')
                .to('.menu__link-number', {
                    y: 0,
                    opacity: 1,
                    duration: 0.5,
                    stagger: 0.08,
                    ease: 'power2.out'
                }, '-=0.5')
                .to('.menu__footer', {
                    opacity: 1,
                    duration: 0.5,
                    ease: 'power2.out'
                }, '-=0.3');
        }
    }

    function closeMenu() {
        if (!menuOpen) return;

        menuOpen = false;
        navToggle.classList.remove('active');

        if (typeof gsap !== 'undefined') {
            const tl = gsap.timeline({
                onComplete: () => {
                    menu.classList.remove('is-active');
                    document.body.style.overflow = '';

                    // Reset all elements
                    gsap.set('.menu__link-text, .menu__link-number', {
                        y: '100%',
                        opacity: 0
                    });
                    gsap.set('.menu__header, .menu__footer', {
                        opacity: 0
                    });
                    gsap.set('.menu__bg', {
                        scaleY: 0
                    });
                }
            });

            tl.to('.menu__footer', {
                opacity: 0,
                duration: 0.3,
                ease: 'power2.in'
            })
                .to('.menu__link-text, .menu__link-number', {
                    y: -30,
                    opacity: 0,
                    duration: 0.4,
                    stagger: 0.04,
                    ease: 'power2.in'
                }, '-=0.2')
                .to('.menu__header', {
                    opacity: 0,
                    duration: 0.3,
                    ease: 'power2.in'
                }, '-=0.3')
                .to('.menu__bg', {
                    scaleY: 0,
                    transformOrigin: 'bottom',
                    duration: 0.5,
                    ease: 'power3.inOut'
                }, '-=0.2');
        } else {
            menu.classList.remove('is-active');
            document.body.style.overflow = '';
        }
    }

    // MENU LOGO TRICOLOR GRADIENT ANIMATION
    if (typeof gsap !== 'undefined') {
        const menuLogoText = document.getElementById('menuLogoText');
        if (menuLogoText) {
            gsap.to(menuLogoText, {
                backgroundPosition: '400% 50%',
                duration: 20,
                ease: 'none',
                repeat: -1
            });
            console.log('✓ Menu logo tricolor animation initialized');
        }
    }

    // NAVBAR SCROLL BEHAVIOR
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;

        // Add scrolled class
        if (currentScroll > 100) {
            nav.classList.add('nav--scrolled');
        } else {
            nav.classList.remove('nav--scrolled');
        }

        // Hide on scroll down, show on scroll up
        if (currentScroll > lastScroll && currentScroll > 200 && !menuOpen) {
            nav.style.transform = 'translateY(-100%)';
        } else {
            nav.style.transform = 'translateY(0)';
        }

        lastScroll = currentScroll;
    }, { passive: true });

    // NAVBAR VISITOR COUNTER ANIMATION
    if (typeof gsap !== 'undefined') {
        const visitorCountEl = document.querySelector('.nav__visitor-count');

        if (visitorCountEl) {
            const targetCount = parseInt(visitorCountEl.getAttribute('data-visitor-count')) || 0;

            // Animate counter on page load
            gsap.fromTo(visitorCountEl,
                { textContent: 0 },
                {
                    textContent: targetCount,
                    duration: 2,
                    ease: 'power2.out',
                    snap: { textContent: 1 },
                    delay: 0.8,
                    onUpdate() {
                        const current = Math.ceil(parseFloat(visitorCountEl.textContent));
                        // Format with commas
                        visitorCountEl.textContent = current.toLocaleString();
                    }
                }
            );

            console.log('✓ Visitor counter animation initialized');
        }
    }

    // GSAP SCROLL ANIMATIONS
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);

        ScrollTrigger.config({
            limitCallbacks: true,
            syncInterval: 16
        });

        const noMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (!noMotion) {

            // Hero entrance animation
            const heroTl = gsap.timeline({ delay: 0.6 });

            heroTl
                .from('.hero__background', {
                    opacity: 0,
                    duration: 1.2,
                    ease: 'power2.out'
                })
                .from('.hero__title-line--indian', {
                    y: 50,
                    opacity: 0,
                    duration: 1,
                    ease: 'power3.out'
                }, '-=0.8')
                .from('.hero__title-line--thozhilali', {
                    y: 50,
                    opacity: 0,
                    duration: 1,
                    ease: 'power3.out'
                }, '-=0.7')
                .from('.hero__subtitle', {
                    y: 25,
                    opacity: 0,
                    duration: 0.8,
                    ease: 'power2.out'
                }, '-=0.5')
                .from('.hero__meta', {
                    y: 20,
                    opacity: 0,
                    duration: 0.7,
                    ease: 'power2.out'
                }, '-=0.4')
                .from('.hero__cta', {
                    y: 20,
                    opacity: 0,
                    duration: 0.6,
                    ease: 'power2.out'
                }, '-=0.3');

            // Navbar logo animation
            gsap.from('.nav__logo-img', {
                scale: 0.8,
                opacity: 0,
                duration: 0.8,
                ease: 'power3.out',
                delay: 0.5
            });

            // Nav toggle animation
            gsap.from('.nav__toggle', {
                scale: 0.8,
                opacity: 0,
                duration: 0.8,
                ease: 'power3.out',
                delay: 0.6
            });


            // Image reveals on scroll
            gsap.utils.toArray('[data-reveal-image]').forEach(el => {
                if (el.closest('.hero')) return;

                gsap.fromTo(el,
                    { clipPath: 'inset(20% 0 0 0)' },
                    {
                        clipPath: 'inset(0% 0 0 0)',
                        duration: 0.9,
                        ease: 'power2.out',
                        scrollTrigger: {
                            trigger: el,
                            start: 'top 85%',
                            once: true
                        }
                    }
                );
            });


            // Section text reveals
            gsap.utils.toArray('[data-reveal]').forEach(el => {
                const isHero = el.closest('.hero');
                const isFeaturedHeader = el.classList.contains('section-label') && el.closest('.featured__header');

                if (isHero || isFeaturedHeader) {
                    return;
                }

                gsap.from(el, {
                    y: 20,
                    opacity: 0,
                    duration: 0.7,
                    ease: 'power2.out',
                    scrollTrigger: {
                        trigger: el,
                        start: 'top 88%',
                        once: true
                    }
                });
            });


            // Magazine cover
            gsap.from('.magazine-cover', {
                y: 28,
                scale: 0.98,
                opacity: 0,
                duration: 0.9,
                ease: 'power3.out',
                scrollTrigger: {
                    trigger: '.featured',
                    start: 'top 72%',
                    once: true
                }
            });

            gsap.from('.featured__text > *', {
                y: 20,
                opacity: 0,
                duration: 0.7,
                stagger: 0.08,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: '.featured__text',
                    start: 'top 80%',
                    once: true
                }
            });


            // Story cards
            gsap.from('.story-card', {
                y: 28,
                opacity: 0,
                duration: 0.7,
                stagger: 0.06,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: '.stories__grid',
                    start: 'top 80%',
                    once: true
                }
            });


            // Archive items
            gsap.from('.archive-item', {
                y: 24,
                opacity: 0,
                duration: 0.6,
                stagger: 0.05,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: '.archive__grid',
                    start: 'top 80%',
                    once: true
                }
            });


            // Stats counter
            document.querySelectorAll('.stat-item__number').forEach(stat => {
                const target = parseInt(stat.getAttribute('data-count'));
                if (isNaN(target)) return;

                gsap.fromTo(stat,
                    { textContent: 0 },
                    {
                        textContent: target,
                        duration: 2,
                        ease: 'power2.out',
                        snap: { textContent: 1 },
                        scrollTrigger: {
                            trigger: stat,
                            start: 'top 85%',
                            once: true
                        },
                        onUpdate() {
                            stat.textContent = Math.ceil(parseFloat(stat.textContent));
                        }
                    }
                );
            });


            // Footer
            gsap.from('.footer__main > *', {
                y: 18,
                opacity: 0,
                duration: 0.6,
                stagger: 0.08,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: '.footer',
                    start: 'top 88%',
                    once: true
                }
            });

            console.log('✓ ScrollTrigger animations:', ScrollTrigger.getAll().length, 'active');
        }
    }

    // RESIZE HANDLER
    let ww = window.innerWidth;
    window.addEventListener('resize', () => {
        const nw = window.innerWidth;
        if ((ww <= 1024 && nw > 1024) || (ww > 1024 && nw <= 1024)) {
            if (typeof ScrollTrigger !== 'undefined') ScrollTrigger.refresh();
        }
        ww = nw;
    });

    // ACCESSIBILITY
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') document.body.classList.add('keyboard-nav');
    });
    document.addEventListener('mousedown', () => {
        document.body.classList.remove('keyboard-nav');
    });

});

/** @odoo-module **/
/**
 * Mutego Distribution — Website JavaScript
 * Odoo 17 Compatible
 */

import { onMounted, onWillUnmount } from "@odoo/owl";

// ── Sticky Header Active State ─────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {

    // Mark active nav link based on current path
    const currentPath = window.location.pathname;
    document.querySelectorAll('.mutego-header .nav-link').forEach(function (link) {
        const href = link.getAttribute('href');
        if (href && (currentPath === href || (href !== '/' && currentPath.startsWith(href)))) {
            link.classList.add('active');
        }
    });

    // ── Scroll-based header shadow ───────────────────────────────
    const header = document.getElementById('mutego-header');
    if (header) {
        function updateHeaderShadow() {
            if (window.scrollY > 20) {
                header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.12)';
            } else {
                header.style.boxShadow = '0 1px 3px rgba(0,0,0,0.08)';
            }
        }
        window.addEventListener('scroll', updateHeaderShadow, { passive: true });
        updateHeaderShadow();
    }

    // ── Smooth scroll for anchor links ──────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ── Scroll reveal animation ──────────────────────────────────
    const revealElements = document.querySelectorAll(
        '.product-card, .branch-card, .news-card, .value-card, .mvv-card, .brand-card, .ops-card, .branch-detail-card'
    );

    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        revealElements.forEach(function (el) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            revealObserver.observe(el);
        });
    }

    // ── Animated stat counters ──────────────────────────────────
    const statNumbers = document.querySelectorAll('.mutego-stats-bar .stat-number');

    function animateCount(el) {
        const text = el.textContent.trim();
        const hasPlus = text.includes('+');
        const hasK = text.toLowerCase().includes('k');
        const numStr = text.replace(/[^0-9]/g, '');
        const target = parseInt(numStr, 10);
        if (isNaN(target) || target === 0) return;

        const duration = 1500;
        const start = performance.now();

        function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(ease * target);

            let display = current.toLocaleString();
            if (hasK) display = (current / 1000).toFixed(0) + 'K';
            if (hasPlus) display += '+';
            el.textContent = display;

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    if ('IntersectionObserver' in window) {
        const statsObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCount(entry.target);
                    statsObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statNumbers.forEach(function (el) { statsObserver.observe(el); });
    }

    // ── Contact form validation feedback ────────────────────────
    const contactForm = document.querySelector('.mutego-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            const requiredFields = contactForm.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(function (field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    valid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
                contactForm.querySelector('.is-invalid')?.focus();
            } else {
                const btn = contactForm.querySelector('[type="submit"]');
                if (btn) {
                    btn.disabled = true;
                    btn.innerHTML = '<i class="fa fa-spinner fa-spin me-2"></i>Sending...';
                }
            }
        });

        // Live validation on blur
        contactForm.querySelectorAll('[required]').forEach(function (field) {
            field.addEventListener('blur', function () {
                if (!this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                }
            });
        });
    }

    // ── Auto-dismiss success alert ───────────────────────────────
    const successAlert = document.querySelector('.mutego-alert-success');
    if (successAlert) {
        setTimeout(function () {
            successAlert.style.transition = 'opacity 0.5s ease';
            successAlert.style.opacity = '0';
            setTimeout(function () { successAlert.remove(); }, 500);
        }, 5000);
    }

});
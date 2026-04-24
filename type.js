document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Language Selector Logic
    const currentLangBtn = document.getElementById('currentLangBtn');
    const langDropdown = document.getElementById('langDropdown');
    const currentFlag = document.getElementById('currentFlag');
    const currentLangText = document.getElementById('currentLangText');
    const langOptions = document.querySelectorAll('.lang-option');

    if (currentLangBtn && langDropdown) {
        currentLangBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            langDropdown.classList.toggle('show');
            currentLangBtn.classList.toggle('active');
        });

        // Google Translate Integration
        // 1. Inject hidden div
        const gtDiv = document.createElement('div');
        gtDiv.id = 'google_translate_element';
        gtDiv.style.display = 'none';
        document.body.appendChild(gtDiv);

        // 2. Inject Google Translate script
        window.googleTranslateElementInit = function() {
            new google.translate.TranslateElement({
                pageLanguage: 'tr',
                includedLanguages: 'tr,en,fr,ar',
                autoDisplay: false
            }, 'google_translate_element');
        };
        const gtScript = document.createElement('script');
        gtScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        document.head.appendChild(gtScript);

        // 3. Inject CSS to hide Google's default top banner
        const style = document.createElement('style');
        style.innerHTML = `
            .goog-te-banner-frame.skiptranslate { display: none !important; }
            body { top: 0px !important; }
            #goog-gt-tt { display: none !important; }
            .goog-text-highlight { background-color: transparent !important; box-shadow: none !important; }
        `;
        document.head.appendChild(style);

        // Load saved language from cookie to update UI on page load
        const match = document.cookie.match(/googtrans=\/tr\/([a-z]{2})/);
        if (match) {
            const savedLang = match[1].toUpperCase();
            const option = Array.from(langOptions).find(opt => opt.getAttribute('data-lang') === savedLang);
            if (option) {
                currentLangText.textContent = savedLang;
                currentFlag.src = `https://flagcdn.com/w20/${option.getAttribute('data-flag')}.png`;
            }
        }

        langOptions.forEach(option => {
            option.addEventListener('click', () => {
                const lang = option.getAttribute('data-lang');
                const flag = option.getAttribute('data-flag');
                
                // Update UI based on selection natively
                currentLangText.textContent = lang;
                currentFlag.src = `https://flagcdn.com/w20/${flag}.png`;
                
                // Trigger Google Translate
                const langCode = lang.toLowerCase();
                const gtCombo = document.querySelector('.goog-te-combo');
                
                if (gtCombo) {
                    gtCombo.value = langCode;
                    gtCombo.dispatchEvent(new Event('change'));
                } else {
                    // Fallback: set cookie and reload
                    document.cookie = `googtrans=/tr/${langCode}; path=/`;
                    window.location.reload();
                }

                // Close dropdown
                langDropdown.classList.remove('show');
                currentLangBtn.classList.remove('active');
            });
        });

        // Click outside to remotely close the dropdown anywhere
        document.addEventListener('click', (e) => {
            if (!currentLangBtn.contains(e.target) && !langDropdown.contains(e.target)) {
                langDropdown.classList.remove('show');
                currentLangBtn.classList.remove('active');
            }
        });
    }

    // Lightbox Gallery Logic
    const expandableImages = document.querySelectorAll('.expandable-image, #expandableImage');
    const lightboxModal = document.getElementById('lightboxModal');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxClose = document.getElementById('lightboxClose');

    if (expandableImages.length > 0 && lightboxModal) {
        let currentLightboxIndex = 0;
        const lightboxPrevBtn = document.getElementById('lightboxPrevBtn');
        const lightboxNextBtn = document.getElementById('lightboxNextBtn');
        const lightboxCounter = document.getElementById('lightboxCounter');

        const updateCounter = () => {
            if (lightboxCounter) lightboxCounter.textContent = (currentLightboxIndex + 1) + " / " + expandableImages.length;
        };

        const openLightbox = (index) => {
            currentLightboxIndex = index;
            if (lightboxImg) {
                lightboxImg.src = expandableImages[index] ? expandableImages[index].src : '';
            }
            updateCounter();
            lightboxModal.classList.add('active');
        };

        const closeLightbox = () => {
            lightboxModal.classList.remove('active');
        };

        expandableImages.forEach((img, index) => {
            const targetElement = img.closest('.expandable-slide') || img.parentElement;
            targetElement.style.cursor = 'pointer'; 
            targetElement.addEventListener('click', () => openLightbox(index)); 
        });
        
        if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);

        if (lightboxPrevBtn) {
            lightboxPrevBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                currentLightboxIndex = (currentLightboxIndex - 1 + expandableImages.length) % expandableImages.length;
                if (lightboxImg) lightboxImg.src = expandableImages[currentLightboxIndex].src;
                updateCounter();
            });
        }
        
        if (lightboxNextBtn) {
            lightboxNextBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                currentLightboxIndex = (currentLightboxIndex + 1) % expandableImages.length;
                if (lightboxImg) lightboxImg.src = expandableImages[currentLightboxIndex].src;
                updateCounter();
            });
        }

        // Disariya tiklaninca modal'i kapat
        lightboxModal.addEventListener('click', (e) => {
            if (e.target === lightboxModal) {
                closeLightbox();
            }
        });

        // ESC tusuna basinca modal'i kapat
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightboxModal.classList.contains('active')) {
                closeLightbox();
            }
        });
    }

    // Parfüm Sayfasi Icin Özel Büyütme (Isolated Modal) JS
    const pfExpandableImage = document.getElementById('pfExpandableImage');
    const pfModalOverlay = document.getElementById('pfModalOverlay');
    const pfModalImage = document.getElementById('pfModalImage');
    const pfModalClose = document.getElementById('pfModalClose');
    const pfZoomIconBtn = document.getElementById('pfZoomIconBtn');

    if (pfExpandableImage && pfModalOverlay) {
        const openPfLightbox = () => {
            pfModalImage.src = pfExpandableImage.src;
            pfModalOverlay.classList.add('active');
        };

        const closePfLightbox = () => {
            pfModalOverlay.classList.remove('active');
        };

        // Resim ve Ikon uzerine tiklayinca acilmasini sagla
        pfExpandableImage.parentElement.addEventListener('click', openPfLightbox);
        pfModalClose.addEventListener('click', closePfLightbox);

        pfModalOverlay.addEventListener('click', (e) => {
            if (e.target === pfModalOverlay) closePfLightbox();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && pfModalOverlay.classList.contains('active')) {
                closePfLightbox();
            }
        });
    }

    // --- Slider Logic extracted from parfum-koku-mak.html ---
    const productSlider = document.getElementById('productSlider');
    const sliderDots = document.querySelectorAll('.slider-dot');
    if (productSlider && sliderDots.length > 0) {
        productSlider.addEventListener('scroll', () => {
            const slideWidth = productSlider.offsetWidth;
            if (slideWidth > 0) {
                const index = Math.round(productSlider.scrollLeft / slideWidth);
                sliderDots.forEach((dot, i) => dot.classList.toggle('active', i === index));
            }
        });
        sliderDots.forEach((dot, i) => {
            dot.addEventListener('click', (e) => {
                e.stopPropagation();
                productSlider.scrollTo({ left: productSlider.offsetWidth * i, behavior: 'smooth' });
            });
        });

        const prevSBtn = document.getElementById('sliderBtnPrev');
        const nextSBtn = document.getElementById('sliderBtnNext');
        if(prevSBtn) {
            prevSBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const slideWidth = productSlider.offsetWidth;
                const index = Math.round(productSlider.scrollLeft / slideWidth);
                if (index === 0) {
                    productSlider.scrollTo({ left: slideWidth * (sliderDots.length - 1), behavior: 'smooth' });
                } else {
                    productSlider.scrollBy({ left: -slideWidth, behavior: 'smooth' });
                }
            });
        }
        if(nextSBtn) {
            nextSBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const slideWidth = productSlider.offsetWidth;
                const index = Math.round(productSlider.scrollLeft / slideWidth);
                if (index === sliderDots.length - 1) {
                    productSlider.scrollTo({ left: 0, behavior: 'smooth' });
                } else {
                    productSlider.scrollBy({ left: slideWidth, behavior: 'smooth' });
                }
            });
        }
    }
});

// --- KORUMA KODLARI (Sağ Tık ve Kısayol Engelleme) ---
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
});

document.addEventListener('keydown', function(e) {
    // F12
    if (e.key === 'F12' || e.keyCode === 123) {
        e.preventDefault();
        return false;
    }
    // Ctrl+Shift+I / Cmd+Option+I (Geliştirici Konsolu)
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'I' || e.key === 'i')) {
        e.preventDefault();
        return false;
    }
    // Ctrl+Shift+J / Cmd+Option+J
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'J' || e.key === 'j')) {
        e.preventDefault();
        return false;
    }
    // Ctrl+U / Cmd+Option+U (Kaynağı Görüntüle)
    if ((e.ctrlKey || e.metaKey) && (e.key === 'U' || e.key === 'u')) {
        e.preventDefault();
        return false;
    }
    // Ctrl+S / Cmd+S (Kaydet)
    if ((e.ctrlKey || e.metaKey) && (e.key === 'S' || e.key === 's')) {
        e.preventDefault();
        return false;
    }
    // Ctrl+P / Cmd+P (Yazdır)
    if ((e.ctrlKey || e.metaKey) && (e.key === 'P' || e.key === 'p')) {
        e.preventDefault();
        return false;
    }
});

// Sürüklemeyi tamamen iptal et (özellikle resimler için ek JS önlemi)
document.addEventListener('dragstart', function(e) {
    e.preventDefault();
});

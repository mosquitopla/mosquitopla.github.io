document.addEventListener('DOMContentLoaded', () => {
    const burgerBtn = document.querySelector('.burger-btn');
    const mobileMenu = document.querySelector('.menu');

    if (burgerBtn && mobileMenu) {
        burgerBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            
            burgerBtn.classList.toggle('is-active');
            mobileMenu.classList.toggle('is-open');
        });
        
        mobileMenu.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    document.addEventListener('click', () => {
        if (mobileMenu && mobileMenu.classList.contains('is-open')) {
            mobileMenu.classList.remove('is-open');
            if (burgerBtn) burgerBtn.classList.remove('is-active');
        }
    });
});


const reviewsSwiperExists = document.querySelector('.reviews-swiper');

if (reviewsSwiperExists) {
    const reviewsSwiper = new Swiper('.reviews-swiper', {
        loop: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
}
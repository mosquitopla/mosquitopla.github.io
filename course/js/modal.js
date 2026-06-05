const modalOverlay = document.querySelector('.modal-wrap');
const cartHeaderBtn = document.querySelector('.cart'); 
const closeModalBtn = document.getElementById('closeModalBtn');
const requestForm = document.getElementById('requestForm');
const phoneInput = document.getElementById('userPhone');

if (cartHeaderBtn && modalOverlay) {
    cartHeaderBtn.addEventListener('click', function(event) {
        modalOverlay.classList.add('is-open');
    });
}

if (closeModalBtn) {
    closeModalBtn.addEventListener('click', () => {
        modalOverlay.classList.remove('is-open');
    });
}

if (modalOverlay) {
    modalOverlay.addEventListener('click', (event) => {
        if (event.target === event.currentTarget) {
            modalOverlay.classList.remove('is-open');
        }
    });
}


if (phoneInput) {
    phoneInput.addEventListener('input', function(e) {
        let inputNumbersValue = e.target.value.replace(/\D/g, '');
        let formattedInputValue = '';

        if (inputNumbersValue.startsWith('38')) {
            inputNumbersValue = inputNumbersValue.substring(2);
        }

        if (inputNumbersValue.length > 0) {
            formattedInputValue = '+38 (' + inputNumbersValue.substring(0, 3);
        }
        if (inputNumbersValue.length >= 4) {
            formattedInputValue += ') ' + inputNumbersValue.substring(3, 6);
        }
        if (inputNumbersValue.length >= 7) {
            formattedInputValue += '-' + inputNumbersValue.substring(6, 8);
        }
        if (inputNumbersValue.length >= 9) {
            formattedInputValue += '-' + inputNumbersValue.substring(8, 10);
        }

        e.target.value = formattedInputValue;
    });

    phoneInput.addEventListener('keydown', function(e) {
        if (e.keyCode === 8 && e.target.value.length <= 5) {
            e.target.value = '';
        }
    });
}


if (requestForm) {
    requestForm.addEventListener('submit', function(event) {
        event.preventDefault(); 

        const lastName = document.getElementById('userLastName').value;
        const firstName = document.getElementById('userName').value;
        const phone = phoneInput.value;

        alert(`Дякуємо, ${lastName} ${firstName}! Ваш запит успішно відправлено. Ми зв'яжемося з вами за телефоном ${phone}.`)
        
        modalOverlay.classList.remove('is-open');
        requestForm.reset();
    });
}
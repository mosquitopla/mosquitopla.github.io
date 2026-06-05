const products = [
  {
    id: 1,
    badge: 'Овочі',
    image: 'images/shop/products/kapusta_brokoli.png',
    alt: 'Броколі',
    name: 'Капуста Броколі',
    oldPrice: '20.00',
    price: '13.00',
    stars: 5,
  },
  {
    id: 2,
    badge: 'Фрукти',
    image: 'images/shop/products/banana.png',
    alt: 'Банани',
    name: 'Органічні Банани',
    oldPrice: '20.00',
    price: '14.00',
    stars: 5,
  },
  {
    id: 3,
    badge: 'Горіхи',
    image: 'images/shop/products/almond.png',
    alt: 'Горіхи',
    name: 'Мигдаль',
    oldPrice: '35.00',
    price: '25.00',
    stars: 5,
  },
  {
    id: 4,
    badge: 'Овочі',
    image: 'images/shop/products/tomaty_cherry.png',
    alt: 'Томати чері',
    name: 'Червоні Томати Чері',
    oldPrice: '25.00',
    price: '17.00',
    stars: 5,
  },
  {
    id: 5,
    badge: 'Овочі',
    image: 'images/shop/products/cucumber.png',
    alt: 'Огірки',
    name: 'Огірки',
    oldPrice: '20.00',
    price: '11.00',
    stars: 5,
  },
  {
    id: 6,
    badge: 'Горіхи',
    image: 'images/shop/products/hazelnut.png',
    alt: 'Фундук',
    name: 'Лісовий Фундук',
    oldPrice: '28.00',
    price: '22.00',
    stars: 5,
  },
  {
    id: 7,
    badge: 'Ферма',
    image: 'images/shop/products/eggs.png',
    alt: 'Яйця',
    name: 'Домашні Яйця (коробка)',
    oldPrice: '24.00',
    price: '17.00',
    stars: 5,
  },
  {
    id: 8,
    badge: 'Бакалія',
    image: 'images/shop/products/bread.png',
    alt: 'Хліб',
    name: 'Житній хліб на заквасці',
    oldPrice: '20.00',
    price: '15.00',
    stars: 5,
  },
  {
    id: 9,
    badge: 'Овочі',
    image: 'images/shop/products/garlic.png',
    alt: 'Часник Білий',
    name: 'Часник білий',
    oldPrice: '20.00',
    price: '13.00',
    stars: 5,
  },
  {
    id: 10,
    badge: 'Фрукти',
    image: 'images/shop/products/apple.png',
    alt: 'Яблука «Чемпіон»',
    name: 'Яблука «Чемпіон»',
    oldPrice: '20.00',
    price: '14.00',
    stars: 5,
  },
  {
    id: 11,
    badge: 'Горіхи',
    image: 'images/shop/products/nut-greek.png',
    alt: 'Горіх Волоський',
    name: 'Горіх Волоський',
    oldPrice: '35.00',
    price: '25.00',
    stars: 5,
  },
  {
    id: 12,
    badge: 'Овочі',
    image: 'images/shop/products/tomatoes.png',
    alt: 'Помідори',
    name: 'Помідори',
    oldPrice: '25.00',
    price: '17.00',
    stars: 5,
  },
  {
    id: 13,
    badge: 'Ягоди',
    image: 'images/shop/products/garnet.png',
    alt: 'Гранат',
    name: 'Гранат',
    oldPrice: '20.00',
    price: '11.00',
    stars: 5,
  },
  {
    id: 14,
    badge: 'Ягоди',
    image: 'images/shop/products/grape.png',
    alt: 'Виноград Кишмиш',
    name: 'Виноград Кишмиш',
    oldPrice: '28.00',
    price: '22.00',
    stars: 5,
  },
  {
    id: 15,
    badge: 'Ягоди',
    image: 'images/shop/products/strawberry.png',
    alt: 'Полуниця Садова',
    name: 'Полуниця Садова',
    oldPrice: '24.00',
    price: '17.00',
    stars: 5,
  },
  {
    id: 16,
    badge: 'Фрукти',
    image: 'images/shop/products/pear.png',
    alt: 'Груша',
    name: 'Груша',
    oldPrice: '20.00',
    price: '15.00',
    stars: 5,
  },
]

function renderStars(count) {
  return Array.from({ length: count }, () => `
    <svg class="star-icon"><use href="icons/sprite.svg#star-icon"></use></svg>
  `).join('')
}

function renderProductCard(product) {
  return `
    <article class="item-card">
      <span class="item-badge">${product.badge}</span>
      <div class="item-img">
        <img src="${product.image}" alt="${product.alt}">
      </div>
      <h4 class="item-name">${product.name}</h4>
      <div class="item-footer">
        <div class="price">
          <span class="old-price">${product.oldPrice} ₴</span> ${product.price} ₴
        </div>
        <div class="product-stars">
          ${renderStars(product.stars)}
        </div>
      </div>
    </article>
  `
}

const productsGrid = document.getElementById('productsList')

productsGrid.innerHTML = products
  .map((product) => renderProductCard(product))
  .join('')
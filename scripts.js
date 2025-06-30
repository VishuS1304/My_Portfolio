// frontend/scripts.js

// ——————————————————————————————
// Utility: Debounce
// ——————————————————————————————
function debounce(fn, wait = 50) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), wait);
  };
}

document.addEventListener('DOMContentLoaded', () => {
  // ———————————————————————————————————————————
  // 1) Mobile Menu Toggle + Auto‑close
  // ———————————————————————————————————————————
  const menu   = document.getElementById('menu');
  const toggle = document.querySelector('.mobile-toggle');
  function toggleMobileMenu() {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    menu.classList.toggle('active');
  }
  if (toggle && menu) {
    toggle.addEventListener('click', e => {
      e.stopPropagation();
      toggleMobileMenu();
    });
    document.addEventListener('click', e => {
      if (!menu.contains(e.target) && !toggle.contains(e.target)) {
        menu.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
    document.querySelectorAll('#menu a').forEach(link => {
      link.addEventListener('click', () => {
        menu.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // ———————————————————————————————————————————
  // 2) Header Hide on Scroll
  // ———————————————————————————————————————————
  (function () {
    let lastY = 0;
    const header = document.querySelector('header');
    window.addEventListener('scroll', debounce(() => {
      const currentY = window.scrollY;
      const isMenuOpen = menu && menu.classList.contains('active');
      if (!isMenuOpen) {
        if (currentY > lastY && currentY > 100) {
          header.classList.add('hide');
        } else {
          header.classList.remove('hide');
        }
      }
      lastY = currentY;
    }, 100));
  })();

  // ———————————————————————————————————————————
  // 3) Chatbot Widget Logic
  // ———————————————————————————————————————————
  const chatContainer = document.getElementById('chatbot-container');
  const chatToggle    = document.getElementById('chatbot-toggle');
  const chatWidget    = document.getElementById('chatbot-widget');
  const chatClose     = document.getElementById('chatbot-close');
  const chatMessages  = document.getElementById('chatbot-messages');
  const chatForm      = document.getElementById('chatbot-form');
  const chatInput     = document.getElementById('chatbot-input');
  const chatSend      = document.getElementById('chatbot-send');
  const API_BASE      = 'http://127.0.0.1:8000';
  let sse = null;

  function openChat() {
    chatContainer.classList.add('expanded');
    chatToggle.setAttribute('aria-expanded', 'true');
    chatWidget.style.display = 'flex';
    chatInput.focus();
  }
  function closeChat() {
    chatContainer.classList.remove('expanded');
    chatToggle.setAttribute('aria-expanded', 'false');
    chatWidget.style.display = 'none';
    if (sse) { sse.close(); sse = null; }
    chatSend.disabled = false;
  }

  chatToggle.addEventListener('click', () =>
    chatContainer.classList.contains('expanded') ? closeChat() : openChat()
  );
  chatClose.addEventListener('click', closeChat);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && chatContainer.classList.contains('expanded')) {
      closeChat();
    }
  });

  function appendMessage(sender, text='') {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
  }

  chatForm.addEventListener('submit', e => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;
    openChat();
    appendMessage('user', text);
    chatInput.value = '';
    chatSend.disabled = true;
    const botDiv = appendMessage('bot');
    sse = new EventSource(`${API_BASE}/chat/stream?message=${encodeURIComponent(text)}`);
    sse.onmessage = evt => {
      try {
        const { reply } = JSON.parse(evt.data);
        botDiv.textContent += reply;
        chatMessages.scrollTop = chatMessages.scrollHeight;
      } catch {}
    };
    sse.addEventListener('end', () => { chatSend.disabled = false; sse.close(); sse = null; });
    sse.onerror = () => {
      botDiv.textContent += '\n[Connection error]';
      chatSend.disabled = false;
      if (sse) { sse.close(); sse = null; }
    };
  });

  window.addEventListener('beforeunload', () => { if (sse) sse.close(); });

  // ———————————————————————————————————————————
  // 4) Scroll‑to‑Top Button
  // ———————————————————————————————————————————
  const scrollBtn = document.getElementById('scroll-up');
  const toggleScrollBtn = () => {
    if (window.scrollY > 300) scrollBtn.classList.add('show');
    else scrollBtn.classList.remove('show');
  };
  window.addEventListener('scroll', debounce(toggleScrollBtn, 100));
  scrollBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // ———————————————————————————————————————————
  // 5) Footer Date & Time
  // ———————————————————————————————————————————
  const dtEl = document.getElementById('currentDateTime');
  const yrEl = document.getElementById('year');
  function updateDateTime() {
    const now = new Date();
    dtEl && (dtEl.textContent = now.toLocaleString());
    yrEl && (yrEl.textContent = now.getFullYear());
  }
  updateDateTime();
  setInterval(updateDateTime, 60_000);

  // ———————————————————————————————————————————
  // 6) Email/Contact Widget Logic
  // ———————————————————————————————————————————
// Contact Form Toggle Logic with accessibility fix using `inert`
const contactToggle = document.getElementById('email-toggle');
const contactWidget = document.getElementById('contact-widget');
const contactClose  = document.getElementById('contact-close');
const contactForm   = document.getElementById('contact-form');
const cfStatus      = document.getElementById('cf-status');

function openContact() {
  contactWidget.removeAttribute('inert');               // Re-enable access
  contactWidget.style.display = 'flex';
  contactWidget.classList.add('open');
  contactToggle.setAttribute('aria-expanded', 'true');
  setTimeout(() => {
    const firstInput = contactWidget.querySelector('input');
    firstInput?.focus(); // Optional focus handling
  }, 100);
}

function closeContact() {
  if (document.activeElement && contactWidget.contains(document.activeElement)) {
    document.activeElement.blur();                      // Prevent focused elements inside hidden widget
  }

  contactWidget.setAttribute('inert', '');              // Block interactions/accessibility
  contactWidget.style.display = 'none';
  contactWidget.classList.remove('open');
  contactToggle.setAttribute('aria-expanded', 'false');
}

// Toggle open/close
contactToggle.addEventListener('click', () => {
  const isOpen = contactWidget.style.display === 'flex';
  isOpen ? closeContact() : openContact();
});
contactClose.addEventListener('click', closeContact);

// Submit using EmailJS
contactForm.addEventListener('submit', async e => {
  e.preventDefault();
  cfStatus.textContent = 'Sending…';
  try {
    await emailjs.send('service_saxdc56','template_ezh0s0d',{
      user_name:  contactForm.user_name.value,
      user_email: contactForm.user_email.value,
      subject:    contactForm.subject.value,
      message:    contactForm.message.value,
    });
    cfStatus.textContent = '✅ Sent!';
    contactForm.reset();
  } catch(err) {
    cfStatus.textContent = '❌ Failed to send.';
    console.error(err);
  } finally {
    setTimeout(() => cfStatus.textContent = '', 5000);
  }
 });
});
document.addEventListener('DOMContentLoaded', () => {
  // ———————————————————————————————————————————
  // 1) Debounce Utility
  // ———————————————————————————————————————————
  function debounce(fn, wait = 50) {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => fn.apply(this, args), wait);
    };
  }

  // ———————————————————————————————————————————
  // 2) Mobile Menu Toggle
  // ———————————————————————————————————————————
  const menu = document.getElementById('menu');
  const toggle = document.querySelector('.mobile-toggle');
  if (toggle && menu) {
    toggle.addEventListener('click', e => {
      e.stopPropagation();
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      menu.classList.toggle('active');
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
  // 3) Chatbot Setup
  // ———————————————————————————————————————————
  const chatContainer = document.getElementById('chatbot-container');
  const chatToggle    = document.getElementById('chatbot-toggle');
  const chatWidget    = document.getElementById('chatbot-widget');
  const chatClose     = document.getElementById('chatbot-close');
  const chatMessages  = document.getElementById('chatbot-messages');
  const chatForm      = document.getElementById('chatbot-form');
  const chatInput     = document.getElementById('chatbot-input');
  const chatSend      = document.getElementById('chatbot-send');

  // 👇 Use this in production (deployed site):
  const API_BASE = 'https://my-portfolio-uene.onrender.com';

  // ✅ Optional for local testing
  // const API_BASE = 'http://127.0.0.1:8000';

  let sse = null;

  function appendMessage(sender, text = '') {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
  }

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
    if (sse) {
      sse.close();
      sse = null;
    }
    chatSend.disabled = false;
  }

  chatToggle?.addEventListener('click', () =>
    chatContainer.classList.contains('expanded') ? closeChat() : openChat()
  );
  chatClose?.addEventListener('click', closeChat);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && chatContainer.classList.contains('expanded')) {
      closeChat();
    }
  });

  chatForm?.addEventListener('submit', e => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;
    openChat();
    appendMessage('user', text);
    chatInput.value = '';
    chatSend.disabled = true;

    const botDiv = appendMessage('bot');

    // ✅ Close old SSE connection before opening new
    if (sse) {
      sse.close();
      sse = null;
    }

    try {
      sse = new EventSource(`${API_BASE}/chat/stream?message=${encodeURIComponent(text)}`);

      sse.onmessage = evt => {
        try {
          const { reply } = JSON.parse(evt.data);
          botDiv.textContent += reply;
          chatMessages.scrollTop = chatMessages.scrollHeight;
        } catch (err) {
          console.error('Parse error:', err);
        }
      };

      sse.addEventListener('end', () => {
        chatSend.disabled = false;
        if (sse) {
          sse.close();
          sse = null;
        }
      });

      sse.onerror = () => {
        botDiv.textContent += '\n⚠️ [Connection error]';
        chatSend.disabled = false;
        if (sse) {
          sse.close();
          sse = null;
        }
      };
    } catch (err) {
      console.error('Connection error:', err);
      botDiv.textContent = '❌ Unable to connect to server.';
      chatSend.disabled = false;
    }
  });

  window.addEventListener('beforeunload', () => {
    if (sse) sse.close();
  });

  // ———————————————————————————————————————————
  // 4) Scroll To Top
  // ———————————————————————————————————————————
  const scrollBtn = document.getElementById('scroll-up');
  const toggleScrollBtn = () => {
    if (window.scrollY > 300) scrollBtn.classList.add('show');
    else scrollBtn.classList.remove('show');
  };
  window.addEventListener('scroll', debounce(toggleScrollBtn, 100));
  scrollBtn?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // ———————————————————————————————————————————
  // 5) Date & Time in Footer
  // ———————————————————————————————————————————
  const dtEl = document.getElementById('currentDateTime');
  const yrEl = document.getElementById('year');

  function updateDateTime() {
    const now = new Date();
    const formatted = now.toLocaleString('en-IN', {
      weekday: 'short',         // e.g., Mon
      year: 'numeric',          // e.g., 2025
      month: 'short',           // e.g., Jul
      day: '2-digit',           // e.g., 02
      hour: '2-digit',          // e.g., 10 PM
      minute: '2-digit',
      second: '2-digit',
      hour12: true              // 12-hour format
    });

    if (dtEl) dtEl.textContent = formatted;
    if (yrEl) yrEl.textContent = now.getFullYear();
  }

  // Initial update
  updateDateTime();

  // Update every second
  setInterval(updateDateTime, 1000);

  // ———————————————————————————————————————————
  // 6) Email Contact Widget (Optional)
  // ———————————————————————————————————————————
  const contactToggle = document.getElementById('email-toggle');
  const contactWidget = document.getElementById('contact-widget');
  const contactClose = document.getElementById('contact-close');
  const contactForm = document.getElementById('contact-form');
  const cfStatus = document.getElementById('cf-status');

  function openContact() {
    contactWidget.removeAttribute('inert');
    contactWidget.style.display = 'flex';
    contactWidget.classList.add('open');
    contactToggle.setAttribute('aria-expanded', 'true');
    setTimeout(() => contactWidget.querySelector('input')?.focus(), 100);
  }

  function closeContact() {
    document.activeElement?.blur();
    contactWidget.setAttribute('inert', '');
    contactWidget.style.display = 'none';
    contactWidget.classList.remove('open');
    contactToggle.setAttribute('aria-expanded', 'false');
  }

  contactToggle?.addEventListener('click', () => {
    const isOpen = contactWidget.style.display === 'flex';
    isOpen ? closeContact() : openContact();
  });

  contactClose?.addEventListener('click', closeContact);

  contactForm?.addEventListener('submit', async e => {
    e.preventDefault();
    cfStatus.textContent = 'Sending...';
    try {
      await emailjs.send('service_saxdc56', 'template_ezh0s0d', {
        user_name: contactForm.user_name.value,
        user_email: contactForm.user_email.value,
        subject: contactForm.subject.value,
        message: contactForm.message.value,
      });
      cfStatus.textContent = '✅ Sent!';
      contactForm.reset();
    } catch (err) {
      cfStatus.textContent = '❌ Failed to send.';
      console.error(err);
    } finally {
      setTimeout(() => cfStatus.textContent = '', 5000);
    }
  });
});

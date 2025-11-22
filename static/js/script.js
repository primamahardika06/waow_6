// Global utility functions
function showNotification(message, type = 'success') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.custom-notification');
    existingNotifications.forEach(notif => notif.remove());
    
    const notification = document.createElement('div');
    notification.className = `custom-notification alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Common error handler
function handleApiError(error, context) {
    console.error(`Error in ${context}:`, error);
    const errorMessage = error.message || 'Terjadi kesalahan, silakan coba lagi';
    showNotification(`Error: ${errorMessage}`, 'error');
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('id-ID', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Debounce function untuk performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Function to change login text
function changeLoginText(newTitle, newSubtitle) {
  document.getElementById("welcomeText").textContent = newTitle;
  document.getElementById("subtitleText").textContent = newSubtitle;
}

// Function to show error message
function showError(message) {
  const errorDiv = document.getElementById("errorMessage");
  errorDiv.textContent = message;
  errorDiv.style.display = "block";

  // Change text to indicate error
  changeLoginText("Login Failed!", "Please check your credentials");

  // Hide error after 5 seconds
  setTimeout(() => {
    errorDiv.style.display = "none";
    changeLoginText("Welcome to Prima Shop!", "Please Login Your Account");
  }, 5000);
}

// Form validation
function validateForm() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!email || !password) {
    showError("Please fill in all fields");
    return false;
  }

  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    showError("Please enter a valid email address");
    return false;
  }

  return true;
}

// Example: Change text based on time of day
function updateGreetingBasedOnTime() {
  const hour = new Date().getHours();
  let greeting = "Welcome to Prima Shop!";

  if (hour < 12) {
    greeting = "Good Morning! Welcome to Prima Shop";
  } else if (hour < 18) {
    greeting = "Good Afternoon! Welcome to Prima Shop";
  } else {
    greeting = "Good Evening! Welcome to Prima Shop";
  }

  document.getElementById("welcomeText").textContent = greeting;
}

async function handleLogin(event) {
  event.preventDefault(); // supaya tdk reload

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const result = await response.json();

  if (result.success) {
    window.location.href = result.redirect;
  } else {
    showError(result.message);
  }
}

// Call when page loads
document.addEventListener("DOMContentLoaded", function () {
  updateGreetingBasedOnTime();

  // Add event listeners for real-time validation
  document.getElementById("email").addEventListener("input", function () {
    // Clear error when user starts typing
    document.getElementById("errorMessage").style.display = "none";
  });

  document.getElementById("password").addEventListener("input", function () {
    // Clear error when user starts typing
    document.getElementById("errorMessage").style.display = "none";
  });
});

// Example: Change text on button hover (optional)
document
  .querySelector('button[type="submit"]')
  .addEventListener("mouseover", function () {
    document.getElementById("subtitleText").textContent =
      "Click to sign in to your account";
  });

document
  .querySelector('button[type="submit"]')
  .addEventListener("mouseout", function () {
    document.getElementById("subtitleText").textContent =
      "Please Login Your Account";
  });

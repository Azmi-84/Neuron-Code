// Utility functions
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// Application state
const state = {
  currentUser: null,
  currentRole: null,
  books: [],
  issuedBooks: [],
};

// API base URL - adjust this to your Flask API when it's running
const API_BASE_URL = "http://localhost:5000/api";

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
  // Navigation and UI controls
  initializeNavigation();
  initializeAuthTabs();
  initializeDashboardOptions();
  initializeNotifications();

  // Form submissions
  initializeAuthForms();
  initializeDashboardForms();
});

// Navigation and UI Controls
function initializeNavigation() {
  // Role selection
  $("#student-btn").addEventListener("click", () => showAuthSection("student"));
  $("#librarian-btn").addEventListener("click", () =>
    showAuthSection("librarian")
  );

  // Back buttons
  $("#back-from-student").addEventListener("click", showRoleSelection);
  $("#back-from-librarian").addEventListener("click", showRoleSelection);

  // Logout buttons
  $("#student-logout").addEventListener("click", handleLogout);
  $("#librarian-logout").addEventListener("click", handleLogout);
}

function showAuthSection(role) {
  hideAllSections();
  $(`#${role}-auth`).classList.remove("hidden");
  state.currentRole = role;
}

function showRoleSelection() {
  hideAllSections();
  $("#role-selection").classList.remove("hidden");
}

function showDashboard(role, user) {
  hideAllSections();
  $(`#${role}-dashboard`).classList.remove("hidden");
  $(`#${role}-name`).textContent = user.username;
  state.currentUser = user;
  state.currentRole = role;
}

function hideAllSections() {
  const sections = $$(".section");
  sections.forEach((section) => section.classList.add("hidden"));
}

function initializeAuthTabs() {
  // Initialize auth tabs for both student and librarian
  ["student", "librarian"].forEach((role) => {
    const tabs = $$(`#${role}-auth .auth-tab`);
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        // Deactivate all tabs
        tabs.forEach((t) => t.classList.remove("active"));
        // Hide all forms
        $$(`#${role}-auth .auth-form`).forEach((form) =>
          form.classList.add("hidden")
        );

        // Activate current tab and show corresponding form
        tab.classList.add("active");
        const targetForm = tab.getAttribute("data-target");
        $(`#${targetForm}`).classList.remove("hidden");
      });
    });
  });
}

function initializeDashboardOptions() {
  // Student dashboard options
  $$("#student-dashboard .dashboard-option").forEach((option) => {
    option.addEventListener("click", () =>
      handleDashboardAction("student", option.getAttribute("data-action"))
    );
  });

  // Librarian dashboard options
  $$("#librarian-dashboard .dashboard-option").forEach((option) => {
    option.addEventListener("click", () =>
      handleDashboardAction("librarian", option.getAttribute("data-action"))
    );
  });
}

function handleDashboardAction(role, action) {
  // Clear previous content
  const contentElement = $(`#${role}-content`);
  contentElement.innerHTML = "";

  // Handle different actions
  switch (action) {
    case "view-catalog":
      loadCatalog(contentElement);
      break;
    case "search-book":
      loadSearchInterface(contentElement);
      break;
    case "issue-book":
      loadIssueBookInterface(contentElement);
      break;
    case "return-book":
      loadReturnBookInterface(contentElement);
      break;
    case "add-book":
      loadAddBookInterface(contentElement);
      break;
    case "view-issued":
      loadIssuedBooksInterface(contentElement);
      break;
    case "remove-book":
      loadRemoveBookInterface(contentElement);
      break;
    case "update-book":
      loadUpdateBookInterface(contentElement);
      break;
    case "reset-password":
      loadResetPasswordInterface(contentElement, role);
      break;
  }
}

// Form Initializations
function initializeAuthForms() {
  // Student login form
  $("#student-login-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = $("#student-email").value;
    const password = $("#student-password").value;

    loginUser("student", email, password);
  });

  // Student registration form
  $("#student-register-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const studentId = $("#new-student-id").value;
    const username = $("#new-student-username").value;
    const email = $("#new-student-email").value;
    const password = $("#new-student-password").value;
    const confirmPassword = $("#confirm-student-password").value;
    const phone = $("#new-student-phone").value;

    if (password !== confirmPassword) {
      showNotification("Passwords do not match", "error");
      return;
    }

    registerUser("student", {
      student_id: studentId,
      username,
      email,
      password,
      phone_num: phone,
    });
  });

  // Student password reset form
  $("#student-reset-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = $("#reset-student-email").value;
    const currentPassword = $("#reset-student-current").value;
    const newPassword = $("#reset-student-new").value;
    const confirmPassword = $("#reset-student-confirm").value;

    if (newPassword !== confirmPassword) {
      showNotification("Passwords do not match", "error");
      return;
    }

    resetPassword("student", email, currentPassword, newPassword);
  });

  // Librarian login form
  $("#librarian-login-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = $("#librarian-email").value;
    const password = $("#librarian-password").value;

    loginUser("librarian", email, password);
  });

  // Librarian registration form
  $("#librarian-register-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const librarianId = $("#new-librarian-id").value;
    const username = $("#new-librarian-username").value;
    const email = $("#new-librarian-email").value;
    const password = $("#new-librarian-password").value;
    const confirmPassword = $("#confirm-librarian-password").value;
    const phone = $("#new-librarian-phone").value;

    if (password !== confirmPassword) {
      showNotification("Passwords do not match", "error");
      return;
    }

    registerUser("librarian", {
      librarian_id: librarianId,
      username,
      email,
      password,
      phone_num: phone,
    });
  });

  // Librarian password reset form
  $("#librarian-reset-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = $("#reset-librarian-email").value;
    const currentPassword = $("#reset-librarian-current").value;
    const newPassword = $("#reset-librarian-new").value;
    const confirmPassword = $("#reset-librarian-confirm").value;

    if (newPassword !== confirmPassword) {
      showNotification("Passwords do not match", "error");
      return;
    }

    resetPassword("librarian", email, currentPassword, newPassword);
  });
}

function initializeDashboardForms() {
  // These will be initialized when the dashboard actions are triggered
  // as they use templates that are only added to the DOM when needed
}

// Dashboard Content Loaders
function loadCatalog(container) {
  // Clone the catalog template
  const template = $("#catalog-template").content.cloneNode(true);
  container.appendChild(template);

  // Fetch books
  fetchBooks().then((books) => {
    const booksContainer = container.querySelector(".books-container");
    displayBooks(books, booksContainer);
  });
}

function loadSearchInterface(container) {
  // Clone the search template
  const template = $("#search-book-template").content.cloneNode(true);
  container.appendChild(template);

  // Initialize search button
  container.querySelector("#search-button").addEventListener("click", () => {
    const query = container.querySelector("#search-query").value;
    if (!query) {
      showNotification("Please enter a search term", "error");
      return;
    }

    searchBooks(query).then((books) => {
      const resultsContainer = container.querySelector(".search-results");
      resultsContainer.innerHTML = "";

      if (books.length === 0) {
        resultsContainer.innerHTML =
          "<p>No books found matching your search.</p>";
        return;
      }

      displayBooks(books, resultsContainer);
    });
  });
}

function loadIssueBookInterface(container) {
  // Clone the issue book template
  const template = $("#issue-book-template").content.cloneNode(true);
  container.appendChild(template);

  // Initialize form submission
  container
    .querySelector("#issue-book-form")
    .addEventListener("submit", (e) => {
      e.preventDefault();

      const bookId = container.querySelector("#issue-book-id").value;
      const studentId = container.querySelector("#issue-student-id").value;
      const username = container.querySelector("#issue-username").value;
      const returnDate = container.querySelector("#issue-return-date").value;

      issueBook(bookId, studentId, username, returnDate);
    });
}

function loadReturnBookInterface(container) {
  // Clone the return book template
  const template = $("#return-book-template").content.cloneNode(true);
  container.appendChild(template);

  // Initialize form submission
  container
    .querySelector("#return-book-form")
    .addEventListener("submit", (e) => {
      e.preventDefault();

      const bookId = container.querySelector("#return-book-id").value;
      const studentId = container.querySelector("#return-student-id").value;
      const username = container.querySelector("#return-username").value;

      returnBook(bookId, studentId, username);
    });

  // Load issued books for this student if in student role
  if (state.currentRole === "student" && state.currentUser) {
    fetchIssuedBooks(state.currentUser.student_id).then((issuedBooks) => {
      const issuedBooksContainer = container.querySelector(
        ".issued-books-container"
      );
      issuedBooksContainer.innerHTML = "";

      if (issuedBooks.length === 0) {
        issuedBooksContainer.innerHTML = "<p>You have no books issued.</p>";
        return;
      }

      issuedBooks.forEach((book) => {
        const bookElement = document.createElement("div");
        bookElement.className = "issued-book-item";
        bookElement.innerHTML = `
                    <h4>${book.book_name}</h4>
                    <p><strong>Book ID:</strong> ${book.book_id}</p>
                    <p><strong>Issue Date:</strong> ${book.issue_date}</p>
                    <p><strong>Return Date:</strong> ${book.return_date}</p>
                `;
        issuedBooksContainer.appendChild(bookElement);
      });
    });
  }
}

function loadAddBookInterface(container) {
  // Clone the add book template
  const template = $("#add-book-template").content.cloneNode(true);
  container.appendChild(template);

  // Initialize form submission
  container.querySelector("#add-book-form").addEventListener("submit", (e) => {
    e.preventDefault();

    const bookName = container.querySelector("#add-book-name").value;
    const author = container.querySelector("#add-author").value;
    const price = container.querySelector("#add-price").value;
    const quantity = container.querySelector("#add-quantity").value;
    const publication = container.querySelector("#add-publication").value;
    const pubDate = container.querySelector("#add-pub-date").value;

    addBook({
      book_name: bookName,
      author,
      price,
      quantity,
      publication,
      publication_date: pubDate,
    });
  });
}

function loadRemoveBookInterface(container) {
  // Clone the remove book template
  const template = $("#remove-book-template").content.cloneNode(true);
  container.appendChild(template);

  // Initialize form submission
  container
    .querySelector("#remove-book-form")
    .addEventListener("submit", (e) => {
      e.preventDefault();

      const bookId = container.querySelector("#remove-book-id").value;
      removeBook(bookId);
    });
}

function loadUpdateBookInterface(container) {
  // Clone the update book template
  const template = $("#update-book-template").content.cloneNode(true);
  container.appendChild(template);

  // Load book details when requested
  container
    .querySelector("#load-book-details")
    .addEventListener("click", () => {
      const bookId = container.querySelector("#update-book-id").value;

      if (!bookId) {
        showNotification("Please enter a book ID", "error");
        return;
      }

      fetchBookDetails(bookId).then((book) => {
        if (!book) {
          showNotification("Book not found", "error");
          return;
        }

        // Display the update form with book details
        const updateDetails = container.querySelector("#update-book-details");
        updateDetails.classList.remove("hidden");

        container.querySelector("#update-book-name").value =
          book.book_name || "";
        container.querySelector("#update-author").value = book.author || "";
        container.querySelector("#update-price").value = book.price || "";
        container.querySelector("#update-quantity").value = book.quantity || "";
        container.querySelector("#update-publication").value =
          book.publication || "";
        container.querySelector("#update-pub-date").value =
          book.publication_date || "";
      });
    });

  // Initialize form submission
  container
    .querySelector("#update-book-form")
    .addEventListener("submit", (e) => {
      e.preventDefault();

      const bookId = container.querySelector("#update-book-id").value;
      const updateDetails = container.querySelector("#update-book-details");

      if (updateDetails.classList.contains("hidden")) {
        showNotification("Please load book details first", "error");
        return;
      }

      const updates = {};

      const bookName = container.querySelector("#update-book-name").value;
      if (bookName) updates.book_name = bookName;

      const author = container.querySelector("#update-author").value;
      if (author) updates.author = author;

      const price = container.querySelector("#update-price").value;
      if (price) updates.price = price;

      const quantity = container.querySelector("#update-quantity").value;
      if (quantity) updates.quantity = quantity;

      const publication = container.querySelector("#update-publication").value;
      if (publication) updates.publication = publication;

      const pubDate = container.querySelector("#update-pub-date").value;
      if (pubDate) updates.publication_date = pubDate;

      updateBook(bookId, updates);
    });
}

function loadIssuedBooksInterface(container) {
  // Clone the view issued template
  const template = $("#view-issued-template").content.cloneNode(true);
  container.appendChild(template);

  // Fetch all issued books
  fetchAllIssuedBooks().then((issuedBooks) => {
    const issuedBooksContainer = container.querySelector(".issued-books-list");

    if (issuedBooks.length === 0) {
      issuedBooksContainer.innerHTML = "<p>No books are currently issued.</p>";
      return;
    }

    issuedBooks.forEach((book) => {
      const bookElement = document.createElement("div");
      bookElement.className = "issued-book-item";
      bookElement.innerHTML = `
                <h4>${book.book_name}</h4>
                <p><strong>Book ID:</strong> ${book.book_id}</p>
                <div class="issued-to">
                    <h5>Issued To:</h5>
                    <ul>
                        ${book.issued_to
                          .map(
                            (issue) => `
                            <li>
                                <p><strong>Student ID:</strong> ${issue.student_id}</p>
                                <p><strong>Username:</strong> ${issue.username}</p>
                                <p><strong>Issue Date:</strong> ${issue.issue_date}</p>
                                <p><strong>Return Date:</strong> ${issue.return_date}</p>
                            </li>
                        `
                          )
                          .join("")}
                    </ul>
                </div>
            `;
      issuedBooksContainer.appendChild(bookElement);
    });
  });
}

function loadResetPasswordInterface(container, role) {
  // Create form dynamically
  const formContainer = document.createElement("div");
  formContainer.className = "reset-password-container";
  formContainer.innerHTML = `
        <h3>Reset Password</h3>
        <form id="dashboard-reset-form">
            <div class="form-group">
                <label for="dashboard-reset-current">Current Password:</label>
                <input type="password" id="dashboard-reset-current" required>
            </div>
            <div class="form-group">
                <label for="dashboard-reset-new">New Password:</label>
                <input type="password" id="dashboard-reset-new" required>
                <small>Must be at least 8 characters with uppercase, lowercase, digit, and special character</small>
            </div>
            <div class="form-group">
                <label for="dashboard-reset-confirm">Confirm New Password:</label>
                <input type="password" id="dashboard-reset-confirm" required>
            </div>
            <button type="submit" class="submit-btn">Reset Password</button>
        </form>
    `;

  container.appendChild(formContainer);

  // Initialize form
  container
    .querySelector("#dashboard-reset-form")
    .addEventListener("submit", (e) => {
      e.preventDefault();

      const currentPassword = container.querySelector(
        "#dashboard-reset-current"
      ).value;
      const newPassword = container.querySelector("#dashboard-reset-new").value;
      const confirmPassword = container.querySelector(
        "#dashboard-reset-confirm"
      ).value;

      if (newPassword !== confirmPassword) {
        showNotification("Passwords do not match", "error");
        return;
      }

      resetPassword(
        role,
        state.currentUser.email,
        currentPassword,
        newPassword
      );
    });
}

// Utility for displaying books
function displayBooks(books, container) {
  container.innerHTML = "";

  books.forEach((book) => {
    const template = $("#book-card-template").content.cloneNode(true);

    // Fill in book details
    template.querySelector(".book-title").textContent = book.book_name;
    template.querySelector(".book-id").textContent = book.book_id;
    template.querySelector(".book-author").textContent = book.author;
    template.querySelector(".book-price").textContent = book.price;
    template.querySelector(".book-quantity").textContent = book.quantity;
    template.querySelector(".book-publication").textContent = book.publication;
    template.querySelector(".book-pub-date").textContent =
      book.publication_date;

    // Add action buttons based on role
    const actionsContainer = template.querySelector(".book-actions");

    if (state.currentRole === "student") {
      // Only add issue button if quantity > 0
      if (book.quantity > 0) {
        const issueBtn = document.createElement("button");
        issueBtn.className = "issue-btn";
        issueBtn.textContent = "Issue Book";
        issueBtn.addEventListener("click", () => {
          handleDashboardAction("student", "issue-book");
          // Pre-fill the issue form with this book
          setTimeout(() => {
            $("#issue-book-id").value = book.book_id;
            $("#issue-student-id").value = state.currentUser.student_id;
            $("#issue-username").value = state.currentUser.username;
          }, 100);
        });
        actionsContainer.appendChild(issueBtn);
      }
    } else if (state.currentRole === "librarian") {
      // Add update button
      const updateBtn = document.createElement("button");
      updateBtn.className = "update-btn";
      updateBtn.textContent = "Update";
      updateBtn.addEventListener("click", () => {
        handleDashboardAction("librarian", "update-book");
        // Pre-fill the update form with this book
        setTimeout(() => {
          $("#update-book-id").value = book.book_id;
          // Trigger the load details button
          $("#load-book-details").click();
        }, 100);
      });
      actionsContainer.appendChild(updateBtn);

      // Add remove button
      const removeBtn = document.createElement("button");
      removeBtn.className = "remove-btn";
      removeBtn.textContent = "Remove";
      removeBtn.addEventListener("click", () => {
        if (confirm(`Are you sure you want to remove "${book.book_name}"?`)) {
          removeBook(book.book_id);
        }
      });
      actionsContainer.appendChild(removeBtn);
    }

    container.appendChild(template);
  });
}

// API Calls
async function fetchBooks() {
  try {
    const response = await fetch(`${API_BASE_URL}/books`);
    if (!response.ok) throw new Error("Failed to fetch books");

    const data = await response.json();
    state.books = data.books;
    return data.books;
  } catch (error) {
    console.error("Error fetching books:", error);
    showNotification("Failed to load books", "error");
    return [];
  }
}

async function searchBooks(query) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/books/search?query=${encodeURIComponent(query)}`
    );
    if (!response.ok) throw new Error("Search failed");

    const data = await response.json();
    return data.books;
  } catch (error) {
    console.error("Error searching books:", error);
    showNotification("Search failed", "error");
    return [];
  }
}

async function fetchBookDetails(bookId) {
  try {
    const response = await fetch(`${API_BASE_URL}/books/${bookId}`);
    if (!response.ok) {
      if (response.status === 404) return null;
      throw new Error("Failed to fetch book details");
    }

    const data = await response.json();
    return data.book;
  } catch (error) {
    console.error("Error fetching book details:", error);
    showNotification("Failed to load book details", "error");
    return null;
  }
}

async function loginUser(role, email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/${role}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        showNotification("Invalid credentials", "error");
        return;
      }
      throw new Error("Login failed");
    }

    const data = await response.json();
    showDashboard(role, data.user);
    showNotification("Login successful", "success");
  } catch (error) {
    console.error("Login error:", error);
    showNotification("Login failed", "error");
  }
}

async function registerUser(role, userData) {
  try {
    const response = await fetch(`${API_BASE_URL}/${role}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      // Check for specific errors
      const data = await response.json();
      showNotification(data.message || "Registration failed", "error");
      return;
    }

    const data = await response.json();
    showNotification("Registration successful. You can now login.", "success");

    // Switch to login tab
    $(`#${role}-auth .auth-tab[data-target="${role}-login"]`).click();
  } catch (error) {
    console.error("Registration error:", error);
    showNotification("Registration failed", "error");
  }
}

async function resetPassword(role, email, currentPassword, newPassword) {
  try {
    const response = await fetch(`${API_BASE_URL}/${role}/reset-password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        current_password: currentPassword,
        new_password: newPassword,
      }),
    });

    if (!response.ok) {
      const data = await response.json();
      showNotification(data.message || "Password reset failed", "error");
      return;
    }

    showNotification("Password reset successful", "success");

    // If reset was done from the dashboard, log out
    if (state.currentUser) {
      handleLogout();
    }
  } catch (error) {
    console.error("Password reset error:", error);
    showNotification("Password reset failed", "error");
  }
}

async function addBook(bookData) {
  try {
    const response = await fetch(`${API_BASE_URL}/books`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(bookData),
    });

    if (!response.ok) throw new Error("Failed to add book");

    const data = await response.json();
    showNotification(
      `Book added successfully. Book ID: ${data.book_id}`,
      "success"
    );

    // Reset the form
    $("#add-book-form").reset();
  } catch (error) {
    console.error("Error adding book:", error);
    showNotification("Failed to add book", "error");
  }
}

async function updateBook(bookId, updates) {
  try {
    const response = await fetch(`${API_BASE_URL}/books/${bookId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    });

    if (!response.ok) throw new Error("Failed to update book");

    showNotification("Book updated successfully", "success");

    // Reload book catalog if visible
    if (
      $(".catalog-container") &&
      !$(".catalog-container").classList.contains("hidden")
    ) {
      handleDashboardAction(state.currentRole, "view-catalog");
    }
  } catch (error) {
    console.error("Error updating book:", error);
    showNotification("Failed to update book", "error");
  }
}

async function removeBook(bookId) {
  try {
    const response = await fetch(`${API_BASE_URL}/books/${bookId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      const data = await response.json();
      showNotification(data.message || "Failed to remove book", "error");
      return;
    }

    showNotification("Book removed successfully", "success");

    // Reload book catalog if visible
    if (
      $(".catalog-container") &&
      !$(".catalog-container").classList.contains("hidden")
    ) {
      handleDashboardAction(state.currentRole, "view-catalog");
    }
  } catch (error) {
    console.error("Error removing book:", error);
    showNotification("Failed to remove book", "error");
  }
}

async function issueBook(bookId, studentId, username, returnDate) {
  try {
    const response = await fetch(`${API_BASE_URL}/books/${bookId}/issue`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: studentId,
        username,
        return_date: returnDate,
      }),
    });

    if (!response.ok) {
      const data = await response.json();
      showNotification(data.message || "Failed to issue book", "error");
      return;
    }

    showNotification("Book issued successfully", "success");

    // Reset the form
    $("#issue-book-form").reset();
  } catch (error) {
    console.error("Error issuing book:", error);
    showNotification("Failed to issue book", "error");
  }
}

async function returnBook(bookId, studentId, username) {
  try {
    const response = await fetch(`${API_BASE_URL}/books/${bookId}/return`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: studentId,
        username,
      }),
    });

    if (!response.ok) {
      const data = await response.json();
      showNotification(data.message || "Failed to return book", "error");
      return;
    }

    showNotification("Book returned successfully", "success");

    // Reset the form and reload the interface to update issued books list
    $("#return-book-form").reset();
    if (state.currentRole === "student") {
      handleDashboardAction("student", "return-book");
    }
  } catch (error) {
    console.error("Error returning book:", error);
    showNotification("Failed to return book", "error");
  }
}

async function fetchIssuedBooks(studentId) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/students/${studentId}/issued-books`
    );
    if (!response.ok) throw new Error("Failed to fetch issued books");

    const data = await response.json();
    return data.books;
  } catch (error) {
    console.error("Error fetching issued books:", error);
    showNotification("Failed to load issued books", "error");
    return [];
  }
}

async function fetchAllIssuedBooks() {
  try {
    const response = await fetch(`${API_BASE_URL}/books/issued`);
    if (!response.ok) throw new Error("Failed to fetch issued books");

    const data = await response.json();
    return data.books;
  } catch (error) {
    console.error("Error fetching all issued books:", error);
    showNotification("Failed to load issued books", "error");
    return [];
  }
}

function handleLogout() {
  state.currentUser = null;
  showRoleSelection();
  showNotification("Logged out successfully", "success");
}

// Notification System
function initializeNotifications() {
  const notification = $("#notification");
  $(".notification-close").addEventListener("click", () => {
    notification.style.display = "none";
  });
}

function showNotification(message, type = "info") {
  const notification = $("#notification");
  $(".notification-message").textContent = message;

  // Set type
  notification.className = "notification";
  notification.classList.add(type);

  // Show notification
  notification.style.display = "block";

  // Auto-hide after 3 seconds
  setTimeout(() => {
    notification.style.display = "none";
  }, 3000);
}
// Generated by Copilot

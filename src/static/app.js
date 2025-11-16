document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const categoryFilter = document.getElementById("category-filter");
  const difficultyFilter = document.getElementById("difficulty-filter");
  const clearFiltersBtn = document.getElementById("clear-filters");

  // Function to fetch activities from API with optional filters
  async function fetchActivities(filters = {}) {
    try {
      // Build query string from filters
      const params = new URLSearchParams();
      if (filters.category) params.append("category", filters.category);
      if (filters.difficulty) params.append("difficulty", filters.difficulty);
      
      const queryString = params.toString();
      const url = queryString ? `/activities?${queryString}` : "/activities";
      
      const response = await fetch(url);
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      
      // Clear activity select options (keep the first default option)
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      if (Object.keys(activities).length === 0) {
        activitiesList.innerHTML = "<p>No activities found matching your filters.</p>";
        return;
      }

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft =
          details.max_participants - details.participants.length;

        // Get category color class
        const categoryClass = getCategoryClass(details.category);
        
        // Create tags HTML
        const tagsHTML = details.tags && details.tags.length > 0
          ? `<div class="tags">
              ${details.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>`
          : '';

        // Create participants HTML with delete icons instead of bullet points
        const participantsHTML =
          details.participants.length > 0
            ? `<div class="participants-section">
              <h5>Participants:</h5>
              <ul class="participants-list">
                ${details.participants
                  .map(
                    (email) =>
                      `<li><span class="participant-email">${email}</span><button class="delete-btn" data-activity="${name}" data-email="${email}">❌</button></li>`
                  )
                  .join("")}
              </ul>
            </div>`
            : `<p><em>No participants yet</em></p>`;

        activityCard.innerHTML = `
          <div class="activity-header">
            <h4>${name}</h4>
            <span class="category-badge ${categoryClass}">${details.category}</span>
          </div>
          <p>${details.description}</p>
          ${tagsHTML}
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Difficulty:</strong> ${details.difficulty_level}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants-container">
            ${participantsHTML}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });

      // Add event listeners to delete buttons
      document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", handleUnregister);
      });
    } catch (error) {
      activitiesList.innerHTML =
        "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }
  
  // Helper function to get category color class
  function getCategoryClass(category) {
    const categoryMap = {
      'Technical': 'category-technical',
      'Sports': 'category-sports',
      'Arts': 'category-arts',
      'Academic': 'category-academic'
    };
    return categoryMap[category] || 'category-default';
  }
  
  // Handle filter changes
  function handleFilterChange() {
    const filters = {
      category: categoryFilter.value,
      difficulty: difficultyFilter.value
    };
    fetchActivities(filters);
  }
  
  // Add event listeners for filters
  categoryFilter.addEventListener("change", handleFilterChange);
  difficultyFilter.addEventListener("change", handleFilterChange);
  
  clearFiltersBtn.addEventListener("click", () => {
    categoryFilter.value = "";
    difficultyFilter.value = "";
    fetchActivities();
  });

  // Handle unregister functionality
  async function handleUnregister(event) {
    const button = event.target;
    const activity = button.getAttribute("data-activity");
    const email = button.getAttribute("data-email");

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(
          activity
        )}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";

        // Refresh activities list to show updated participants
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to unregister. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error unregistering:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(
          activity
        )}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();

        // Refresh activities list to show updated participants
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});

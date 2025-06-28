// AI Journal Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card, .feature-card, .step-card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(card => {
        observer.observe(card);
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                showAlert('Please fill in all required fields.', 'danger');
            }
        });
    });

    // Character counter for textareas
    const contentTextarea = document.getElementById('content');
    if (contentTextarea) {
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.id = 'char-counter';
        contentTextarea.parentNode.appendChild(counter);

        function updateCounter() {
            const count = contentTextarea.value.length;
            const wordCount = contentTextarea.value.trim().split(/\s+/).filter(word => word.length > 0).length;
            counter.textContent = `${count} characters, ${wordCount} words`;
        }

        contentTextarea.addEventListener('input', updateCounter);
        updateCounter();
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Enhanced search functionality
    const searchInput = document.getElementById('q');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Auto-submit search after 1 second of no typing
                if (this.value.length >= 3 || this.value.length === 0) {
                    this.form.submit();
                }
            }, 1000);
        });
    }

    // Sentiment score visualization
    const sentimentBars = document.querySelectorAll('.progress-bar');
    sentimentBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-text');
            navigator.clipboard.writeText(textToCopy).then(() => {
                showAlert('Copied to clipboard!', 'success');
            }).catch(() => {
                showAlert('Failed to copy to clipboard.', 'danger');
            });
        });
    });

    // Dark mode toggle (if implemented)
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDark);
            this.innerHTML = isDark ? 
                '<i class="fas fa-sun me-2"></i>Light Mode' : 
                '<i class="fas fa-moon me-2"></i>Dark Mode';
        });

        // Load saved preference
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode === 'true') {
            document.body.classList.add('dark-mode');
            darkModeToggle.innerHTML = '<i class="fas fa-sun me-2"></i>Light Mode';
        }
    }

    // Entry preview functionality
    const previewButtons = document.querySelectorAll('.preview-btn');
    previewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const entryId = this.getAttribute('data-entry-id');
            // Show preview modal or expand entry
            showEntryPreview(entryId);
        });
    });

    // Tag filtering
    const tagFilters = document.querySelectorAll('.tag-filter');
    tagFilters.forEach(tag => {
        tag.addEventListener('click', function() {
            const tagName = this.getAttribute('data-tag');
            filterEntriesByTag(tagName);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + N for new entry
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            window.location.href = '/new_entry';
        }
        
        // Ctrl/Cmd + S for save (if on entry form)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            const saveButton = document.querySelector('button[type="submit"]');
            if (saveButton && saveButton.closest('form')) {
                e.preventDefault();
                saveButton.click();
            }
        }
    });

    // Auto-save functionality for long entries
    const autoSaveTextarea = document.getElementById('content');
    if (autoSaveTextarea) {
        let autoSaveTimeout;
        autoSaveTextarea.addEventListener('input', function() {
            clearTimeout(autoSaveTimeout);
            autoSaveTimeout = setTimeout(() => {
                // Auto-save draft after 30 seconds of no typing
                saveDraft();
            }, 30000);
        });
    }

    // Initialize any additional components
    initializeComponents();
});

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function showEntryPreview(entryId) {
    // Implementation for entry preview modal
    console.log('Showing preview for entry:', entryId);
}

function filterEntriesByTag(tagName) {
    // Implementation for tag filtering
    console.log('Filtering by tag:', tagName);
}

function saveDraft() {
    // Implementation for auto-saving drafts
    console.log('Auto-saving draft...');
}

function initializeComponents() {
    // Initialize any additional components or libraries
    console.log('Initializing components...');
}

// Export functions for use in other scripts
window.AIJournal = {
    showAlert,
    showEntryPreview,
    filterEntriesByTag,
    saveDraft
}; 
/**
 * MafadzaTechSolutions Main JavaScript
 */

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Format currency inputs
    document.querySelectorAll('.currency-input').forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });
    
    // Confirm delete actions
    document.querySelectorAll('.confirm-delete').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
});

// Function to update repair status
function updateRepairStatus(repairId, status) {
    fetch(`/admin/api/repair/${repairId}/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error updating status: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating status');
    });
}

// Function to generate report
function generateReport(format = 'pdf') {
    const month = document.getElementById('reportMonth').value;
    const year = document.getElementById('reportYear').value;
    
    window.open(`/admin/reports/export?format=${format}&month=${month}&year=${year}`, '_blank');
}

// Form validation
function validateBookingForm() {
    const requiredFields = document.querySelectorAll('form [required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    if (!isValid) {
        alert('Please fill in all required fields marked with *.');
    }
    
    return isValid;
}

// Track repair status check
function checkRepairStatus(trackingId) {
    if (!trackingId) {
        alert('Please enter a tracking ID');
        return;
    }
    
    window.location.href = `/track-repair?tracking_id=${trackingId}`;
}
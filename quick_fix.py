#!/usr/bin/env python3
"""
Quick fix for common template issues
"""

import os

print("Fixing template issues...")

# Ensure all template files exist
templates = {
    'app/templates/book_repair.html': '''{% extends "base.html" %}

{% block title %}Book Repair - {{ super() }}{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="card shadow border-0">
                <div class="card-header bg-primary text-white">
                    <h3 class="mb-0"><i class="fas fa-calendar-plus"></i> Book Device Repair</h3>
                </div>
                <div class="card-body">
                    <form method="POST" action="{{ url_for('main.book_repair') }}">
                        <div class="mb-3">
                            <label class="form-label">Name</label>
                            <input type="text" class="form-control" name="name" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Phone</label>
                            <input type="tel" class="form-control" name="phone" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Device Type</label>
                            <select class="form-select" name="device_type" required>
                                <option value="">Select</option>
                                <option value="Laptop">Laptop</option>
                                <option value="Phone">Phone</option>
                                <option value="Tablet">Tablet</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Brand</label>
                            <input type="text" class="form-control" name="brand" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Problem Description</label>
                            <textarea class="form-control" name="problem" rows="4" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
    
    'app/templates/admin/login.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <h1 class="text-center mb-4">Admin Login</h1>
                <div class="card">
                    <div class="card-body">
                        {% with messages = get_flashed_messages(with_categories=true) %}
                            {% if messages %}
                                {% for category, message in messages %}
                                    <div class="alert alert-{{ category }}">{{ message }}</div>
                                {% endfor %}
                            {% endif %}
                        {% endwith %}
                        
                        <form method="POST" action="{{ url_for('admin.login') }}">
                            <div class="mb-3">
                                <label class="form-label">Username</label>
                                <input type="text" name="username" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Login</button>
                        </form>
                        
                        <div class="mt-3 text-center">
                            <small class="text-muted">
                                Default: admin / Admin123!
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
}

# Create directories if they don't exist
for path in templates.keys():
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

# Create template files
for path, content in templates.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created/updated: {path}")

print("\n✓ Fix applied!")
print("\nNow try running: python run.py")
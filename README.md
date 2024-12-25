# Obiadomat

A web application built with Django that streamlines group food ordering and management processes.

## About The Project

Obiadomat is a comprehensive solution for organizing group food orders. It simplifies the entire process from selecting a restaurant to managing payments between participants. The platform allows users to create meal sessions, invite participants, and manage orders efficiently.

### Core Features

- User authentication system with email verification
- Role-based access control (Admin, Manager, Customer)
- Restaurant and menu management
- Meal session creation and management
- Group invitation system with email notifications
- Order management with editing capabilities
- Detailed order summaries and reports

### Advanced Features

#### Enhanced Permission System
- Custom view-level permissions
- Advanced session management permissions
- Flexible role assignment for session managers

#### Automated Processes
- Celery integration for background tasks
- Automated session status updates
- Email notification system for:
  - Account activation
  - Password reset
  - Session invitations
  - Order confirmations

## Technical Implementation

- Framework: Django
- Task Queue: Celery
- Email Integration: Custom email notification system
- Authentication: Extended Django authentication with email verification
- Database: Custom models for restaurants, sessions, and orders

## Deployment

The application is deployed on Render and can be accessed at: https://app-yxxf.onrender.com
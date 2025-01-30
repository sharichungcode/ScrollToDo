# ScrollToDo
[Deployed Website](https://scroll-to-do-fc37dc092ebb.herokuapp.com/)

## Overview
ScrollToDo is a task management tool designed to help users efficiently create, organize, and prioritize their tasks. Unlike traditional task managers, ScrollToDo introduces an intuitive prioritization system that mimics the casual and engaging experience of scrolling through social media. It provides two main prioritization modes: linear ranking and matrix-based sorting, allowing users to prioritize tasks effortlessly from any device, including mobile.

## UX Design Process

### **Link to User Stories in GitHub Projects:**
- [GitHub Projects Board](https://github.com/users/sharichungcode/projects/3/)

### **Wireframes:**
- [Attach or link to wireframes](#)
- Design ensures high contrast and accessibility.
- Layout optimizations for mobile-first usability and smooth prioritization interactions.

### **Design Rationale:**
- Aesthetic: Minimalistic and user-friendly UI.
- Prioritization Modes: Drag-and-drop for intuitive ranking.
- Accessibility: WCAG-compliant color contrasts, screen-reader support, and large tap targets for mobile users.

### **Reasoning for Final Changes:**
- Optimized drag interactions for mobile users.
- Added a button-based alternative for users with motor impairments.
- Improved matrix prioritization visualization for better clarity.

## Key Features
- **Task Creation & Management:** Create, edit, delete tasks easily.
- **Prioritization:**
  - Linear Ranking (drag-and-drop or button-based ranking).
  - Matrix Prioritization (drag tasks into quadrants).
- **Progress Tracking:** Checkboxes for completed tasks and an analytics dashboard.
- **Inclusivity Notes:**
  - Designed with accessibility-first principles, ensuring all users can engage effectively.

## Deployment
- **Platform:** Heroku
- **Deployment Steps:**
  1. Clone the repository.
  2. Install dependencies and set up the database.
  3. Deploy using platform-specific CI/CD pipeline.
- **Verification & Validation:**
  - Ensuring feature parity between development and production.
  - Accessibility audits using Lighthouse.
- **Security Measures:**
  - Environment variables for sensitive data.
  - Secure authentication and authorization.
  - Debug mode disabled in production.

## AI Implementation and Orchestration

### **Use Cases & Reflections:**
- **Code Creation:** AI-assisted generation for rapid prototyping, ensuring alignment with accessibility standards.
- **Debugging:** AI-aided troubleshooting for efficiency and maintainability.
- **Performance & UX Optimization:** AI-driven suggestions implemented with minimal manual refinements.
- **Automated Testing:** AI-generated unit tests adjusted to enhance inclusivity and cover edge cases.

### **Overall Impact:**
- Faster development cycles due to AI-driven optimizations.
- Improved code quality with minimal manual intervention.
- Adjustments required to contextualize AI-generated outputs effectively.

## Testing Summary

### **Manual Testing:**
- **Devices & Browsers Tested:**
  - Chrome, Firefox, Safari, Edge
  - Mobile, tablet, and desktop responsiveness tested
  - Screen reader & keyboard navigation testing conducted
- **Features Tested:**
  - CRUD operations, prioritization, analytics, and authentication
- **Results:**
  - All features performed as expected with no accessibility issues found.

### **Automated Testing:**
- **Tools Used:** Django TestCase / Jest / Cypress
- **Features Covered:**
  - Task prioritization, user authentication, analytics tracking
- **Adjustments Made:**
  - Enhanced AI-generated test cases for accessibility compliance

## Future Enhancements
- Task import from external to-do apps (iOS Reminders, Google Tasks)
- Real-time collaboration (shared task lists, team prioritization)
- AI-powered task prioritization suggestions
- Calendar integration for task scheduling
- Voice input for hands-free task management
- Enhanced accessibility options (colorblind-friendly themes, text-to-speech support)

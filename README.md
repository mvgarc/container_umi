# Container UMI -- Logistics Document Management System

## Overview

Container UMI is a backend-focused web application developed to
digitalize and centralize the administrative management of **Bill of
Lading (BL)** and related documentation in import/export operations.

The system improves traceability, reduces operational risk, and enables
structured multi-user access to critical logistics documentation.

------------------------------------------------------------------------

## Business Problem

In logistics environments handling import/export operations, document
management is often:

-   Manual or fragmented
-   Lacking clear traceability
-   Reactive in expiration control
-   Without structured digital backup

This increases operational risk and reduces administrative efficiency.

------------------------------------------------------------------------

## Implemented Solution

The system provides:

-   Structured BL registration
-   Association of multiple documents per BL
-   Expiration date tracking
-   Secure digital file storage
-   Multi-user authenticated access
-   Centralized administrative control

------------------------------------------------------------------------

## Technical Architecture

### Technology Stack

-   **Backend:** Python + Django\
-   **WSGI Server:** Gunicorn\
-   **Reverse Proxy:** Nginx\
-   **Database:** PostgreSQL (SQLite for local development)\
-   **Infrastructure:** AWS Lightsail\
-   **Operating System:** Ubuntu Linux

### Deployment Architecture

Client → Nginx → Gunicorn → Django → PostgreSQL

This setup reflects a production-ready architecture following web
deployment best practices.

------------------------------------------------------------------------

## System Design

The project follows Django's MVT (Model-View-Template) pattern:

-   **Model:** Data layer and relational modeling\
-   **View:** Business logic\
-   **Template:** Presentation layer

Key design decisions:

-   Modular app structure\
-   Clear separation of responsibilities\
-   Use of ForeignKey relationships\
-   Structured file management using FileField

------------------------------------------------------------------------

## Database Modeling

Relational database design including:

-   One-to-many relationship (BL → Documents)
-   Referential integrity with ForeignKey constraints
-   Scalable schema prepared for migration to managed RDS if required

------------------------------------------------------------------------

## Authentication & Security

-   Django built-in authentication system
-   Multi-user session management
-   CSRF protection
-   Controlled file uploads
-   Reverse proxy configuration via Nginx
-   Isolated virtual environment
-   Production deployment on secure Linux server

Optional scalability improvements:

-   HTTPS via Let's Encrypt
-   Automated backups
-   Migration to AWS RDS
-   Enhanced role-based access control

------------------------------------------------------------------------

## Infrastructure

Deployed on:

-   **AWS Lightsail**
    -   Ubuntu instance
    -   1GB RAM
    -   2 vCPU
    -   40GB SSD

Configured manually with Nginx + Gunicorn for production stability.

------------------------------------------------------------------------

## Project Status

-   Production deployed
-   Multi-user operational
-   Designed for administrative logistics environments

------------------------------------------------------------------------

Backend-focused web application deployed in AWS production environment.

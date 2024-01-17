# F-Store

Welcome to the F-store repository, an advanced and dynamic online store for clothing and accessories. This project, "F-Store" integrates a range of modern web technologies and practices, offering a feature-rich platform for both users and administrators.

## Key Features

- **Dynamic Shopping Cart**: A standout feature of F-Store is its agile and dynamic cart system. For unauthenticated users, the cart data is saved in local storage, and upon authentication, it seamlessly transitions to server-side management using Django REST framework.
- **Comprehensive Admin Panel**: An extensive admin panel to manage products, orders, and user accounts effectively.
- **Responsive Design**: The application is designed to be responsive, ensuring a smooth user experience across various devices.
- **Enhanced User Experience**: Features like category filters, user profiles, and intuitive navigation enhance the overall user experience.
- **Stripe Payment Integration**: Fully configured Stripe payment system for secure and reliable transaction processing in a test mode (Card: 4242 4242 4242 4242, Date: any future date, CVC: any 3 digits).
- **Security and Permissions**: A strong focus on security and permissions to protect user data and interactions.
- **Email and Order Status Management**: Integration of Celery for email sending and order status updates.

## Technologies Used

### Frontend
- HTML, CSS, JavaScript
- Bootstrap for responsive design

### Backend
- Django and Django REST framework
- Django-allauth for authentication
- Django-environ for environment management
- Comprehensive use of Django messages

### Database
- PostgreSQL

### Others
- Celery for asynchronous tasks
- Unittests and CI/CD integration
- Digital Ocean for hosting
- Nginx and Gunicorn
- HTTPS for secure communication
- Custom domain (f-store.tech) and email setup (f-store@f-store.tech)

## Contributing

Anyone interested in contributing to the F-store project is welcome. Your contributions will help make this project even better.

## License

This project code is entirely or partly available for use without any restrictions.

## Live Application

Check out the live application here: [F-store](https://f-store.tech/)

[![Django CI](https://github.com/Serg-f/f_store/actions/workflows/django.yml/badge.svg)](https://github.com/Serg-f/f_store/actions/workflows/django.yml)

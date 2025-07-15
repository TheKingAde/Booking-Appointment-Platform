# BookingPro - Professional Booking & Appointment Platform

## 🚀 Project Overview

BookingPro is a modern, full-stack booking and appointment platform built with Flask and JavaScript. It features a clean, animated UI with a green/white/red color scheme, real-time booking management, and Telegram bot integration for instant notifications.

## ✨ Key Features

- **Modern UI Design**: Clean, animated interface with smooth CSS animations
- **Real-time Booking**: Instant appointment confirmation with availability checking
- **Telegram Integration**: Automatic booking notifications via Telegram Bot API
- **Admin Dashboard**: Intuitive calendar view for managing appointments
- **Mobile Responsive**: Optimized for all devices
- **Secure Authentication**: Admin access with session management
- **Database Integration**: SQLite database for storing bookings and services
- **RESTful API**: Clean API endpoints for booking operations

## 🎨 Design Features

- **Color Scheme**: Green (#2c8b2c) and white with red (#e74c3c) accents
- **CSS Animations**: Smooth transitions, hover effects, and loading animations
- **Interactive Elements**: Animated buttons, cards, and form elements
- **Responsive Layout**: Mobile-first design with fluid grids
- **Modern Typography**: Poppins font for excellent readability

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.0, SQLAlchemy 2.0.36, Python 3.13
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), FontAwesome icons
- **Database**: SQLite (easily configurable for other databases)
- **Notifications**: Telegram Bot API integration
- **Development**: Virtual environment, modular code structure

## 📦 Installation & Setup

### Prerequisites
- Python 3.13 or higher
- Virtual environment support
- Internet connection for dependencies

### 1. Clone the Repository
```bash
git clone <repository-url>
cd booking-platform
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🔧 Configuration

### Telegram Bot Setup
Update the following variables in `app.py`:
```python
TG_API_URL = "https://api.telegram.org"
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
```

### Admin Authentication
Default admin credentials:
- Username: `admin`
- Password: `admin123`

**⚠️ Important**: Change these credentials in production!

## 🚀 Usage Guide

### For Customers

1. **Browse Services**: Visit the homepage to view available services
2. **Book Appointment**: 
   - Click "Book Now" or navigate to the booking page
   - Select service, date, and time
   - Fill in personal details
   - Confirm booking
3. **Confirmation**: Receive instant confirmation on screen

### For Administrators

1. **Login**: Access `/admin/login` with admin credentials
2. **Dashboard**: View booking statistics and calendar
3. **Manage Bookings**: Edit, reschedule, or cancel appointments
4. **Notifications**: Receive Telegram notifications for all booking activities

## 📱 Pages & Features

### Homepage (`/`)
- Hero section with animated elements
- Feature highlights with icons
- Statistics display
- Call-to-action sections

### Services Page (`/services`)
- Service cards with pricing and descriptions
- Hover animations and transitions
- Direct booking links

### Booking Page (`/booking`)
- Multi-step booking process
- Interactive calendar
- Real-time availability checking
- Form validation and user feedback

### Admin Dashboard (`/admin/dashboard`)
- Booking statistics and metrics
- Calendar view with appointment indicators
- Booking management interface
- Quick actions for common tasks

## 🔄 API Endpoints

### Public Endpoints
- `GET /` - Homepage
- `GET /services` - Services page
- `GET /booking` - Booking page
- `GET /api/services` - Get all services
- `GET /api/available-slots` - Get available time slots
- `POST /api/bookings` - Create new booking

### Admin Endpoints (Authentication Required)
- `GET /admin/dashboard` - Admin dashboard
- `PUT /api/bookings/<id>` - Update booking
- `DELETE /api/bookings/<id>` - Delete booking

## 🗄️ Database Schema

### Services Table
- `id`: Primary key
- `name`: Service name
- `duration`: Duration in minutes
- `price`: Service price
- `description`: Service description

### Bookings Table
- `id`: Primary key
- `client_name`: Customer name
- `client_email`: Customer email
- `client_phone`: Customer phone
- `service_id`: Foreign key to services
- `appointment_date`: Appointment date and time
- `status`: Booking status (confirmed, cancelled)
- `notes`: Additional notes
- `created_at`: Creation timestamp

## 🔔 Telegram Integration

The system sends automated notifications for:
- New booking confirmations
- Booking updates and changes
- Booking cancellations

### Message Format
```
🎉 New Booking Confirmed!

👤 Client: John Doe
📧 Email: john@example.com
📞 Phone: +1234567890
💼 Service: Hair Cut & Style
📅 Date: 2025-01-15
🕐 Time: 14:30
💰 Price: $45.00
📝 Notes: First time customer

Booking ID: #123
```

## 🎯 Sample Services

The application comes with pre-configured services:
- **Hair Cut & Style** - 60 minutes - $45.00
- **Manicure & Pedicure** - 90 minutes - $35.00
- **Facial Treatment** - 75 minutes - $65.00
- **Massage Therapy** - 60 minutes - $80.00
- **Consultation** - 30 minutes - $25.00

## 📱 Mobile Optimization

- Responsive navigation with mobile menu
- Touch-friendly interface elements
- Optimized form layouts for mobile
- Fast loading with minimal dependencies
- Progressive enhancement approach

## 🔧 Customization

### Styling
- Modify CSS variables in `templates/base.html`
- Update color scheme in `:root` selector
- Customize animations and transitions

### Services
- Add/modify services in the database
- Update service icons and descriptions
- Adjust pricing and duration

### Branding
- Update logo and company name
- Customize email templates
- Modify notification messages

## 🚀 Deployment

### Production Considerations
1. **Security**: Change default admin credentials
2. **Database**: Use PostgreSQL or MySQL for production
3. **Environment Variables**: Store sensitive data in environment variables
4. **SSL**: Enable HTTPS with SSL certificates
5. **Scaling**: Consider using Gunicorn or uWSGI
6. **Monitoring**: Implement logging and error tracking

### Environment Variables
```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="your-database-url"
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

## 📊 Performance Features

- **Efficient Database Queries**: Optimized SQLAlchemy queries
- **Client-side Caching**: Smart caching of service data
- **Lazy Loading**: Images and content loaded as needed
- **Minified Assets**: CSS and JavaScript optimization
- **Database Indexing**: Proper indexing for faster queries

## 🛡️ Security Features

- **SQL Injection Protection**: SQLAlchemy ORM protection
- **XSS Protection**: Input sanitization and validation
- **CSRF Protection**: Session-based authentication
- **Input Validation**: Server-side and client-side validation
- **Secure Headers**: Security headers implementation

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check database file permissions
   - Verify SQLite installation

2. **Telegram Notifications Not Working**
   - Verify bot token and chat ID
   - Check internet connectivity
   - Ensure bot is activated

3. **CSS Not Loading**
   - Clear browser cache
   - Check static file serving
   - Verify CSS file paths

4. **Python Version Compatibility**
   - Ensure Python 3.13 or higher
   - Check virtual environment activation

## 📝 License

This project is created for educational and portfolio purposes. Feel free to modify and use according to your needs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues, questions, or contributions:
- Create an issue in the repository
- Check existing documentation
- Review the troubleshooting section

## 🎉 Acknowledgments

- Flask community for the excellent framework
- Font Awesome for beautiful icons
- Google Fonts for typography
- Telegram Bot API for notification system

---

**Built with ❤️ using Flask, modern CSS, and JavaScript**

*This project demonstrates full-stack development skills, modern UI/UX design, and real-world application features suitable for professional portfolios.*
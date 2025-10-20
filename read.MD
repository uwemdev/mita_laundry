# Mita Laundry - Laundry Management Platform

![Mita Laundry](https://img.shields.io/badge/Mita-Laundry-blue) ![Python](https://img.shields.io/badge/Python-3.6%2B-blue) ![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey) ![SQLite](https://img.shields.io/badge/SQLite-Database-green)

A comprehensive laundry management platform built with Flask and SQLite that allows users to place laundry orders, track their progress, and manage services efficiently.

## 🌟 Features

### User Features
- **User Authentication**: Secure signup and login system
- **Order Management**: Create laundry orders with washing, ironing, or both services
- **Real-time Tracking**: Track order status using unique order numbers
- **Service Selection**: Choose between washing, ironing, or wash & iron services
- **Pickup Options**: Select store pickup or home delivery
- **Order History**: View all past and current orders
- **Responsive Design**: Mobile-friendly interface

### Admin Features
- **Dashboard**: Comprehensive overview with statistics
- **Order Management**: View and update order statuses
- **User Management**: Monitor registered users
- **Real-time Updates**: Instant status changes for orders

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Session-based with password hashing
- **Icons**: Font Awesome

## 📋 Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd mita_laundry

# Or simply download and extract the project files
```

### 2. Install Dependencies
```bash
pip install flask
```

### 3. Initialize the Database
```bash
python3 app.py
```
The application will automatically:
- Create the SQLite database (`laundry.db`)
- Initialize all required tables
- Create an admin user

### 4. Access the Application
```bash
python3 app.py
```
Visit `http://localhost:5000` in your browser.

## 👤 Default Admin Account

- **Email**: `admin@mitalaundry.com`
- **Password**: `admin123`

## 📁 Project Structure

```
mita_laundry/
├── app.py                 # Main Flask application
├── laundry.db            # SQLite database (auto-generated)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── login.html        # User login
│   ├── signup.html       # User registration
│   ├── dashboard.html    # User dashboard
│   ├── create_order.html # Order creation form
│   ├── track_order.html  # Order tracking
│   ├── order_details.html # Order details page
│   ├── admin_dashboard.html # Admin dashboard
│   ├── admin_orders.html   # Admin order management
│   └── admin_users.html    # Admin user management
└── static/              # Static assets
    ├── css/
    │   └── style.css    # Custom styles
    └── js/
        └── script.js    # JavaScript functions
```

## 💰 Pricing Structure

### Washing Services
- T-Shirts: ₹20
- Shorts: ₹25
- Pants: ₹30
- Caps: ₹15
- Socks: ₹10
- Towels: ₹35
- Bedsheets: ₹50

### Ironing Services
- T-Shirts: ₹15
- Shorts: ₹20
- Pants: ₹25
- Caps: ₹10
- Socks: ₹8
- Towels: ₹20
- Bedsheets: ₹30

### Combined Services (Wash & Iron)
- Combined pricing of both services

## 🎨 Design Features

- **Color Scheme**: Beautiful dark and light blue theme
- **Responsive Layout**: Works on all device sizes
- **Modern UI**: Clean and professional interface
- **Interactive Elements**: Hover effects and smooth transitions
- **Progress Indicators**: Visual order status tracking

## 🔄 Order Status Flow

1. **Pending** → Order created and awaiting processing
2. **In Progress** → Order being processed
3. **Completed** → Order ready for pickup/delivery

## 📊 Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `password` - Hashed password
- `phone` - Contact number
- `address` - Delivery address
- `created_at` - Account creation timestamp
- `is_admin` - Admin privileges flag

### Orders Table
- `id` - Primary key
- `order_number` - Unique order identifier
- `user_id` - Foreign key to users table
- `service_type` - washing/ironing/both
- `status` - pending/in_progress/completed
- `pickup_option` - pickup/delivery
- `total_items` - Total number of items
- `total_price` - Order total cost
- Individual item counts (tshirts, shorts, pants, etc.)
- Timestamps for creation, updates, and completion

## 🛡️ Security Features

- Password hashing using SHA-256
- Session-based authentication
- SQL injection prevention through parameterized queries
- Admin route protection
- Input validation and sanitization

## 🔧 Customization

### Modifying Prices
Edit the `PRICING` dictionary in `app.py`:

```python
PRICING = {
    'washing': {
        'tshirts': 25,  # Change price here
        # ... other items
    },
    # ... other services
}
```

### Adding New Services
1. Update the service type options in forms
2. Modify pricing structure
3. Update order processing logic

### Styling Changes
Edit `static/css/style.css` to modify colors, layouts, and design elements.

## 🐛 Troubleshooting

### Common Issues

1. **Database Table Errors**
   - Delete `laundry.db` and restart the application
   - Run `python3 app.py` to recreate the database

2. **Port Already in Use**
   ```bash
   # Kill the process using port 5000
   sudo lsof -t -i tcp:5000 | xargs kill -9
   ```

3. **Module Not Found Errors**
   ```bash
   pip install flask
   ```

## 📈 Future Enhancements

- [ ] Email notifications
- [ ] Payment integration
- [ ] SMS alerts
- [ ] Advanced reporting
- [ ] Multi-language support
- [ ] Image upload for special instructions
- [ ] Loyalty program
- [ ] Mobile app

## 👥 User Roles

### Customer
- Register and login
- Place laundry orders
- Track order status
- View order history
- Choose pickup/delivery options

### Administrator
- Monitor all orders
- Update order statuses
- Manage user accounts
- View business analytics
- Access admin dashboard

## 📞 Support

For support or questions:
- Email: uwemdev@hotmail.com
- Phone: +234 (811) 057-2387

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**Mita Laundry** - Making laundry management simple and efficient! 🧺✨
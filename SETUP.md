# Database Setup Guide

## Prerequisites

1. **PostgreSQL installed** on your machine
   - Download from: https://www.postgresql.org/download/
   - Remember your postgres password during installation

## Step 1: Install PostgreSQL

1. Download and install PostgreSQL from https://www.postgresql.org/download/
2. During installation, set a password for the `postgres` user
3. Remember the port (default: 5432)

## Step 2: Create Database

Open PostgreSQL command line (psql) or use pgAdmin:

```sql
-- Create database
CREATE DATABASE civic_services;
```

## Step 3: Run SQL Scripts

```bash
# Navigate to project directory
cd "C:\Desktop\Github Projects\Civic Services and DataBase Management System"

# Run schema creation script
psql -U postgres -d civic_services -f create.sql

# Run seed data script
psql -U postgres -d civic_services -f insert.sql
```

Or in pgAdmin SQL Editor:
1. Open `create.sql` and execute
2. Open `insert.sql` and execute

## Step 4: Update .env File

Edit the `.env` file with your credentials:

```env
DB_USERNAME=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=civic_services
ADMIN_PASSWORD=meow@1234
```

## Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Run the Application

```bash
python Server.py
```

Access at: http://localhost:5173

## Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | (use admin login) | meow@1234 |
| Citizen | sunita_sharma | motherpass1 |
| Employee | amit_admin | password123 |
| Monitor | Preetham | Preetham123@ |

## Troubleshooting

### Connection Error
- Ensure PostgreSQL service is running
- Check if port 5432 is correct
- Verify username and password in `.env`

### Table Already Exists
- The `create.sql` script drops tables first, so this should not happen
- If it does, manually drop tables or create a fresh database

### Permission Denied
- Make sure your PostgreSQL user has privileges on `civic_services` database

# Civic Services & Database Management System

A comprehensive full-stack web application for managing civic services at the Panchayat (village council) level, built with Flask and PostgreSQL.

### Live Server: [https://civic-services-and-database-management.onrender.com](https://civic-services-and-database-management.onrender.com)

---

## Project Metrics

| Metric | Value |
|--------|-------|
| REST API Endpoints | **38** |
| Database Tables | **12** |
| Database Constraints | **23** (12 Foreign Keys + 11 CHECK) |
| User Roles | **4** (Admin, Employee, Citizen, Monitor) |
| HTML Templates | **22** |
| JavaScript Functions | **90** |
| Frontend-Backend Integrations | **35** |

---

## Key Achievements

- Designed a **normalized PostgreSQL schema** with **12 tables** and **23 constraints** ensuring data integrity
- Built **38 RESTful API endpoints** serving **4 user roles** with conditional routing
- Developed **90 JavaScript functions** across **22 HTML templates** for dynamic frontend interactions
- Integrated **35 fetch() API calls** for seamless client-server communication
- Implemented **role-based access control** with admin-protected routes
- Created **real-time census analytics** with demographic breakdowns, income brackets, and yearly trends

---

## Features

- **Role-Based Access Control**: Admin, Employee, Citizen, and Monitor roles with different permissions
- **Citizen Management**: Add, update, and delete citizen records with household management
- **Welfare Schemes**: Create schemes, apply for schemes, and track application status
- **Agricultural Records**: Track farmland ownership and cultivation records
- **Service Requests**: Submit and process certificate requests (Birth, Death, Income, Marriage, Caste)
- **Census Data**: Record life events and generate demographic reports
- **Vaccination Records**: Track vaccination history for citizens
- **Resource Management**: Manage and monitor civic assets and infrastructure

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask, Flask-SQLAlchemy |
| Database | PostgreSQL |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| ORM | SQLAlchemy with relationship mappings |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (22 HTML Pages)              │
│    90 JS Functions  │  35 API Calls  │  Role-Based UI   │
└───────────────────────────┬─────────────────────────────┘
                            │ REST API (38 Endpoints)
┌───────────────────────────▼─────────────────────────────┐
│              Backend (Flask Server)                      │
│    Authentication  │  Role Routing  │  CRUD Operations   │
└───────────────────────────┬─────────────────────────────┘
                            │ SQLAlchemy ORM
┌───────────────────────────▼─────────────────────────────┐
│         PostgreSQL Database (12 Tables, 23 Constraints)  │
│  Citizens │ Employees │ Schemes │ Census │ Vaccinations  │
└─────────────────────────────────────────────────────────┘
```

---

## Database Schema (12 Tables)

| Table | Description |
|-------|-------------|
| `citizens` | Core citizen records with personal details |
| `employee` | Employee roles within the Panchayat |
| `users` | User authentication and role management |
| `households` | Household information and property details |
| `welfarescheme` | Government welfare schemes |
| `schemeapplication` | Scheme application tracking |
| `agriculturalland` | Agricultural land records |
| `cultivationrecord` | Crop cultivation data |
| `servicerequests` | Certificate and service requests |
| `censusdata` | Life events (Birth, Death, Marriage, Divorce) |
| `vaccinations` | Vaccination records |
| `assets` | Civic infrastructure and assets |

---

## API Endpoints (38 Total)

### Authentication (1)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | User login with role-based response |

### Citizens (2)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/get-citizen` | Get citizen details |
| POST | `/update-citizen` | Update citizen profile |

### Welfare Schemes (4)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/schemes` | Schemes page |
| GET | `/schemes/getschemes` | Get all/applied schemes |
| GET | `/schemes/getpendingschemes` | Get pending approvals |
| POST | `/applyschemes` | Apply for schemes |

### Agricultural Records (4)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/agrirecords` | Agriculture page |
| GET | `/farmland` | Get farmland details |
| GET | `/cultivationrecords` | Get cultivation records |
| POST | `/addcultivation` | Add cultivation record |

### Service Requests (5)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/services` | Citizen requests page |
| GET | `/api/citizenrequests` | Get citizen's requests |
| POST | `/api/citizenrequests` | Submit new request |
| GET | `/api/servicerequests` | Get pending requests |
| PUT | `/api/servicerequests/<id>` | Update request status |

### Census (4)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/census` | Census data page |
| POST | `/api/census` | Add census record |
| GET | `/censusreport` | Census report page |
| GET | `/api/censusreport` | Get census analytics |

### Vaccinations (4)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vaccinations` | Vaccinations page |
| GET | `/api/vaccinations` | Get vaccination records |
| POST | `/api/vaccinations` | Add vaccination record |
| DELETE | `/api/vaccinations/<id>` | Delete vaccination record |

### Resources (4)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/resources` | Resources page |
| GET | `/api/resources` | Get all assets |
| POST | `/api/resources` | Add new asset |
| DELETE | `/api/resources/<id>` | Delete asset |

### Admin (7)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin` | Admin dashboard |
| POST | `/admin/add-citizen` | Add new citizen |
| POST | `/admin/delete-citizen` | Delete citizen |
| POST | `/admin/add-employee` | Add employee |
| GET/POST | `/admin/edit-employee` | Edit employee |
| POST | `/admin/remove-employee` | Remove employee |

---

## Project Structure

```
├── Server.py                 # Flask backend
├── create.sql                # Database schema
├── insert.sql                # Seed data
├── Home.html                 # Landing page
├── Home_admin.html           # Admin dashboard
├── templates/
│   ├── Home_citizen.html     # Citizen dashboard
│   ├── Home_employee.html    # Employee dashboard
│   └── Home_monitor.html     # Monitor dashboard
├── Profile_*.html            # Profile pages (3 roles)
├── Schemes_*.html            # Welfare scheme pages (3 roles)
├── Agri_*.html               # Agriculture pages (2 roles)
├── Services_*.html           # Service request pages (2 roles)
├── Census_*.html             # Census pages (3 views)
├── Vaccinations_*.html       # Vaccination pages (2 roles)
└── Resources_*.html          # Resource pages (2 roles)
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pavanjarpula/Civic-Services-and-DataBase-Management-System.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:
   - Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
   - Create database: `CREATE DATABASE civic_services;`
   - Run schema: `psql -U postgres -d civic_services -f create.sql`
   - Run seed data: `psql -U postgres -d civic_services -f insert.sql`

4. Create `.env` file with your credentials:
   ```env
   DB_USERNAME=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=civic_services
   ADMIN_PASSWORD=meow@1234
   ```

5. Run the application:
   ```bash
   python Server.py
   ```

6. Access the application at `http://localhost:5173`

---

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | - | `meow@1234` |
| Monitor | `Preetham` | `Preetham123@` |
| Employee | `amit_admin` | `password123` |
| Citizen | `sunita_sharma` | `motherpass1` |

---

## License

This project is for educational purposes.

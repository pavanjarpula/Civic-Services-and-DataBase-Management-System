from flask import Flask, jsonify, send_file, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import func, extract, case
from datetime import datetime, timedelta
import calendar
    
app = Flask(__name__)
password_admin = "meow@1234"

# PostgreSQL database configuration
DB_USERNAME = "22CS10015"
DB_PASSWORD = "22CS10015"
DB_HOST = "10.5.18.69"
DB_PORT = "5432"
DB_NAME = "22CS10015"

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database Models
class Citizen(db.Model):
    __tablename__ = 'citizens'
    citizenid = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    dateofbirth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    householdid = db.Column(db.Integer)
    contactnumber = db.Column(db.String(15))
    job = db.Column(db.String(50))
    educationalqualification = db.Column(db.String(50))
    fatherid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete='SET NULL'), nullable=True)
    motherid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete='SET NULL'), nullable=True)

class Employee(db.Model):
    __tablename__ = 'employee'
    employeeid = db.Column(db.Integer, primary_key=True)
    citizenid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete='CASCADE'), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    citizenid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete='SET NULL'), nullable=True)

class Scheme(db.Model):
    __tablename__ = 'welfarescheme'  # Table name in the database

    schemeid = db.Column(db.Integer, primary_key=True)
    # Scheme Details
    schemename = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    eligibilitycriteria = db.Column(db.String(200), nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    launchdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    department = db.Column(db.String(100), nullable=False)
    validtill = db.Column(db.DateTime, nullable=False)

class Schemeapp(db.Model):
    __tablename__ = 'schemeapplication'
    applicationid = db.Column(db.Integer, primary_key=True)
    citizenid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete='CASCADE'), nullable=False)
    schemeid = db.Column(db.Integer, db.ForeignKey('welfarescheme.schemeid', ondelete='CASCADE'), nullable=False)
    applicationdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=False)
    remarks = db.Column(db.Text)

class AgriculturalLand(db.Model):
    __tablename__ = 'agriculturalland'
    landid = db.Column(db.Integer, primary_key=True)
    citizenid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete='CASCADE'), nullable=False)
    area = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)

class CultivationRecord(db.Model):
    __tablename__ = 'cultivationrecord'
    cultivationid = db.Column(db.Integer, primary_key=True)
    landid = db.Column(db.Integer, db.ForeignKey('agriculturalland.landid', ondelete='CASCADE') , nullable=False)
    year = db.Column(db.Integer, nullable=False)
    citizenid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete='CASCADE'), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    croptype = db.Column(db.String(100), nullable=False)
    cultivatedarea = db.Column(db.Float, nullable=False)
    productionquantity = db.Column(db.Float)

class Asset(db.Model):
    __tablename__ = 'assets'
    assetid = db.Column(db.Integer, primary_key=True)  
    # assetid = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    installationdate = db.Column(db.Date, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    lastmaintenancedate = db.Column(db.Date)
    
class ServiceRequest(db.Model):
    __tablename__ = 'servicerequests'
    requestid = db.Column(db.Integer, primary_key=True)
    citizenid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete='CASCADE'), nullable=False)
    requesttype = db.Column(db.String(50), nullable=False)
    requestdate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    citizen = db.relationship("Citizen", backref="requests")

class CensusData(db.Model):
    __tablename__ = 'censusdata'
    censuseventid = db.Column(db.Integer, primary_key=True)
    citizenid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete='CASCADE'), nullable=False)
    eventtype = db.Column(db.String(20), nullable=False)
    eventdate = db.Column(db.Date, nullable=False)
    eventnotes = db.Column(db.Text)
    citizen = db.relationship('Citizen', backref=db.backref('census_records', cascade='all, delete'))
    __table_args__ = (
        db.CheckConstraint("eventtype IN ('Birth', 'Death', 'Marriage', 'Divorce')", name='eventtype_check'),
    )

class Households(db.Model):
    householdid = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    income = db.Column(db.Numeric(12,2), nullable=False)
    numberofmembers = db.Column(db.Integer, nullable=False)
    propertyvalue = db.Column(db.Numeric(12,2))

    __table_args__ = (
        db.CheckConstraint("income >= 0", name='income_check'),
        db.CheckConstraint("numberofmembers > 0", name='members_check'),
        db.CheckConstraint("propertyvalue >= 0", name='property_check'),
    )

class Vaccination(db.Model):
    __tablename__ = 'vaccinations'

    vaccinationid = db.Column(db.Integer, primary_key=True)
    citizenid = db.Column(db.Integer, db.ForeignKey('citizens.citizenid', ondelete="CASCADE"), nullable=False)
    vaccinetype = db.Column(db.String(255), nullable=False)
    dateadministered = db.Column(db.Date, nullable=False)

@app.route('/')
def login_page():
    return send_file("Home.html")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if not user or user.password != data['password']:
        return jsonify({'error': 'Invalid username or password'}), 401
    if user.role == 'Admin':
        return jsonify({'Admin': True, 'success': True,'password': password_admin})
    if user.role == 'Monitor':
        return jsonify({'id': user.userid, 'success': True,'Monitor':True})        
    return jsonify({'id': user.userid, 'success': True,})

@app.route('/home')
def home():
    userid_ = request.args.get('id', type=int)
    user = User.query.filter_by(userid = userid_).first()
    if user.role == 'Monitor':
        return render_template("Home_monitor.html",username=user.username)

    citizen = Citizen.query.filter_by(citizenid=user.citizenid).first()
    
    if not citizen:
        return "User not found", 404
    
    return render_template("Home_employee.html" if user.role == 'Employee' else "Home_citizen.html", username=citizen.fullname)

@app.route('/profile')
def profile():
    userid_ = request.args.get('id', type=int)
    user = User.query.filter_by(userid = userid_).first()
    if user.role == 'Monitor':
        return send_file("Profile_monitor.html")
    
    return send_file("Profile_employee.html" if user.role == 'Employee' else "Profile_citizen.html")

@app.route('/get-citizen')
def get_citizen():
    userid_ = request.args.get('id', type=int)
    user = User.query.filter_by(userid = userid_).first()
    if user.role == 'Monitor':
        response = {
            "username": user.username
        }
        return jsonify(response)
    
    citizen = Citizen.query.filter_by(citizenid=user.citizenid).first()
    employee = Employee.query.filter_by(citizenid=user.citizenid).first()
    
    if not citizen:
        return jsonify({"error": "Citizen not found"}), 404
    
    response = {
        "id": citizen.citizenid,
        "name": citizen.fullname,
        "dob": citizen.dateofbirth.strftime('%Y-%m-%d'),
        "gender": citizen.gender,
        "householdid": citizen.householdid,
        "phone": citizen.contactnumber,
        "job": citizen.job,
        "qualification": citizen.educationalqualification,
        "father_id": citizen.fatherid,
        "mother_id": citizen.motherid,
        "is_employee": bool(employee),
        "username": user.username,
        "employee_role": employee.role if employee else None
    }
    return jsonify(response)

@app.route('/update-citizen', methods=['POST'])
def update_citizen():
    data = request.json
    userid_ = data.get("id")
    if not userid_:
        return jsonify({"error": "User ID is required"}), 400
    user = User.query.filter_by(userid = userid_).first()
    if user.role == 'Monitor':
        if "password" in data and data["password"]:
            user.password = data["password"]
        if "username" in data and data["username"]:
            user.username = data["username"]
        try:
            db.session.commit()
            return jsonify({"success": "Profile updated successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    
    citizen = Citizen.query.filter_by(citizenid=user.citizenid).first()
    if not citizen:
        return jsonify({"error": "Citizen not found"}), 404
    
    if "password" in data and data["password"]:
        user.password = data["password"]
    if "username" in data and data["username"]:
        user.username = data["username"]
    if "job" in data and data["job"]:
        citizen.job = data["job"]
    if "qualification" in data and data["qualification"]:
        citizen.educationalqualification = data["qualification"]

    
    try:
        db.session.commit()
        return jsonify({"success": "Profile updated successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

#schemes
@app.route('/schemes')
def scheme():
    userid_ = request.args.get('id', type=int)
    user = User.query.filter_by(userid = userid_).first()
    if user.role == 'Monitor':
        return send_file("Schemes_monitor.html")

    return send_file("Schemes_employee.html" if user.role == 'Employee' else "Schemes_citizen.html")

@app.route('/schemes/getschemes')
def getscheme():
    userid_ = request.args.get('id', type=int)
    user = User.query.filter_by(userid = userid_).first()
    only_applied = request.args.get('onlyapplied', default="false").lower() == "true"
    schemes = []

    if user.role == 'Monitor':
        # Fetch all schemes and count the number of citizens participating (status=True)
        monitored_schemes = (
            db.session.query(Scheme.schemeid, Scheme.schemename, Scheme.description, db.func.count(Schemeapp.applicationid))
            .outerjoin(Schemeapp, (Scheme.schemeid == Schemeapp.schemeid) & (Schemeapp.status == True))
            .group_by(Scheme.schemeid)
            .all()
        )
        
        for schemeid, schemename, description, participant_count in monitored_schemes:
            schemes.append({
                "schemeid": schemeid,
                "SchemeName": schemename,
                "Description": description,
                "Participants": participant_count
            })
        return jsonify(schemes)
    
    if not userid_:
        return jsonify({"error": "User ID is required"}), 400

    if not only_applied:
        allschemes = Scheme.query.all()
        for scheme in allschemes:
            schemes.append({
                "schemeid": scheme.schemeid,
                "SchemeName": scheme.schemename,
                "Description": scheme.description,
                "EligibilityCriteria": scheme.eligibilitycriteria,
                "Benefits": scheme.benefits,
                "LaunchDate": scheme.launchdate.strftime('%Y-%m-%d'),
                "Department": scheme.department,
                "ValidTill": scheme.validtill.strftime('%Y-%m-%d'),
                "status": None  # Status is not relevant when fetching all schemes
            })
    else:
        # Fetch schemes along with their application status from Schemeapp
        applied_schemes = (
            db.session.query(Scheme, Schemeapp.remarks)
            .join(Schemeapp, Scheme.schemeid == Schemeapp.schemeid)
            .filter(Schemeapp.citizenid == user.citizenid)
            .all()
        )

        for scheme, status in applied_schemes:
            schemes.append({
                "schemeid": scheme.schemeid,
                "SchemeName": scheme.schemename,
                "Description": scheme.description,
                "EligibilityCriteria": scheme.eligibilitycriteria,
                "Benefits": scheme.benefits,
                "LaunchDate": scheme.launchdate.strftime('%Y-%m-%d'),
                "Department": scheme.department,
                "ValidTill": scheme.validtill.strftime('%Y-%m-%d'),
                "status": status  # Status from Schemeapp table
            })

    return jsonify(schemes)

@app.route('/schemes/getpendingschemes')
def getpendingscheme():
    schemes = []
    pending_schemes = (
            db.session.query(Scheme, Schemeapp.remarks,Schemeapp.citizenid,Schemeapp.applicationid)
            .join(Schemeapp, Scheme.schemeid == Schemeapp.schemeid)
            .filter(Schemeapp.status == False)
            .all()
        )
    for scheme,remarks, citizenid,applicationid in pending_schemes:
            schemes.append({
                "schemeid": scheme.schemeid,
                "applicationid": applicationid,
                "SchemeName": scheme.schemename,
                "Description": scheme.description,
                "EligibilityCriteria": scheme.eligibilitycriteria,
                "Benefits": scheme.benefits,
                "Department": scheme.department,
                "ValidTill": scheme.validtill.strftime('%Y-%m-%d'),
                "citizenid": citizenid,
                "remarks": remarks
            })
    return jsonify(schemes)
    

@app.route('/applyschemes', methods=['POST'])
def apply_schemes():
    data = request.json
    userid_ = request.args.get('id', type=int)
    user = User.query.filter_by(userid = userid_).first()
    is_user = request.args.get('user', default="false").lower() == "true"

    if not userid_:
        return jsonify({"error": "User ID is required"}), 400

    if not data or 'schemeids' not in data:
        return jsonify({"error": "Scheme IDs are required"}), 400

    scheme_ids = data["schemeids"]
    applied_schemes = []

    if is_user:  
        # Case when it's a citizen applying for schemes
        for schemeid in scheme_ids:
            existing_application = Schemeapp.query.filter_by(citizenid=user.citizenid, schemeid=schemeid).first()

            if existing_application:
                applied_schemes.append({"schemeid": schemeid, "message": "Already Applied"})
            else:
                new_application = Schemeapp(
                    citizenid=user.citizenid,
                    schemeid=schemeid,
                    remarks="Pending Approval"
                )
                db.session.add(new_application)
    else:
        # Case when it's an admin or non-user updating the scheme table
        for app in scheme_ids:
            applicationid = app["applicationid"]
            remarks = app["remarks"]
            status = app["status"]

            scheme_app = Schemeapp.query.filter_by(applicationid=applicationid).first()
            if scheme_app:
                scheme_app.remarks = remarks
                scheme_app.status = status
            else:
                applied_schemes.append({"applicationid": applicationid, "message": "Application Not Found"})

    try:
        db.session.commit()
        return jsonify({"success": applied_schemes})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
#Agri Records
@app.route('/agrirecords')
def agripage():
    userid_ = request.args.get('id', type=int)
    user = User.query.filter_by(userid = userid_).first()
    if user.role == 'Monitor':
        return send_file("Agri_monitor.html")

    return send_file("Agri_citizen.html")

@app.route('/farmland', methods=['GET'])
def get_farmlands():
    """Fetch all farmland owned by a user."""
    userid_ = request.args.get('userid', type=int)
    user = User.query.filter_by(userid = userid_).first()
    if user.role == 'Monitor':
        # Fetch citizen details and total farmland area
        users = db.session.query(
            Citizen.citizenid,
            Citizen.fullname.label("citizenname"),
            func.sum(AgriculturalLand.area).label("TotalFarmland")
        ).join(AgriculturalLand,Citizen.citizenid == AgriculturalLand.citizenid)\
         .group_by(Citizen.citizenid)

        return jsonify([{
            "citizenid": user.citizenid,
            "citizenname": user.citizenname,
            "TotalFarmland": user.TotalFarmland
        } for user in users])
      
    if not userid_:
        return jsonify({"error": "User ID is required"}), 400

    lands = AgriculturalLand.query.filter_by(citizenid=user.citizenid).all()
    return jsonify([{
        "landid": land.landid,
        "Area": land.area,
        "Address": land.address
    } for land in lands])

@app.route('/cultivationrecords', methods=['GET'])
def get_cultivation_records():
    """Fetch all cultivation records for the user's farmlands."""
    userid_ = request.args.get('userid', type=int)
    user = User.query.filter_by(userid = userid_).first()
    if user.role == 'Monitor':
        # Aggregate data grouped by year, season, and croptype
        results = db.session.query(
            CultivationRecord.year,
            CultivationRecord.season,
            CultivationRecord.croptype,
            func.sum(CultivationRecord.cultivatedarea).label("TotalCultivatedArea"),
            func.sum(CultivationRecord.productionquantity).label("TotalProductionQuantity")
        ).group_by(CultivationRecord.year, CultivationRecord.season, CultivationRecord.croptype).all()

        if not results:
            return jsonify({"error": "No cultivation records found"}), 404

        return jsonify([
            {
                "year": result.year,
                "season": result.season,
                "croptype": result.croptype,
                "TotalCultivatedArea": result.TotalCultivatedArea,
                "TotalProductionQuantity": result.TotalProductionQuantity
            }
            for result in results
        ])

    if not userid_:
        return jsonify({"error": "User ID is required"}), 400

    records = db.session.query(CultivationRecord).join(AgriculturalLand).filter(AgriculturalLand.citizenid == user.citizenid).all()
    return jsonify([{
        "cultivationid": record.cultivationid,
        "landid": record.landid,
        "year": record.year,
        "season": record.season,
        "croptype": record.croptype,
        "cultivatedarea": record.cultivatedarea,
        "productionquantity": record.productionquantity
    } for record in records])

@app.route('/addcultivation', methods=['POST'])
def add_cultivation():
    """Add a cultivation record."""
    data = request.json
    userid_ = data['citizenid']
    user = User.query.filter_by(userid = userid_).first()
    required_fields = ["landid", "year", "season", "croptype", "cultivatedarea", "productionquantity", "citizenid"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_record = CultivationRecord(
        landid=data['landid'],
        year=data['year'],
        season=data['season'],
        croptype=data['croptype'],
        cultivatedarea=data['cultivatedarea'],
        productionquantity=data['productionquantity'],
        citizenid=user.citizenid
    )

    db.session.add(new_record)
    db.session.commit()

    return jsonify({"message": "Cultivation record added successfully!"}), 201

# Employee - Resources

@app.route('/resources')
def resources_page():
    print("Entered")
    is_monitor = request.args.get('monitor', default="false").lower() == "true"
    if is_monitor:
        return send_file("Resources_monitor.html")
    
    return send_file('Resources_employee.html')

@app.route('/api/resources', methods=['GET'])
def get_resources():
    resources = Asset.query.all()
    return jsonify([{
        'id': resource.assetid,
        'type': resource.type,
        'location': resource.location,
        'installationdate': resource.installationdate.strftime('%Y-%m-%d'),
        'condition': resource.condition,
        'lastmaintenancedate': resource.lastmaintenancedate.strftime('%Y-%m-%d') if resource.lastmaintenancedate else 'N/A'
    } for resource in resources])

@app.route('/api/resources', methods=['POST'])
def add_resource():
    data = request.json
    new_resource = Asset(
        type=data['type'],
        location=data['location'],
        installationdate=datetime.strptime(data['installationdate'], '%Y-%m-%d'),
        condition=data['condition'],
        lastmaintenancedate=datetime.strptime(data['lastmaintenancedate'], '%Y-%m-%d') if data.get('lastmaintenancedate') else None
    )
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({'message': 'Resource added successfully'}), 201

@app.route('/api/resources/<int:assetid>', methods=['DELETE'])
def delete_resource(assetid):
    resource = Asset.query.get(assetid)
    if resource:
        db.session.delete(resource)
        db.session.commit()
        return jsonify({'message': 'Resource deleted successfully'}), 200
    return jsonify({'error': 'Resource not found'}), 404

#Citizen - Service Requests

@app.route('/services')
def citizenrequests_page():
    return send_file('Services_citizen.html')

@app.route('/api/citizenrequests', methods=['GET'])
def get_citizen_requests():
    """Fetch all service requests made by a specific citizen."""
    userid_ = request.args.get('citizenid', type=int)
    user = User.query.filter_by(userid = userid_).first()
    if not userid_:
        return jsonify({"error": "Citizen ID is required"}), 400

    requests = ServiceRequest.query.filter_by(citizenid=user.citizenid).order_by(ServiceRequest.requestdate.desc()).all()

    return jsonify([
        {
            'requestid': req.requestid,
            'requesttype': req.requesttype,
            'requestdate': req.requestdate.strftime('%Y-%m-%d'),
            'status': req.status
        }
        for req in requests
    ])

@app.route('/api/citizenrequests', methods=['POST'])
def add_service_request():
    """Allow a citizen to submit a new service request."""
    data = request.json
    userid_=data['citizenid']
    user = User.query.filter_by(userid = userid_).first()
    if not data or 'citizenid' not in data or 'requesttype' not in data:
        return jsonify({"error": "Citizen ID and request type are required"}), 400

    new_request = ServiceRequest(
        citizenid=user.citizenid,
        requesttype=data['requesttype'],
        requestdate=datetime.utcnow(),
        status="Pending"
    )
    print(new_request)
    db.session.add(new_request)
    db.session.commit()
    return jsonify({'message': 'Request submitted successfully'}), 201

#Employee - Service Requests

@app.route('/servicerequests')
def servicerequests_page():
    return send_file('Services_employee.html')

@app.route('/api/servicerequests', methods=['GET'])
def get_service_requests():
    requests = db.session.query(
        ServiceRequest.requestid,
        Citizen.fullname.label('citizenname'),
        ServiceRequest.requesttype,
        ServiceRequest.requestdate,
        ServiceRequest.status
    ).join(Citizen, ServiceRequest.citizenid == Citizen.citizenid).filter(ServiceRequest.status == "Pending").order_by(ServiceRequest.requestdate.asc()).all()
    return jsonify([
        {
            'requestid': req.requestid,
            'citizenname': req.citizenname,
            'requesttype': req.requesttype,
            'requestdate': req.requestdate.strftime('%Y-%m-%d'),
            'status': req.status
        }
        for req in requests
    ])

@app.route('/api/servicerequests/<int:requestid>', methods=['PUT'])
def update_service_request(requestid):
    data = request.json
    new_status = data.get('status')

    if new_status not in ['approved', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400

    request_entry = ServiceRequest.query.get(requestid)
    if not request_entry:
        return jsonify({'error': 'Request not found'}), 404

    request_entry.status = new_status.capitalize()
    print(request_entry.status)
    db.session.commit()

    return jsonify({'message': f'Service request {new_status} successfully'}), 200

# Vaccinations
@app.route('/vaccinations')
def vaccinations_page():
    is_monitor = request.args.get('monitor', default="false").lower() == "true"
    if is_monitor:
        return send_file("Vaccinations_monitor.html")
    
    return send_file('Vaccinations_employee.html')

@app.route('/api/vaccinations', methods=['GET'])
def get_vaccinations():
    vaccinations = db.session.query(Vaccination, Citizen.fullname).join(Citizen, Citizen.citizenid == Vaccination.citizenid).all()

    return jsonify([{
        'id': record.Vaccination.vaccinationid,
        'citizen_name': record.fullname,
        'citizen_id': record.Vaccination.citizenid,
        'vaccinetype': record.Vaccination.vaccinetype,
        'date_administered': record.Vaccination.dateadministered.strftime('%Y-%m-%d')
    } for record in vaccinations])

@app.route('/api/vaccinations', methods=['POST'])
def add_vaccination():
    """Add a vaccination record."""
    data = request.json
    userid_ = data['citizenid']
    user = User.query.filter_by(userid = userid_).first()
    print("Received Data:", data)

    new_vaccination = Vaccination(
        citizenid=user.citizenid,
        vaccinetype=data['vaccinetype'],
        dateadministered=datetime.strptime(data['dateadministered'], '%Y-%m-%d')
    )

    db.session.add(new_vaccination)
    db.session.commit()

    return jsonify({'message': 'Vaccination record added successfully'}), 201

@app.route('/api/vaccinations/<int:vaccinationid>', methods=['DELETE'])
def delete_vaccination(vaccinationid):
    vaccination = Vaccination.query.get(vaccinationid)
    if vaccination:
        db.session.delete(vaccination)
        db.session.commit()
        return jsonify({'message': 'vaccination deleted successfully'}), 200
    return jsonify({'error': 'vaccination not found'}), 404


#census data
@app.route('/census')
def census_page():
    userid_ = request.args.get('id', type=int)
    user = User.query.filter_by(userid = userid_).first()
    is_monitor = request.args.get('monitor', default="false").lower() == "true"
    if is_monitor:
        return send_file('Census_monitor.html')
    
    return send_file('Census_data.html')

@app.route('/api/census', methods=['POST'])
def add_census_data():
    """Allow employees to add census records."""
    data = request.json
    userid_ = data['citizenid']
    user = User.query.filter_by(userid = userid_).first()
    
    if not data or 'citizenid' not in data or 'eventtype' not in data or 'eventdate' not in data:
        return jsonify({"error": "Citizen ID, event type, and date are required"}), 400

    new_entry = CensusData(
        citizenid=user.citizenid,
        eventtype=data['eventtype'],
        eventdate=datetime.strptime(data['eventdate'], '%Y-%m-%d'),
        eventnotes=data.get('eventnotes', '')
    )

    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Census data added successfully!"}), 201

@app.route('/censusreport')
def census_report_page():
    
    return send_file('Census_report.html')

@app.route('/api/censusreport')
def get_census_report():
    current_year = datetime.now().year
    years = [current_year - 4, current_year - 3, current_year - 2, current_year - 1, current_year]

    total_population_query = db.session.query(Citizen).count()
    male_count_query = db.session.query(Citizen).filter(Citizen.gender == 'Male').count()
    female_count_query = db.session.query(Citizen).filter(Citizen.gender == 'Female').count()
    other_count_query = db.session.query(Citizen).filter(Citizen.gender == 'Other').count()
    
    total_households = db.session.query(Households).count()
    
    all_households = db.session.query(Households.numberofmembers).all()
    total_members = sum(household[0] for household in all_households)
    avg_household_size = total_members / total_households if total_households > 0 else 0
    
    all_incomes = db.session.query(Households.income).all()
    total_income = sum(income[0] for income in all_incomes)
    avg_household_income = total_income / total_households if total_households > 0 else 0
    
    current_date = datetime.now().date()
    
    all_citizens = db.session.query(Citizen.dateofbirth).all()
    
    children_count = 0
    youth_count = 0
    adults_count = 0
    seniors_count = 0
    
    for citizen in all_citizens:
        birth_date = citizen[0]
        age_days = (current_date - birth_date).days
        
        if age_days < 365 * 15:
            children_count += 1
        elif age_days < 365 * 25:
            youth_count += 1
        elif age_days < 365 * 60:
            adults_count += 1
        else:
            seniors_count += 1
    
    yearly_data = {
        year: {"births": 0, "deaths": 0, "marriages": 0, "divorces": 0} for year in years
    }
    
    all_events = db.session.query(CensusData.eventtype, CensusData.eventdate).all()
    
    for event_type, event_date in all_events:
        event_year = event_date.year
        if event_year in years:
            if event_type == 'Birth':
                yearly_data[event_year]['births'] += 1
            elif event_type == 'Death':
                yearly_data[event_year]['deaths'] += 1
            elif event_type == 'Marriage':
                yearly_data[event_year]['marriages'] += 1
            elif event_type == 'Divorce':
                yearly_data[event_year]['divorces'] += 1
    
    male_population = male_count_query
    female_population = female_count_query
    
    gender_rate_data = {
        year: {
            "male_births": 0,
            "female_births": 0,
            "male_deaths": 0,
            "female_deaths": 0
        } for year in years
    }
    
    birth_events = db.session.query(CensusData, Citizen)\
        .join(Citizen, CensusData.citizenid == Citizen.citizenid)\
        .filter(CensusData.eventtype == 'Birth')\
        .all()
        
    death_events = db.session.query(CensusData, Citizen)\
        .join(Citizen, CensusData.citizenid == Citizen.citizenid)\
        .filter(CensusData.eventtype == 'Death')\
        .all()
    
    # Count births by gender and year
    for event, citizen in birth_events:
        event_year = event.eventdate.year
        if event_year in years:
            if citizen.gender == 'Male':
                gender_rate_data[event_year]['male_births'] += 1
            elif citizen.gender == 'Female':
                gender_rate_data[event_year]['female_births'] += 1
    
    # Count deaths by gender and year
    for event, citizen in death_events:
        event_year = event.eventdate.year
        if event_year in years:
            if citizen.gender == 'Male':
                gender_rate_data[event_year]['male_deaths'] += 1
            elif citizen.gender == 'Female':
                gender_rate_data[event_year]['female_deaths'] += 1
    
    # Extract yearly trends for gender rates
    male_births_trend = [gender_rate_data[year]['male_births'] for year in years]
    female_births_trend = [gender_rate_data[year]['female_births'] for year in years]
    male_deaths_trend = [gender_rate_data[year]['male_deaths'] for year in years]
    female_deaths_trend = [gender_rate_data[year]['female_deaths'] for year in years]
    
    # Calculate overall rates per 1000 population (for backward compatibility)
    total_male_births = sum(gender_rate_data[year]['male_births'] for year in years)
    total_female_births = sum(gender_rate_data[year]['female_births'] for year in years)
    total_male_deaths = sum(gender_rate_data[year]['male_deaths'] for year in years)
    total_female_deaths = sum(gender_rate_data[year]['female_deaths'] for year in years)
    
    # Income brackets distribution
    income_brackets = [
        {"label": "Below ₹25,000", "min": 0, "max": 25000},
        {"label": "₹25,000 - ₹50,000", "min": 25001, "max": 50000},
        {"label": "₹50,001 - ₹75,000", "min": 50001, "max": 75000},
        {"label": "₹75,001 - ₹100,000", "min": 75001, "max": 100000},
        {"label": "Above ₹100,000", "min": 100001, "max": float('inf')}
    ]
    
    income_counts = []
    all_incomes = db.session.query(Households.income).all()
    
    for bracket in income_brackets:
        count = sum(1 for income in all_incomes if bracket["min"] <= income[0] <= bracket["max"])
        income_counts.append(count)
    
    income_labels = [bracket["label"] for bracket in income_brackets]
    
    # Compile final JSON response
    census_data = {
        "population": {
            "total": total_population_query,
            "male": male_count_query,
            "female": female_count_query,
            "other": other_count_query
        },
        "households": {
            "total": total_households,
            "average_size": round(avg_household_size, 2),
            "average_income": round(avg_household_income, 2)
        },
        "age_distribution": {
            "children": children_count,
            "youth": youth_count,
            "adults": adults_count,
            "seniors": seniors_count
        },
        "yearly_trends": {
            "years": years,
            "births": [yearly_data[year]['births'] for year in years],
            "deaths": [yearly_data[year]['deaths'] for year in years],
            "marriages": [yearly_data[year]['marriages'] for year in years],
            "divorces": [yearly_data[year]['divorces'] for year in years]
        },
        "gender_rates": {
            "years": years,
            "male_births": male_births_trend,
            "female_births": female_births_trend,
            "male_deaths": male_deaths_trend,
            "female_deaths": female_deaths_trend,
        },
        "income_brackets": {
            "labels": income_labels,
            "counts": income_counts
        }
    }
    
    return jsonify(census_data)

#Admin page
@app.route('/admin')
def admin_home():
    password = request.args.get('password',str)
    if(password == password_admin):
        return send_file("Home_admin.html")
    return jsonify({"error": "Incorrect password"})

@app.route('/admin/add-citizen', methods=['POST'])
def add_citizen():
    data = request.json
    household_registered = data.get("household_registered")  # Expecting 'yes' or 'no'

    if household_registered == "yes":
        householdid = data.get("householdid")
        household = Households.query.filter_by(householdid=householdid).first()
        if not household:
            return jsonify({"error": "Household not found"}), 404
        
        # Increase number of members in the household
        household.numberofmembers += 1

    else:  # If household is not registered, create a new one
        new_household = Households(
            address=data.get("address"),
            income=data.get("income"),
            numberofmembers=1,  # Since we're adding the first member
            propertyvalue=data.get("propertyvalue")
        )
        db.session.add(new_household)
        db.session.commit()  # Commit to generate householdid
        householdid = new_household.householdid

    # Add the new citizen with the determined householdid
    new_citizen = Citizen(
        fullname=data.get("fullname"),
        dateofbirth=datetime.strptime(data.get("dateofbirth"), '%Y-%m-%d'),
        gender=data.get("gender"),
        householdid=householdid,
        contactnumber=data.get("contactnumber"),
        job=data.get("job"),
        educationalqualification=data.get("educationalqualification")
    )
    
    db.session.add(new_citizen)
    db.session.commit()

    return jsonify({"success": "Citizen added successfully!"})

@app.route('/admin/delete-citizen', methods=['POST'])
def delete_citizen():
    data = request.json
    citizen = Citizen.query.filter_by(citizenid=data['citizenid']).first()
    householdid = citizen.householdid
    Citizen.query.filter_by(citizenid=data['citizenid']).delete()
    # householdid = data.get("householdid")
    household = Households.query.filter_by(householdid=householdid).first()
    if household.numberofmembers == 1:
        Households.query.filter_by(householdid=household.householdid).delete()
    else:
        household.numberofmembers -= 1
    db.session.commit()
    return jsonify({"success": "Citizen deleted successfully!"})

@app.route('/admin/add-employee', methods=['POST'])
def add_employee():
    data = request.json
    new_employee = Employee(citizenid=data['citizenid'], role=data['role'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"success": "Employee added successfully!"})

@app.route('/admin/edit-employee', methods=['GET', 'POST'])
def edit_employee():
    if request.method == 'GET':
        employees = Employee.query.all()
        return jsonify([{ "id": e.employeeid, "citizen_id": e.citizenid, "role": e.role } for e in employees])
    
    data = request.json
    employee = Employee.query.filter_by(employeeid=data['employeeid']).first()
    if employee:
        employee.role = data['role']
        db.session.commit()
        return jsonify({"success": "Employee updated successfully!"})
    return jsonify({"error": "Employee not found"}), 401


@app.route('/admin/remove-employee', methods=['POST'])
def remove_employee():
    data = request.json
    employee = Employee.query.filter_by(employeeid=data['employeeid']).first()
    if not employee:
        return jsonify({"error": "Employee not found"}), 401
    # citizen = Citizen.query.filter_by(citizenid=employee.citizenid).first()
    user  = User.query.filter_by(citizenid=employee.citizenid).first()
    user.role = "Citizen"
    Employee.query.filter_by(employeeid=data['employeeid']).delete()
    db.session.commit()
    return jsonify({"success": "Employee removed successfully!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5173, debug=True)

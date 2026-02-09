"""Service for pre-built example demonstrations."""
from typing import Dict
from app.models.domain import AnalysisResult


class ExampleService:
    """Service for retrieving pre-built example demonstrations."""
    
    # Pre-built examples for reliable demos
    EXAMPLES: Dict[str, AnalysisResult] = {
        "food-pantry": AnalysisResult(
            summary="A Food Pantry Management System for tracking inventory, donations, and distributions. The system helps organizations manage their food bank operations efficiently with features for item tracking, donor management, and distribution records.",
            files={
                "models.py": """from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Donor(Base):
    __tablename__ = "donors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    donations = relationship("Donation", back_populates="donor")


class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    quantity = Column(Integer, default=0)
    unit = Column(String(20), default="units")
    expiry_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    donations = relationship("Donation", back_populates="item")
    distributions = relationship("DistributionItem", back_populates="item")


class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, nullable=False)
    donation_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    donor = relationship("Donor", back_populates="donations")
    item = relationship("Item", back_populates="donations")


class Distribution(Base):
    __tablename__ = "distributions"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_name = Column(String(100), nullable=False)
    recipient_contact = Column(String(100))
    distribution_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    items = relationship("DistributionItem", back_populates="distribution")


class DistributionItem(Base):
    __tablename__ = "distribution_items"
    
    id = Column(Integer, primary_key=True, index=True)
    distribution_id = Column(Integer, ForeignKey("distributions.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, nullable=False)
    
    distribution = relationship("Distribution", back_populates="items")
    item = relationship("Item", back_populates="distributions")
""",
                "main.py": """from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models.domain import Donor, Item, Donation, Distribution, DistributionItem
from app.database import get_db

app = FastAPI(title="Food Pantry Management API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Donor endpoints
@app.get("/api/donors", response_model=List[dict])
def get_donors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    donors = db.query(Donor).offset(skip).limit(limit).all()
    return [{"id": d.id, "name": d.name, "email": d.email, "phone": d.phone} for d in donors]


@app.post("/api/donors")
def create_donor(donor_data: dict, db: Session = Depends(get_db)):
    donor = Donor(**donor_data)
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return {"id": donor.id, "name": donor.name, "email": donor.email}


@app.get("/api/donors/{donor_id}")
def get_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return {"id": donor.id, "name": donor.name, "email": donor.email, "phone": donor.phone}


@app.put("/api/donors/{donor_id}")
def update_donor(donor_id: int, donor_data: dict, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    for key, value in donor_data.items():
        setattr(donor, key, value)
    db.commit()
    return {"id": donor.id, "name": donor.name, "email": donor.email}


@app.delete("/api/donors/{donor_id}")
def delete_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    db.delete(donor)
    db.commit()
    return {"message": "Donor deleted successfully"}


# Item endpoints
@app.get("/api/items", response_model=List[dict])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return [{"id": i.id, "name": i.name, "category": i.category, "quantity": i.quantity} for i in items]


@app.post("/api/items")
def create_item(item_data: dict, db: Session = Depends(get_db)):
    item = Item(**item_data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name, "quantity": item.quantity}


@app.get("/api/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item.id, "name": item.name, "category": item.category, "quantity": item.quantity}


@app.put("/api/items/{item_id}")
def update_item(item_id: int, item_data: dict, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item_data.items():
        setattr(item, key, value)
    db.commit()
    return {"id": item.id, "name": item.name, "quantity": item.quantity}


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}


# Donation endpoints
@app.post("/api/donations")
def create_donation(donation_data: dict, db: Session = Depends(get_db)):
    donation = Donation(**donation_data)
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return {"id": donation.id, "donor_id": donation.donor_id, "item_id": donation.item_id}


@app.get("/api/donations", response_model=List[dict])
def get_donations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    donations = db.query(Donation).offset(skip).limit(limit).all()
    return [{"id": d.id, "donor_id": d.donor_id, "item_id": d.item_id, "quantity": d.quantity} for d in donations]
""",
                "App.jsx": """import React, { useState } from 'react';
import { PlusIcon, TrashIcon, PencilIcon } from 'lucide-react';

function App() {
  const [donors, setDonors] = useState([]);
  const [items, setItems] = useState([]);
  const [donations, setDonations] = useState([]);
  const [activeTab, setActiveTab] = useState('donors');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();
    const endpoint = activeTab === 'donors' ? '/api/donors' : 
                     activeTab === 'items' ? '/api/items' : '/api/donations';
    
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      if (activeTab === 'donors') setDonors([...donors, data]);
      else if (activeTab === 'items') setItems([...items, data]);
      else setDonations([...donations, data]);
      setShowModal(false);
      setFormData({});
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          🥫 Food Pantry Management System
        </h1>
        
        {/* Tabs */}
        <div className="flex space-x-4 mb-6 border-b border-gray-300">
          {['donors', 'items', 'donations'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 font-semibold capitalize transition-colors ${
                activeTab === tab
                  ? 'border-b-2 border-indigo-600 text-indigo-600'
                  : 'text-gray-600 hover:text-indigo-600'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-gray-800 capitalize">{activeTab}</h2>
            <button
              onClick={() => setShowModal(true)}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 flex items-center gap-2"
            >
              <PlusIcon size={20} />
              Add New
            </button>
          </div>

          {/* Table */}
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border p-3 text-left">ID</th>
                  <th className="border p-3 text-left">Name</th>
                  {activeTab === 'donors' && <th className="border p-3 text-left">Email</th>}
                  {activeTab === 'items' && <th className="border p-3 text-left">Category</th>}
                  {activeTab === 'items' && <th className="border p-3 text-left">Quantity</th>}
                  <th className="border p-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {(activeTab === 'donors' ? donors : activeTab === 'items' ? items : donations).map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="border p-3">{item.id}</td>
                    <td className="border p-3">{item.name}</td>
                    {activeTab === 'donors' && <td className="border p-3">{item.email}</td>}
                    {activeTab === 'items' && <td className="border p-3">{item.category}</td>}
                    {activeTab === 'items' && <td className="border p-3">{item.quantity}</td>}
                    <td className="border p-3">
                      <div className="flex gap-2">
                        <button className="text-blue-600 hover:text-blue-800">
                          <PencilIcon size={18} />
                        </button>
                        <button className="text-red-600 hover:text-red-800">
                          <TrashIcon size={18} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-96">
              <h3 className="text-xl font-semibold mb-4">Add New {activeTab.slice(0, -1)}</h3>
              <form onSubmit={handleSubmit}>
                {activeTab === 'donors' && (
                  <>
                    <input
                      type="text"
                      placeholder="Name"
                      className="w-full p-2 border rounded mb-2"
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                    />
                    <input
                      type="email"
                      placeholder="Email"
                      className="w-full p-2 border rounded mb-2"
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                    />
                  </>
                )}
                {activeTab === 'items' && (
                  <>
                    <input
                      type="text"
                      placeholder="Name"
                      className="w-full p-2 border rounded mb-2"
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                    />
                    <input
                      type="text"
                      placeholder="Category"
                      className="w-full p-2 border rounded mb-2"
                      onChange={(e) => setFormData({...formData, category: e.target.value})}
                    />
                    <input
                      type="number"
                      placeholder="Quantity"
                      className="w-full p-2 border rounded mb-2"
                      onChange={(e) => setFormData({...formData, quantity: parseInt(e.target.value)})}
                    />
                  </>
                )}
                <div className="flex gap-2 mt-4">
                  <button
                    type="submit"
                    className="flex-1 bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700"
                  >
                    Save
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="flex-1 bg-gray-300 text-gray-700 py-2 rounded hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
""",
                "README.md": """# Food Pantry Management System

A full-stack application for managing food pantry operations including inventory, donations, and distributions.

## Features

- Donor management
- Inventory tracking
- Donation records
- Distribution tracking

## Setup Instructions

### Backend Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn sqlalchemy python-dotenv google-generativeai
```

2. Set up environment variables:
```bash
export GEMINI_API_KEY=your_api_key_here
```

3. Initialize database:
```bash
# Create database and run migrations
```

4. Run the server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open browser:
```
http://localhost:5173
```

## API Endpoints

- `GET /api/donors` - List all donors
- `POST /api/donors` - Create a new donor
- `GET /api/items` - List all items
- `POST /api/items` - Create a new item
- `GET /api/donations` - List all donations
- `POST /api/donations` - Create a new donation

## Deployment

### Backend (Render/Railway)
1. Set environment variables
2. Deploy FastAPI application
3. Configure database

### Frontend (Vercel)
1. Connect GitHub repository
2. Set build command: `npm run build`
3. Deploy
"""
            }
        ),
        "library": AnalysisResult(
            summary="A Library Book Tracking System for managing books, members, and loans. The system enables librarians to track book inventory, manage member registrations, and handle book checkouts and returns efficiently.",
            files={
                "models.py": """from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(20), unique=True, index=True)
    category = Column(String(50))
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    loans = relationship("Loan", back_populates="book")


class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    membership_date = Column(DateTime, default=datetime.utcnow)
    
    loans = relationship("Loan", back_populates="member")


class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    loan_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime)
    
    book = relationship("Book", back_populates="loans")
    member = relationship("Member", back_populates="loans")
""",
                "main.py": """from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.models.domain import Book, Member, Loan
from app.database import get_db

app = FastAPI(title="Library Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/books", response_model=List[dict])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return [{"id": b.id, "title": b.title, "author": b.author, "isbn": b.isbn, "available": b.available} for b in books]


@app.post("/api/books")
def create_book(book_data: dict, db: Session = Depends(get_db)):
    book = Book(**book_data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"id": book.id, "title": book.title, "author": book.author}


@app.get("/api/members", response_model=List[dict])
def get_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = db.query(Member).offset(skip).limit(limit).all()
    return [{"id": m.id, "name": m.name, "email": m.email, "phone": m.phone} for m in members]


@app.post("/api/members")
def create_member(member_data: dict, db: Session = Depends(get_db)):
    member = Member(**member_data)
    db.add(member)
    db.commit()
    db.refresh(member)
    return {"id": member.id, "name": member.name, "email": member.email}


@app.post("/api/loans")
def create_loan(loan_data: dict, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == loan_data["book_id"]).first()
    if not book or not book.available:
        raise HTTPException(status_code=400, detail="Book not available")
    
    loan = Loan(
        book_id=loan_data["book_id"],
        member_id=loan_data["member_id"],
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    book.available = False
    db.add(loan)
    db.commit()
    return {"id": loan.id, "book_id": loan.book_id, "member_id": loan.member_id}


@app.get("/api/loans", response_model=List[dict])
def get_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    loans = db.query(Loan).offset(skip).limit(limit).all()
    return [{"id": l.id, "book_id": l.book_id, "member_id": l.member_id, "loan_date": str(l.loan_date)} for l in loans]
""",
                "App.jsx": """import React, { useState } from 'react';
import { BookOpen, Users, Calendar } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('books');
  const [books, setBooks] = useState([]);
  const [members, setMembers] = useState([]);
  const [loans, setLoans] = useState([]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-8 text-center flex items-center justify-center gap-3">
          <BookOpen size={40} />
          Library Book Tracking System
        </h1>
        
        <div className="flex space-x-4 mb-6 border-b border-gray-300">
          {[
            { id: 'books', label: 'Books', icon: BookOpen },
            { id: 'members', label: 'Members', icon: Users },
            { id: 'loans', label: 'Loans', icon: Calendar }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 font-semibold flex items-center gap-2 transition-colors ${
                activeTab === tab.id
                  ? 'border-b-2 border-emerald-600 text-emerald-600'
                  : 'text-gray-600 hover:text-emerald-600'
              }`}
            >
              <tab.icon size={20} />
              {tab.label}
            </button>
          ))}
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4 capitalize">{activeTab}</h2>
          <p className="text-gray-600">Manage your library {activeTab} here.</p>
        </div>
      </div>
    </div>
  );
}

export default App;
""",
                "README.md": """# Library Book Tracking System

A comprehensive library management system for tracking books, members, and loans.

## Setup

1. Install backend dependencies: `pip install fastapi uvicorn sqlalchemy`
2. Install frontend dependencies: `npm install`
3. Run backend: `uvicorn main:app --reload`
4. Run frontend: `npm run dev`
"""
            }
        ),
        "clinic": AnalysisResult(
            summary="A Clinic Appointment Management System for scheduling patient appointments, managing doctor schedules, and tracking medical records. The system helps healthcare facilities streamline their appointment booking process.",
            files={
                "models.py": """from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    date_of_birth = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    appointments = relationship("Appointment", back_populates="patient")


class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    
    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="scheduled")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
""",
                "main.py": """from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.models.domain import Patient, Doctor, Appointment
from app.database import get_db

app = FastAPI(title="Clinic Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/patients", response_model=List[dict])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return [{"id": p.id, "name": p.name, "email": p.email, "phone": p.phone} for p in patients]


@app.post("/api/patients")
def create_patient(patient_data: dict, db: Session = Depends(get_db)):
    patient = Patient(**patient_data)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return {"id": patient.id, "name": patient.name, "email": patient.email}


@app.get("/api/doctors", response_model=List[dict])
def get_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).offset(skip).limit(limit).all()
    return [{"id": d.id, "name": d.name, "specialization": d.specialization, "email": d.email} for d in doctors]


@app.post("/api/doctors")
def create_doctor(doctor_data: dict, db: Session = Depends(get_db)):
    doctor = Doctor(**doctor_data)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return {"id": doctor.id, "name": doctor.name, "specialization": doctor.specialization}


@app.post("/api/appointments")
def create_appointment(appointment_data: dict, db: Session = Depends(get_db)):
    appointment = Appointment(**appointment_data)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return {"id": appointment.id, "patient_id": appointment.patient_id, "doctor_id": appointment.doctor_id}


@app.get("/api/appointments", response_model=List[dict])
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).offset(skip).limit(limit).all()
    return [{"id": a.id, "patient_id": a.patient_id, "doctor_id": a.doctor_id, "appointment_date": str(a.appointment_date)} for a in appointments]
""",
                "App.jsx": """import React, { useState } from 'react';
import { Calendar, User, Stethoscope } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('appointments');

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-8 text-center flex items-center justify-center gap-3">
          <Stethoscope size={40} />
          Clinic Appointment Management
        </h1>
        
        <div className="flex space-x-4 mb-6 border-b border-gray-300">
          {[
            { id: 'appointments', label: 'Appointments', icon: Calendar },
            { id: 'patients', label: 'Patients', icon: User },
            { id: 'doctors', label: 'Doctors', icon: Stethoscope }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 font-semibold flex items-center gap-2 transition-colors ${
                activeTab === tab.id
                  ? 'border-b-2 border-red-600 text-red-600'
                  : 'text-gray-600 hover:text-red-600'
              }`}
            >
              <tab.icon size={20} />
              {tab.label}
            </button>
          ))}
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4 capitalize">{activeTab}</h2>
          <p className="text-gray-600">Manage clinic {activeTab} here.</p>
        </div>
      </div>
    </div>
  );
}

export default App;
""",
                "README.md": """# Clinic Appointment Management System

A healthcare management system for scheduling appointments and managing patient records.

## Setup

1. Install dependencies: `pip install fastapi uvicorn sqlalchemy`
2. Run server: `uvicorn main:app --reload`
3. Install frontend: `npm install && npm run dev`
"""
            }
        )
    }
    
    def get_example(self, example_id: str) -> AnalysisResult:
        """
        Get a pre-built example by ID.
        
        Args:
            example_id: Identifier for the example (e.g., "food-pantry", "library", "clinic")
            
        Returns:
            AnalysisResult object
            
        Raises:
            ValueError: If example_id is not found
        """
        if example_id not in self.EXAMPLES:
            available = ", ".join(self.EXAMPLES.keys())
            raise ValueError(f"Example '{example_id}' not found. Available examples: {available}")
        
        return self.EXAMPLES[example_id]
    
    def list_examples(self) -> list[str]:
        """List all available example IDs."""
        return list(self.EXAMPLES.keys())

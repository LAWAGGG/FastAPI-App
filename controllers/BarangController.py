from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from config.db import get_db
from models.barang import Barang
from schemas import BarangCreate, BarangResponse
from utils.auth import get_current_active_user, check_admin, check_staff, check_supervisor
from models.user import User

router = APIRouter()

@router.post("/", response_model=BarangResponse)
def create_barang(
    barang: BarangCreate,
    db: Session = Depends(get_db),
    user: User = Depends(check_staff)
):
    db_barang = Barang(**barang.dict())
    db.add(db_barang)
    db.commit()
    db.refresh(db_barang)
    return db_barang

@router.get("/", response_model=List[BarangResponse])
def read_barang(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    return db.query(Barang).offset(skip).limit(limit).all()

@router.get("/{barang_id}", response_model=BarangResponse)
def read_barang(
    barang_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    db_barang = db.query(Barang).filter(Barang.id == barang_id).first()
    if db_barang is None:
        raise HTTPException(status_code=404, detail="Barang not found")
    return db_barang

@router.put("/{barang_id}", response_model=BarangResponse)
def update_barang(
    barang_id: int,
    barang: BarangCreate,
    db: Session = Depends(get_db),
    user: User = Depends(check_staff)
):
    db_barang = db.query(Barang).filter(Barang.id == barang_id).first()
    if db_barang is None:
        raise HTTPException(status_code=404, detail="Barang not found")
    
    for var, value in barang.dict().items():
        setattr(db_barang, var, value)
    
    db.commit()
    db.refresh(db_barang)
    return db_barang

@router.delete("/{barang_id}")
def delete_barang(
    barang_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(check_admin)
):
    db_barang = db.query(Barang).filter(Barang.id == barang_id).first()
    if db_barang is None:
        raise HTTPException(status_code=404, detail="Barang not found")
    
    db.delete(db_barang)
    db.commit()
    return {"message": "Barang deleted successfully"}
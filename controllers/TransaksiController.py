from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from config.db import get_db
from models.transaksi import Transaksi
from models.barang import Barang
from schemas import TransaksiCreate, TransaksiResponse
from utils.auth import get_current_active_user, check_staff, check_admin
from models.user import User

router = APIRouter()

@router.post("/", response_model=TransaksiResponse)
def create_transaksi(
    transaksi: TransaksiCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    # cek barang
    db_barang = db.query(Barang).filter(Barang.id == transaksi.barang_id).first()
    if not db_barang:
        raise HTTPException(status_code=404, detail="Barang not found")
    
    if db_barang.jumlah < transaksi.jumlah:
        raise HTTPException(status_code=400, detail="Jumlah barang tidak mencukupi")

    # hitung total harga
    total_harga = db_barang.harga * transaksi.jumlah

    # kurangi stok barang
    db_barang.jumlah -= transaksi.jumlah

    # buat transaksi baru
    db_transaksi = Transaksi(
        barang_id=transaksi.barang_id,
        jumlah=transaksi.jumlah,
        total_harga=total_harga
    )

    db.add(db_transaksi)
    db.commit()
    db.refresh(db_transaksi)

    return db_transaksi

@router.get("/", response_model=List[TransaksiResponse])
def read_transaksi(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    return db.query(Transaksi).offset(skip).limit(limit).all()

@router.get("/{transaksi_id}", response_model=TransaksiResponse)
def read_transaksi_by_id(
    transaksi_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if not db_transaksi:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    return db_transaksi

@router.delete("/{transaksi_id}")
def delete_transaksi(
    transaksi_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(check_admin)
):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if not db_transaksi:
        raise HTTPException(status_code=404, detail="Transaksi not found")

    db.delete(db_transaksi)
    db.commit()
    return {"message": "Transaksi deleted successfully"}

@router.put("/{transaksi_id}", response_model=TransaksiResponse)
def update_transaksi(
    transaksi_id: int,
    transaksi: TransaksiCreate,
    db: Session = Depends(get_db),
    user: User = Depends(check_staff)
):
    # cari transaksi
    db_transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if not db_transaksi:
        raise HTTPException(status_code=404, detail="Transaksi not found")

    # cari barang terkait
    db_barang = db.query(Barang).filter(Barang.id == transaksi.barang_id).first()
    if not db_barang:
        raise HTTPException(status_code=404, detail="Barang not found")

    # hitung selisih jumlah (stok harus dikembalikan dulu)
    selisih = transaksi.jumlah - db_transaksi.jumlah

    # cek stok kalau jumlah transaksi baru lebih besar
    if selisih > 0 and db_barang.jumlah < selisih:
        raise HTTPException(status_code=400, detail="Jumlah barang tidak mencukupi")

    # update stok barang
    db_barang.jumlah -= selisih

    # update transaksi
    db_transaksi.barang_id = transaksi.barang_id
    db_transaksi.jumlah = transaksi.jumlah
    db_transaksi.total_harga = db_barang.harga * transaksi.jumlah

    db.commit()
    db.refresh(db_transaksi)

    return db_transaksi


from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from config.db import Base

class Barang(Base):
    __tablename__ = "barang"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, index=True)
    deskripsi = Column(String)
    jumlah = Column(Integer)
    harga = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
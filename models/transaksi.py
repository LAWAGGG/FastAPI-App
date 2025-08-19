from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from config.db import Base

class Transaksi(Base):
    __tablename__ = "transaksi"
    
    id = Column(Integer, primary_key=True, index=True)
    barang_id = Column(Integer, ForeignKey("barang.id"))
    jumlah = Column(Integer, nullable=False)
    total_harga = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
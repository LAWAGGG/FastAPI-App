from fastapi import APIRouter
from controllers.TransaksiController import router as transaksi_router

router = APIRouter()

router.include_router(transaksi_router, prefix="/transaksi", tags=["transaksi"])


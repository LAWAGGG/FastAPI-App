from fastapi import APIRouter
from controllers.BarangController import router as barang_router

router = APIRouter()
router.include_router(barang_router, prefix="/barang", tags=["barang"])
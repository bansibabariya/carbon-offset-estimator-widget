from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .db import SessionLocal, engine
from .models import OptIn
from .config import DEFAULT_WIDGET_CONFIG
from .schema import CartItem, EstimateRequest, EstimateResponse, OptInRequest


# Create tables
OptIn.__table__.create(bind=engine, checkfirst=True)

app = FastAPI(title="Carbon Offset Prototype")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# DB session utility
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Endpoints ---
@app.get('/widget-config')
async def widget_config():
    return DEFAULT_WIDGET_CONFIG


@app.post('/estimate', response_model=EstimateResponse)
async def estimate(req: EstimateRequest):
    breakdown = []
    total = 0.0
    for it in req.cart:
        item_offset = round(it.price * 0.02 * it.quantity, 2)
        breakdown.append({
            'title': it.title,
            'price': it.price,
            'quantity': it.quantity,
            'offset': item_offset
        })
        total += item_offset
    total = round(total, 2)
    return {"estimated_offset": total, "breakdown": breakdown}


@app.post('/optin')
async def optin(req: OptInRequest, db: Session = Depends(get_db)):
    rec = OptIn(
        merchant_id=req.merchant_id,
        customer_email=req.customer_email,
        customer_name=req.customer_name,
        estimated_offset=req.estimated_offset,
        cart_snapshot=[item.dict() for item in req.cart]
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return {"status": "ok", "id": rec.id}


@app.get('/cart-details')
async def mock_cart():
    return {
        "merchant_id": "shopify_store_abc",  
        "customer_email": "bansi@example.com",
        "customer_name": "Bansi Kanani",
        "items": [
            {"id": 1, "title": "T-shirt", "price": 84.99, "quantity": 3, "weight": 0.5, "category": "Clothing"},
            {"id": 2, "title": "Shoe", "price": 12, "quantity": 1, "weight": 0.9, "category": "Accessories"}
        ],
        "estimated_offset": 5.34,
        "currency": "USD"
    }


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>EcoCart</title>
            <style>
                h1 {
                    text-align: center;
                    margin-top: 50px;
                    font-family: Arial, sans-serif;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to EcoCart</h1>
        </body>
    </html>
    """

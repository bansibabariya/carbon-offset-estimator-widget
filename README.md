# Carbon Offset Estimator Widget

A prototype widget that allows customers to **opt-in** to offset the carbon footprint of their orders.


## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy, Pydantic  
- **Frontend:** JavaScript, HTML, CSS  
- **Database:** SQLite  


## Features

- Embeddable **carbon offset widget** on cart page.
- **Estimates offsets** dynamically (`price × 0.02 × quantity`).
- **Tracks customer opt-ins** with merchant ID, email, name, cart details.
- **Stores data** in SQLite (`offsets.db`).
- **Demo cart API** (`/cart-details`) for local testing.


## API Endpoints

- GET **/** Welcome page
- GET **/widget-config** Widget config (placement + verbiage)
- POST **/estimate** Calculate offset from cart
- POST **/optin** Save opt-in record
- GET **/cart-details** Demo cart JSON


## Setup

```bash
git clone https://github.com/bansibabariya/carbon-offset-estimator-widget.git
cd carbon-offset-estimator-widget
pip install -r requirements.txt
uvicorn app.main:app --reload

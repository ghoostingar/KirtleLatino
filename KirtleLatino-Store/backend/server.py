from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'kirtlelatino_store')]

# Create the main app
app = FastAPI(title="KirtleLatino Store API")
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "kirtlelatino-super-secret-key-2024"
ALGORITHM = "HS256"

# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    username: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str
    image_url: str
    features: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CartItem(BaseModel):
    product_id: str
    quantity: int = 1

class Cart(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[CartItem] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[CartItem]
    total_amount: float
    status: str = "pending"
    payment_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Authentication helpers
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return User(**user)

# Initialize products
async def init_products():
    existing = await db.products.find_one()
    if not existing:
        products = [
            {
                "id": str(uuid.uuid4()),
                "name": "Rango VIP",
                "description": "Acceso completo a comandos VIP, kit exclusivo y beneficios especiales",
                "price": 9.99,
                "category": "rangos",
                "image_url": "https://images.unsplash.com/photo-1524685794168-52985e79c1f8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxtaW5lY3JhZnR8ZW58MHx8fHwxNzU3NTMxNTAwfDA&ixlib=rb-4.1.0&q=85",
                "features": ["Kit VIP mensual", "Comandos especiales", "Chat colorido", "Prioridad en el servidor"],
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Rango VIP+",
                "description": "Todos los beneficios VIP + acceso a zonas exclusivas y más comandos",
                "price": 19.99,
                "category": "rangos",
                "image_url": "https://images.unsplash.com/photo-1524685794168-52985e79c1f8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxtaW5lY3JhZnR8ZW58MHx8fHwxNzU3NTMxNTAwfDA&ixlib=rb-4.1.0&q=85",
                "features": ["Todo del VIP", "Comando /fly", "Homes adicionales", "Acceso a zonas VIP+"],
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Rango ELITE",
                "description": "El rango más exclusivo con todos los privilegios del servidor",
                "price": 39.99,
                "category": "rangos",
                "image_url": "https://images.unsplash.com/photo-1524685794168-52985e79c1f8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxtaW5lY3JhZnR8ZW58MHx8fHwxNzU3NTMxNTAwfDA&ixlib=rb-4.1.0&q=85",
                "features": ["Todos los comandos", "Kits ilimitados", "Crear warps", "Moderación básica"],
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Kit Guerrero",
                "description": "Equipamiento completo para batalla con armadura de diamante",
                "price": 4.99,
                "category": "kits",
                "image_url": "https://images.unsplash.com/photo-1697479665524-3e06cf37b2b7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwyfHxtaW5lY3JhZnR8ZW58MHx8fHwxNzU3NTMxNTAwfDA&ixlib=rb-4.1.0&q=85",
                "features": ["Armadura de diamante", "Espada encantada", "Pociones de curación", "Comida"],
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Kit Constructor",
                "description": "Herramientas y materiales para grandes construcciones",
                "price": 7.99,
                "category": "kits",
                "image_url": "https://images.unsplash.com/photo-1697479665524-3e06cf37b2b7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwyfHxtaW5lY3JhZnR8ZW58MHx8fHwxNzU3NTMxNTAwfDA&ixlib=rb-4.1.0&q=85",
                "features": ["Herramientas de diamante", "Bloques variados", "Redstone", "Decoraciones"],
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Protección Premium",
                "description": "Protege tu base con la máxima seguridad disponible",
                "price": 12.99,
                "category": "protecciones",
                "image_url": "https://images.unsplash.com/photo-1697479670670-d2a299df749c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwzfHxtaW5lY3JhZnR8ZW58MHx8fHwxNzU3NTMxNTAwfDAO&ixlib=rb-4.1.0&q=85",
                "features": ["Área 200x200", "Protección total", "Agregar miembros", "Anti-grief"],
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Monedas del Servidor",
                "description": "Moneda virtual para comprar en tiendas del servidor",
                "price": 1.99,
                "category": "monedas",
                "image_url": "https://images.unsplash.com/photo-1587573089734-09cb69c0f2b4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHw0fHxtaW5lY3JhZnR8ZW58MHx8fHwxNzU3NTMxNTAwfDAO&ixlib=rb-4.1.0&q=85",
                "features": ["1000 monedas", "Uso inmediato", "No expiran", "Transferibles"],
                "created_at": datetime.utcnow()
            }
        ]
        await db.products.insert_many(products)

# Routes
@api_router.get("/")
async def root():
    return {"message": "KirtleLatino Store API"}

# Auth routes
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    existing_user = await db.users.find_one({"$or": [{"email": user_data.email}, {"username": user_data.username}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email o username ya está en uso")
    
    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password
    )
    
    await db.users.insert_one(user.dict())
    
    access_token = create_access_token(data={"sub": user.id})
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

@api_router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    user = await db.users.find_one({"email": user_data.email})
    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    
    access_token = create_access_token(data={"sub": user["id"]})
    user_response = UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["username"],
        created_at=user["created_at"]
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)

# Product routes
@api_router.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None):
    await init_products()
    
    if category:
        products = await db.products.find({"category": category}).to_list(1000)
    else:
        products = await db.products.find().to_list(1000)
    
    return [Product(**product) for product in products]

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return Product(**product)

# Cart routes
@api_router.get("/cart", response_model=Cart)
async def get_cart(current_user: User = Depends(get_current_user)):
    cart = await db.carts.find_one({"user_id": current_user.id})
    if not cart:
        cart = Cart(user_id=current_user.id)
        await db.carts.insert_one(cart.dict())
        return cart
    return Cart(**cart)

@api_router.post("/cart/add")
async def add_to_cart(item: CartItem, current_user: User = Depends(get_current_user)):
    product = await db.products.find_one({"id": item.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    cart = await db.carts.find_one({"user_id": current_user.id})
    if not cart:
        cart = Cart(user_id=current_user.id, items=[item])
        await db.carts.insert_one(cart.dict())
    else:
        cart_obj = Cart(**cart)
        existing_item = None
        for i, cart_item in enumerate(cart_obj.items):
            if cart_item.product_id == item.product_id:
                existing_item = i
                break
        
        if existing_item is not None:
            cart_obj.items[existing_item].quantity += item.quantity
        else:
            cart_obj.items.append(item)
        
        cart_obj.updated_at = datetime.utcnow()
        await db.carts.update_one({"user_id": current_user.id}, {"$set": cart_obj.dict()})
    
    return {"message": "Producto agregado al carrito"}

@api_router.delete("/cart/remove/{product_id}")
async def remove_from_cart(product_id: str, current_user: User = Depends(get_current_user)):
    cart = await db.carts.find_one({"user_id": current_user.id})
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    cart_obj = Cart(**cart)
    cart_obj.items = [item for item in cart_obj.items if item.product_id != product_id]
    cart_obj.updated_at = datetime.utcnow()
    
    await db.carts.update_one({"user_id": current_user.id}, {"$set": cart_obj.dict()})
    return {"message": "Producto eliminado del carrito"}

# Order routes
@api_router.post("/orders", response_model=Order)
async def create_order(current_user: User = Depends(get_current_user)):
    cart = await db.carts.find_one({"user_id": current_user.id})
    if not cart or not cart["items"]:
        raise HTTPException(status_code=400, detail="Carrito vacío")
    
    total = 0
    for item in cart["items"]:
        product = await db.products.find_one({"id": item["product_id"]})
        if product:
            total += product["price"] * item["quantity"]
    
    order = Order(
        user_id=current_user.id,
        items=cart["items"],
        total_amount=total
    )
    
    await db.orders.insert_one(order.dict())
    await db.carts.update_one({"user_id": current_user.id}, {"$set": {"items": [], "updated_at": datetime.utcnow()}})
    
    return order

@api_router.get("/orders", response_model=List[Order])
async def get_orders(current_user: User = Depends(get_current_user)):
    orders = await db.orders.find({"user_id": current_user.id}).to_list(1000)
    return [Order(**order) for order in orders]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
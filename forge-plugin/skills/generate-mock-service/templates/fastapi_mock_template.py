# FastAPI Mock Server Template
from fastapi import FastAPI, HTTPException, Query, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import time
import os
from datetime import datetime
import asyncio

# Configuration
PORT = int(os.getenv('PORT', {{PORT}}))
MOCK_DELAY_MS = int(os.getenv('MOCK_DELAY_MS', 100))

app = FastAPI(
    title="{{SERVICE_NAME}}",
    description="Mock service for {{SERVICE_NAME}}",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data store
data_store: Dict[str, Any] = {
    # {{DATA_STORE}}
}

# Pydantic models
class ItemBase(BaseModel):
    # {{MODEL_FIELDS}}
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: Optional[str] = None

class Item(ItemBase):
    id: str
    created_at: str
    updated_at: Optional[str] = None

class ItemList(BaseModel):
    data: List[Item]
    page: int
    limit: int
    total: int

# Delay middleware
@app.middleware("http")
async def add_delay(request: Request, call_next):
    """Simulate network delay"""
    await asyncio.sleep(MOCK_DELAY_MS / 1000.0)
    response = await call_next(request)
    return response

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "{{SERVICE_NAME}}",
        "timestamp": datetime.now().isoformat()
    }

# {{ENDPOINT_NAME}} - GET list
@app.get("/{{ENDPOINT_PATH}}", response_model=ItemList)
async def get_items(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    x_mock_scenario: Optional[str] = Header(None)
):
    """Get paginated list of items"""
    
    # Simulate error scenario
    if x_mock_scenario == 'error':
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_server_error",
                "message": "Simulated server error"
            }
        )
    
    # Get items
    items = list(data_store.values())
    start = (page - 1) * limit
    end = start + limit
    
    return {
        "data": items[start:end],
        "page": page,
        "limit": limit,
        "total": len(items)
    }

# {{ENDPOINT_NAME}} - GET by ID
@app.get("/{{ENDPOINT_PATH}}/{item_id}", response_model=Item)
async def get_item(item_id: str):
    """Get item by ID"""
    
    if item_id not in data_store:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"Item {item_id} not found"
            }
        )
    
    return data_store[item_id]

# {{ENDPOINT_NAME}} - POST
@app.post("/{{ENDPOINT_PATH}}", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Create new item"""
    
    # Simulate specific error scenarios
    if hasattr(item, 'trigger_error') and item.trigger_error:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "unprocessable_entity",
                "message": "Unable to process request",
                "details": item.trigger_error
            }
        )
    
    # Create new item
    item_id = f"id_{int(time.time() * 1000)}"
    new_item = Item(
        id=item_id,
        **item.dict(),
        created_at=datetime.now().isoformat()
    )
    
    data_store[item_id] = new_item.dict()
    
    return new_item

# {{ENDPOINT_NAME}} - PUT
@app.put("/{{ENDPOINT_PATH}}/{item_id}", response_model=Item)
async def update_item(item_id: str, item: ItemUpdate):
    """Update item"""
    
    if item_id not in data_store:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"Item {item_id} not found"
            }
        )
    
    # Update only provided fields
    updated_data = {
        **data_store[item_id],
        **item.dict(exclude_unset=True),
        "updated_at": datetime.now().isoformat()
    }
    
    data_store[item_id] = updated_data
    
    return Item(**updated_data)

# {{ENDPOINT_NAME}} - PATCH (partial update)
@app.patch("/{{ENDPOINT_PATH}}/{item_id}", response_model=Item)
async def patch_item(item_id: str, item: ItemUpdate):
    """Partially update item"""
    return await update_item(item_id, item)

# {{ENDPOINT_NAME}} - DELETE
@app.delete("/{{ENDPOINT_PATH}}/{item_id}", status_code=204)
async def delete_item(item_id: str):
    """Delete item"""
    
    if item_id not in data_store:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"Item {item_id} not found"
            }
        )
    
    del data_store[item_id]
    return None

if __name__ == "__main__":
    import uvicorn
    
    print(f"🎭 Mock Service: {{SERVICE_NAME}}")
    print(f"📍 Running on port: {PORT}")
    print(f"🔗 Health check: http://localhost:{PORT}/health")
    print(f"📚 API docs: http://localhost:{PORT}/docs")
    print(f"📖 ReDoc: http://localhost:{PORT}/redoc")
    print(f"\nAvailable endpoints:")
    print(f"  GET    http://localhost:{PORT}/{{ENDPOINT_PATH}}")
    print(f"  GET    http://localhost:{PORT}/{{ENDPOINT_PATH}}/{{id}}")
    print(f"  POST   http://localhost:{PORT}/{{ENDPOINT_PATH}}")
    print(f"  PUT    http://localhost:{PORT}/{{ENDPOINT_PATH}}/{{id}}")
    print(f"  PATCH  http://localhost:{PORT}/{{ENDPOINT_PATH}}/{{id}}")
    print(f"  DELETE http://localhost:{PORT}/{{ENDPOINT_PATH}}/{{id}}")
    print(f"\nMock delay: {MOCK_DELAY_MS}ms")
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.avaliacao_pedido_routers import router as avaliacao_pedido_router
from app.routers.consumidor_routers import router as consumidor_router
from app.routers.item_pedido_routers import router as item_pedido_router
from app.routers.pedido_routers import router as pedido_router
from app.routers.produto_routers import router as produto_router
from app.routers.vendedor_routers import router as vendedor_router

app = FastAPI(
    title="Sistema de Compras Online",
    description="API para gerenciamento de pedidos, produtos, consumidores e vendedores.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produto_router)
app.include_router(vendedor_router)
app.include_router(consumidor_router)
app.include_router(pedido_router)
app.include_router(avaliacao_pedido_router)
app.include_router(item_pedido_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

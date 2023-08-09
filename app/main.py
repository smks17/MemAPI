from __future__ import annotations

import asyncio

from fastapi import FastAPI

from .config import settings, info_settings
from .mem_info import log_memory_usage
import app.routers.user as users_router
import app.routers.mem as mem_router


app = FastAPI(
    debug=settings.debug,
    **(info_settings.model_dump())
)


# add routers
app.include_router(router=users_router.router)
app.include_router(router=mem_router.router)

# default page
@app.get("/")
async def root():
    return {"message": "Hello, This is a test of API task. For usage see '/docs'"}

task: asyncio.Task = None

@app.on_event("startup")
async def shutdown():
    global task
    # runs tracking memory usage by asynchronous
    loop = asyncio.get_event_loop()
    task = loop.create_task(log_memory_usage(), name="log_mem")

@app.on_event("shutdown")
async def shutdown():
    # cancel the logging memory task
    task.cancel()

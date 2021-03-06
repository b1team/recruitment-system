from fastapi import APIRouter
from .endpoints import employees
from .endpoints import employers
from .endpoints import jobs
from .endpoints import users
from .endpoints import login
from .endpoints import register
from .endpoints import tags
from .endpoints import applies

router = APIRouter()

router.include_router(login.router, tags=["login"])
router.include_router(register.router, tags=["register"])
router.include_router(tags.router, tags=["tags"])
router.include_router(users.router, tags=["users"])
router.include_router(jobs.router, tags=["jobs"])
router.include_router(employers.router, tags=["employers"])
router.include_router(employees.router, tags=["employees"])
router.include_router(applies.router, tags=["apply"])


# file scr\routers\tags.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas import tags_shemas
from src.schemas import photo_schema
from src.crud import tags
from src.services.roles import RoleAccess #27/02/24 Olha
from src.db.models import Role  # 27/02/24 Olha
from src.services import roles #27/02/24 Olha

router = APIRouter()

allowed_operation_create = roles.RoleAccess([Role.admin, Role.moderator, Role.user]) #27/02/24 Olha


@router.post("/photos/{photo_id}/tags", response_model=photo_schema.Photo)
def add_tags_to_photo(
    photo_id: int,
    tag_data: tags_shemas.PhotoTagsUpdate,
    db: Session = Depends(get_db),
    _: RoleAccess = Depends(allowed_operation_create) #27/02/24 Olha
):
    if len(tag_data.tags) > 5:
        raise HTTPException(status_code=400, detail="Cannot add more than 5 tags to a photo.")
    return tags.associate_tags_with_photo(db, photo_id, tag_data.tags)

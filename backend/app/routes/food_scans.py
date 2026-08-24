from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..models import Purchase
from ..security import get_current_user, get_db
from ..services import food_vision

router = APIRouter(prefix="/food-scans", tags=["Food Scans"])

MAX_IMAGE_BYTES = 5 * 1024 * 1024
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAGIC_BYTES = {
    "image/jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
    "image/png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    "image/gif": lambda data: data.startswith((b"GIF87a", b"GIF89a")),
    "image/webp": lambda data: data.startswith(b"RIFF") and data[8:12] == b"WEBP",
}


def _validate_image(mime_type: str | None, data: bytes):
    if mime_type not in ALLOWED_MIME_TYPES or not MAGIC_BYTES[mime_type](data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported or invalid image")
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Image exceeds 5 MB limit")


def _scan_response(scan):
    return schemas.FoodScanResponse.model_validate(scan)


@router.post('/analyze', response_model=schemas.FoodScanResponse, status_code=201)
async def analyze_food_scan(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = await image.read(MAX_IMAGE_BYTES + 1)
    _validate_image(image.content_type, data)
    try:
        analysis = food_vision.analyze_image(data, image.content_type)
    except food_vision.FoodVisionError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    except (ValueError, TypeError, KeyError) as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Food analysis returned an invalid result") from exc

    scan = crud.create_food_scan(db, {
        "user_id": current_user.user_id,
        "detected_food_name": analysis.get("food_name"),
        "confidence": analysis.get("confidence"),
        "estimated_calories": analysis.get("estimated_calories"),
        "estimated_protein": analysis.get("estimated_protein_g"),
        "estimated_carbohydrates": analysis.get("estimated_carbohydrates_g"),
        "estimated_fat": analysis.get("estimated_fat_g"),
        "estimated_fiber": analysis.get("estimated_fiber_g"),
        "portion_description": analysis.get("portion_description"),
        "analysis_notes": analysis.get("notes"),
        "raw_analysis": analysis,
        "status": "pending_review",
    })
    return _scan_response(scan)


@router.get('', response_model=list[schemas.FoodScanResponse])
def list_food_scans(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return [_scan_response(scan) for scan in crud.get_food_scans(db, current_user.user_id)]


@router.get('/{scan_id}', response_model=schemas.FoodScanResponse)
def get_food_scan(scan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    scan = crud.get_food_scan(db, scan_id, current_user.user_id)
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food scan not found")
    return _scan_response(scan)


@router.post('/{scan_id}/confirm')
def confirm_food_scan(
    scan_id: int,
    update: schemas.FoodScanConfirm,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    scan = crud.get_food_scan(db, scan_id, current_user.user_id)
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food scan not found")
    if scan.status == "confirmed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Food scan is already confirmed")

    fields = update.model_dump(exclude={"add_to_purchases", "food_item_id", "quantity"}, exclude_unset=True)
    if fields:
        crud.update_food_scan(db, scan, fields)
    scan = crud.update_food_scan(db, scan, {"status": "confirmed"})

    purchase = None
    if update.add_to_purchases:
        if not update.food_item_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Select a catalogue item before adding a purchase")
        food = crud.get_food_item(db, update.food_item_id)
        if not food or not food.is_available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Selected food item is unavailable")
        unit_price = float(food.price)
        purchase = crud.create_purchase_from_dict(db, {
            "user_id": current_user.user_id,
            "item_id": food.item_id,
            "quantity": update.quantity,
            "unit_price": unit_price,
            "total_price": unit_price * update.quantity,
            "amount": unit_price * update.quantity,
            "notes": f"Added from food scan {scan.scan_id}",
        })

    return {"scan": _scan_response(scan), "purchase_id": purchase.purchase_id if purchase else None}


@router.delete('/{scan_id}', status_code=204)
def delete_food_scan(scan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    scan = crud.get_food_scan(db, scan_id, current_user.user_id)
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food scan not found")
    crud.delete_food_scan(db, scan)

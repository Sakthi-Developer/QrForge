# routers/qr.py
import io
from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask

# Create an API router instance
router = APIRouter()


def generate_transparent_qr(
    data: str,
    fg_color=(0, 0, 0, 255),
    box_size: int = 10
):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=box_size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        color_mask=SolidFillColorMask(back_color=(0, 0, 0, 0), front_color=fg_color)
    ).convert("RGBA")

    return img


@router.post("/generate_qr")
async def generate_qr(
    data: str = Form(..., description="Data to encode in QR"),
    r: int = Form(0, description="Red (0-255)"),
    g: int = Form(0, description="Green (0-255)"),
    b: int = Form(0, description="Blue (0-255)"),
    a: int = Form(255, description="Alpha (0-255, transparency)"),
    size: int = Form(10, description="Box size of QR modules"),
    download: bool = Form(False, description="Set true to download instead of preview"),
):
    img = generate_transparent_qr(data, fg_color=(r, g, b, a), box_size=size)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    headers = {}
    if download:
        headers["Content-Disposition"] = 'attachment; filename="qr_code.png"'

    return StreamingResponse(buf, media_type="image/png", headers=headers)

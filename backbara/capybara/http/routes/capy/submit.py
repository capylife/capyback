# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import nanoid
import dhash
import aiofiles
import validators
import re

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.datastructures import UploadFile

from datetime import datetime
from PIL import Image
from io import BytesIO
from typing import cast
from names import get_first_name
from os import path

from ....resources import Sessions
from ....env import NANO_ID_LEN, SAVE_PATH
from ....limiter import LIMITER
from ....errors import FormMissingFields, SimilarImageError

from ...decorators import require_captcha


dhash.force_pil()


class SubmitCapyResource(HTTPEndpoint):
    @LIMITER.limit("20/minute")
    @require_captcha
    async def post(self, request: Request) -> JSONResponse:
        form = await request.form()

        if ("file" not in form or not
                isinstance(form["file"], UploadFile)):
            raise FormMissingFields("'file' is required")

        if ("name" not in form or not isinstance(form["name"], str) or not
                re.match(r'[A-Za-z]+', form["name"])):
            name = get_first_name()
        else:
            name = form["name"].capitalize()

        if ("email" not in form or not
                validators.email(form["email"])):
            email = None
        else:
            email = form["email"]

        image: UploadFile = cast(UploadFile, form["file"])
        image_bytes = await image.read()

        p_row, p_col = dhash.dhash_row_col(Image.open(BytesIO(image_bytes)))
        phash = dhash.format_hex(p_row, p_col)

        similar_image = await Sessions.mongo.capybara.count_documents({
            "phash": phash
        })
        if similar_image > 0:
            raise SimilarImageError()

        _id = nanoid.generate(size=NANO_ID_LEN)

        await Sessions.mongo.capybara.insert_one({
            "_id": _id,
            "created": datetime.now(),
            "used": None,
            "approved": False,
            "name": name,
            "phash": phash,
            "email": email,
            "content_type": image.content_type
        })

        async with aiofiles.open(
                path.join(SAVE_PATH, f"{_id}.capy"), "wb") as f_:
            await f_.write(image_bytes)

        return JSONResponse({
            "_id": _id
        })
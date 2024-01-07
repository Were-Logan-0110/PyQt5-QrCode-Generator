from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    RoundedModuleDrawer,
    CircleModuleDrawer,
    HorizontalBarsDrawer,
    VerticalBarsDrawer,
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
)
from qrcode.image.styles.colormasks import (
    RadialGradiantColorMask,
    SolidFillColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask,
    SquareGradiantColorMask,
)
from PIL import Image
from enum import Enum
from functools import lru_cache


class ModuleDrawerStyle(Enum):
    ROUNDED = RoundedModuleDrawer()
    CIRCLE = CircleModuleDrawer()
    HORIZONTAL_BARS = HorizontalBarsDrawer()
    VERTICAL_BARS = VerticalBarsDrawer()
    SQUARE = SquareModuleDrawer()
    GAPPED_SQUARE = GappedSquareModuleDrawer()


class ColorMaskStyle(Enum):
    RADIAL_GRADIENT = RadialGradiantColorMask()
    SOLID_FILL = SolidFillColorMask()
    HORIZONTAL_GRADIENT = HorizontalGradiantColorMask()
    VERTICAL_GRADIENT = VerticalGradiantColorMask()
    SQUARE_GRADIENT = SquareGradiantColorMask()


def replaceWhite(inputImage, newColor=(255, 0, 0, 100)):
    image = inputImage.convert("RGBA")
    data = list(image.getdata())
    newData = [newColor if item[:3] == (255, 255, 255) else item for item in data]
    modifiedImage = Image.new("RGBA", image.size)
    modifiedImage.putdata(newData)
    return modifiedImage


@lru_cache
def generateQrCode(
    data: str,
    moduleDrawer: ModuleDrawerStyle,
    colorMaskStyle: ColorMaskStyle,
    bgColor=(255, 195, 235, 100),
):
    qr = QRCode(error_correction=ERROR_CORRECT_L)
    qr.add_data(data)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=moduleDrawer.value,
        color_mask=colorMaskStyle.value,
    )
    qrImage = img.get_image()
    modifiedImage = replaceWhite(qrImage, bgColor)
    return modifiedImage


def GetEnumNames(obj: Enum) -> list:
    return obj._member_names_


def GetAvailableDrawerStyles() -> list:
    return GetEnumNames(ModuleDrawerStyle)


def GetAvailableMaskStyles() -> list:
    return GetEnumNames(ColorMaskStyle)


def GetEnumValue(obj: Enum, name: str):
    return obj.__getitem__(name)


def GetDrawerStyle(name: str):
    return GetEnumValue(ModuleDrawerStyle, name)


def GetMaskStyle(name: str):
    return GetEnumValue(ColorMaskStyle, name)


def ParseConstants(constants: list) -> list:
    return [
        " ".join(
            [
                word[0].upper() + word[1:]
                for word in constant.replace("_", " ").lower().split(" ")
            ]
        )
        for constant in constants
    ]


def ReverseParseConstants(parsedConstants: list) -> list:
    return [
        "_".join([word.upper() for word in constant.split(" ")])
        for constant in parsedConstants
    ]

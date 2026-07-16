from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


# ============================================================
# ORTAK INPUT / OUTPUT SINIFLARI
# ============================================================

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class InputImageSecond(Input):
    name: Literal["inputImageSecond"] = "inputImageSecond"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Second Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Output Image"


class OutputScore(Output):
    name: Literal["outputScore"] = "outputScore"
    value: float
    type: Literal["number"] = "number"

    class Config:
        title = "Score"


# ============================================================
# 1. EXECUTOR: RotateImage  -> 1 input / 1 output
# ============================================================

# --- dependentDropdownlist: RotationMode -------------------
# Her iki option da KENDI ICINDE 2 farkli field tipine bagli:
#   - bir textInput (number)
#   - bir dropdownlist (bool/secim)
# Option 1 (Auto)   -> confidence (textInput) + smoothEdges (dropdownlist)
# Option 2 (Manual) -> angle (textInput)      + direction (dropdownlist)

class AutoConfidence(Config):
    name: Literal["AutoConfidence"] = "AutoConfidence"
    value: float = Field(ge=0.0, le=1.0, default=0.8)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Confidence"


class SmoothEdgesTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class SmoothEdgesFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class SmoothEdges(Config):
    name: Literal["SmoothEdges"] = "SmoothEdges"
    value: Union[SmoothEdgesTrue, SmoothEdgesFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Smooth Edges"


class ManualAngle(Config):
    name: Literal["ManualAngle"] = "ManualAngle"
    value: int = Field(ge=-359, le=359, default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Angle"


class DirectionClockwise(Config):
    name: Literal["Clockwise"] = "Clockwise"
    value: Literal["clockwise"] = "clockwise"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Clockwise"


class DirectionCounterClockwise(Config):
    name: Literal["CounterClockwise"] = "CounterClockwise"
    value: Literal["counterclockwise"] = "counterclockwise"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Counter Clockwise"


class ManualDirection(Config):
    name: Literal["ManualDirection"] = "ManualDirection"
    value: Union[DirectionClockwise, DirectionCounterClockwise]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Direction"


class RotationModeAuto(Config):
    """Bu option kendi icinde 2 farkli field tipi acar: textInput + dropdownlist."""
    name: Literal["RotationModeAuto"] = "RotationModeAuto"
    confidence: AutoConfidence
    smoothEdges: SmoothEdges
    value: Literal["auto"] = "auto"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Auto"


class RotationModeManual(Config):
    """Bu option kendi icinde 2 farkli field tipi acar: textInput + dropdownlist."""
    name: Literal["RotationModeManual"] = "RotationModeManual"
    angle: ManualAngle
    direction: ManualDirection
    value: Literal["manual"] = "manual"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Manual"


class RotationMode(Config):
    name: Literal["RotationMode"] = "RotationMode"
    value: Union[RotationModeAuto, RotationModeManual]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Rotation Mode"


class RotateImageInputs(Inputs):
    inputImage: InputImage


class RotateImageConfigs(Configs):
    rotationMode: RotationMode


class RotateImageOutputs(Outputs):
    outputImage: OutputImage


class RotateImageRequest(Request):
    inputs: Optional[RotateImageInputs]
    configs: RotateImageConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class RotateImageResponse(Response):
    outputs: RotateImageOutputs


class RotateImageExecutor(Config):
    name: Literal["RotateImage"] = "RotateImage"
    value: Union[RotateImageRequest, RotateImageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Rotate Image"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# ============================================================
# 2. EXECUTOR: MergeImages -> 2 input / 2 output
# ============================================================

# --- dependentDropdownlist: MergeMode -----------------------
# Her iki option da kendi icinde 2 farkli field tipine bagli:
#   - bir textInput (number)
#   - bir dropdownlist (bool/secim)
# Option 1 (Blend)      -> alpha (textInput)   + preserveAspect (dropdownlist)
# Option 2 (SideBySide) -> gap (textInput)     + order (dropdownlist)

class BlendAlpha(Config):
    name: Literal["BlendAlpha"] = "BlendAlpha"
    value: float = Field(ge=0.0, le=1.0, default=0.5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Blend Alpha"


class AspectRatioTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class AspectRatioFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class PreserveAspect(Config):
    name: Literal["PreserveAspect"] = "PreserveAspect"
    value: Union[AspectRatioTrue, AspectRatioFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Preserve Aspect Ratio"


class SideGap(Config):
    name: Literal["SideGap"] = "SideGap"
    value: int = Field(ge=0, le=200, default=10)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Gap (px)"


class OrderFirstImageFirst(Config):
    name: Literal["FirstImageFirst"] = "FirstImageFirst"
    value: Literal["first_first"] = "first_first"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "First Image Left"


class OrderSecondImageFirst(Config):
    name: Literal["SecondImageFirst"] = "SecondImageFirst"
    value: Literal["second_first"] = "second_first"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Second Image Left"


class SideOrder(Config):
    name: Literal["SideOrder"] = "SideOrder"
    value: Union[OrderFirstImageFirst, OrderSecondImageFirst]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Order"


class MergeModeBlend(Config):
    """Bu option kendi icinde 2 farkli field tipi acar: textInput + dropdownlist."""
    name: Literal["MergeModeBlend"] = "MergeModeBlend"
    alpha: BlendAlpha
    preserveAspect: PreserveAspect
    value: Literal["blend"] = "blend"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Blend"


class MergeModeSideBySide(Config):
    """Bu option kendi icinde 2 farkli field tipi acar: textInput + dropdownlist."""
    name: Literal["MergeModeSideBySide"] = "MergeModeSideBySide"
    gap: SideGap
    order: SideOrder
    value: Literal["side_by_side"] = "side_by_side"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Side by Side"


class MergeMode(Config):
    name: Literal["MergeMode"] = "MergeMode"
    value: Union[MergeModeBlend, MergeModeSideBySide]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Merge Mode"


class MergeImagesInputs(Inputs):
    inputImage: InputImage
    inputImageSecond: InputImageSecond


class MergeImagesConfigs(Configs):
    mergeMode: MergeMode


class MergeImagesOutputs(Outputs):
    outputImage: OutputImage
    outputScore: OutputScore


class MergeImagesRequest(Request):
    inputs: Optional[MergeImagesInputs]
    configs: MergeImagesConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class MergeImagesResponse(Response):
    outputs: MergeImagesOutputs


class MergeImagesExecutor(Config):
    name: Literal["MergeImages"] = "MergeImages"
    value: Union[MergeImagesRequest, MergeImagesResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Merge Images"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


# ============================================================
# EXECUTOR SECIMI VE PACKAGE MODEL
# ============================================================
# Birden fazla executor oldugu icin (kilavuz 2. bolum / Kod4) target belirtmeye
# gerek yok, kullanici Task alanindan hangi executoru kullanacagini secer.

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[RotateImageExecutor, MergeImagesExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage61"] = "DemoPackage61"

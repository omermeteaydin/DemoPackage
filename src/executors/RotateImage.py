"""
    Demo Executor 1: 1 input (inputImage), 1 output (outputImage).
    RotationMode dependentDropdown'una gore goruntuyu dondurur.
"""

import os
import sys
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackagee.src.utils.response import build_rotate_response
from components.DemoPackagee.src.models.PackageModel import PackageModel


class RotateImage(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")

        # RotationMode -> Auto veya Manual dalindan hangisi secildiyse
        # ilgili parametreler dolu, digerleri None gelir.
        self.manual_angle = self.request.get_param("ManualAngle")
        self.manual_direction = self.request.get_param("ManualDirection")
        self.auto_confidence = self.request.get_param("AutoConfidence")
        self.smooth_edges = self.request.get_param("SmoothEdges")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def _resolve_angle(self):
        if self.manual_angle is not None:
            angle = self.manual_angle
            if self.manual_direction == "counterclockwise":
                angle = -angle
            return angle
        # Auto modda: guven skoruna gore basit bir aci hesabi (demo amacli)
        confidence = self.auto_confidence or 0.0
        return confidence * 45

    def rotation(self, image):
        angle = self._resolve_angle()
        height, width = image.shape[:2]
        image_center = (width / 2, height / 2)
        rotation_arr = cv2.getRotationMatrix2D(image_center, angle, 1)

        if self.smooth_edges:
            abs_cos = abs(rotation_arr[0, 0])
            abs_sin = abs(rotation_arr[0, 1])
            bound_w = int(height * abs_sin + width * abs_cos)
            bound_h = int(height * abs_cos + width * abs_sin)
            rotation_arr[0, 2] += bound_w / 2 - image_center[0]
            rotation_arr[1, 2] += bound_h / 2 - image_center[1]
            return cv2.warpAffine(image, rotation_arr, (bound_w, bound_h))

        return cv2.warpAffine(image, rotation_arr, (width, height))

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.rotation(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        return build_rotate_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()


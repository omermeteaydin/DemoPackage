"""
    Demo Executor 2: 2 input (inputImage, inputImageSecond),
    2 output (outputImage, outputScore).
    MergeMode dependentDropdown'una gore iki gorseli birlestirir.
"""

import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackagee.src.utils.response import build_merge_response
from components.DemoPackagee.src.models.PackageModel import PackageModel


class MergeImages(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image_first = self.request.get_param("inputImage")
        self.image_second = self.request.get_param("inputImageSecond")

        # MergeMode -> Blend veya SideBySide dalindan hangisi secildiyse
        # ilgili parametreler dolu, digerleri None gelir.
        self.alpha = self.request.get_param("BlendAlpha")
        self.preserve_aspect = self.request.get_param("PreserveAspect")
        self.gap = self.request.get_param("SideGap")
        self.order = self.request.get_param("SideOrder")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def merge(self, img1, img2):
        if self.alpha is not None:
            h = min(img1.shape[0], img2.shape[0])
            w = min(img1.shape[1], img2.shape[1])
            img1_r = cv2.resize(img1, (w, h))
            img2_r = cv2.resize(img2, (w, h))
            merged = cv2.addWeighted(img1_r, self.alpha, img2_r, 1 - self.alpha, 0)
            score = float(self.alpha)
            return merged, score

        # Side by side modu
        h = max(img1.shape[0], img2.shape[0])
        img1_r = cv2.resize(img1, (int(img1.shape[1] * h / img1.shape[0]), h))
        img2_r = cv2.resize(img2, (int(img2.shape[1] * h / img2.shape[0]), h))
        gap = self.gap or 0
        gap_block = np.zeros((h, gap, 3), dtype=img1_r.dtype)

        if self.order == "second_first":
            merged = np.hstack([img2_r, gap_block, img1_r])
        else:
            merged = np.hstack([img1_r, gap_block, img2_r])

        score = 1.0
        return merged, score

    def run(self):
        img1 = Image.get_frame(img=self.image_first, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image_second, redis_db=self.redis_db)
        merged, score = self.merge(img1.value, img2.value)
        img1.value = merged
        self.image = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.score = score
        return build_merge_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()


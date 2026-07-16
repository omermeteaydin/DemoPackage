from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackage.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    RotateImageOutputs, RotateImageResponse, RotateImageExecutor, OutputImage,
    MergeImagesOutputs, MergeImagesResponse, MergeImagesExecutor, OutputScore,
)

# NOT: "components.DemoPackage" kismini, imajin icindeki gercek klasor
# adina (capsules/ ya da components/ altindaki paket adina) gore guncelle.


def build_rotate_response(context):
    outputImage = OutputImage(value=context.image)
    outputs = RotateImageOutputs(outputImage=outputImage)
    response = RotateImageResponse(outputs=outputs)
    executor = RotateImageExecutor(value=response)
    configExecutor = ConfigExecutor(value=executor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_merge_response(context):
    outputImage = OutputImage(value=context.image)
    outputScore = OutputScore(value=context.score)
    outputs = MergeImagesOutputs(outputImage=outputImage, outputScore=outputScore)
    response = MergeImagesResponse(outputs=outputs)
    executor = MergeImagesExecutor(value=response)
    configExecutor = ConfigExecutor(value=executor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel

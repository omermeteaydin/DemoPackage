# DemoPackage

Bu paket, `GNL - 03 Demo Package` Trello görevi için hazırlanmış, NovaVision altyapısı üzerinde
çalışan bir demo pakettir. İki farklı Executor ve bağımlı (dependent) konfigürasyon yeteneği içerir.

## 🚀 Özellikler ve Kurallar

### 1. İşlem Birimleri (Executors)

* **RotateImage:** Tek bir görsel girişi (`inputImage`) alır, `RotationMode` ayarına göre görseli
  döndürür ve tek bir görsel çıktısı (`outputImage`) üretir.
* **MergeImages:** İki görsel girişi (`inputImage`, `inputImageSecond`) alır, `MergeMode` ayarına
  göre görselleri birleştirir ve iki farklı çıktı üretir: birleşmiş görsel (`outputImage`) ile
  bir benzerlik/karışım skoru (`outputScore`).

### 2. Dinamik Yapılandırma (Dynamic Configuration)

* Her iki Executor'ın config'inde de bir `dependentDropdownlist` (`RotationMode` / `MergeMode`)
  bulunur.
* Kullanıcı seçtiği opsiyona göre (`Auto`/`Manual`, `Blend`/`SideBySide`) farklı giriş alanları
  arasında dinamik geçiş yapar.
* Her bir dropdown opsiyonu kendi içinde **2 farklı tipte alana** bağlıdır:
  * `RotationMode` → `Auto`: `Confidence` (**textInput**) + `SmoothEdges` (**dropdownlist**)
  * `RotationMode` → `Manual`: `Angle` (**textInput**) + `Direction` (**dropdownlist**)
  * `MergeMode` → `Blend`: `Alpha` (**textInput**) + `PreserveAspect` (**dropdownlist**)
  * `MergeMode` → `SideBySide`: `Gap` (**textInput**) + `Order` (**dropdownlist**)

## ✅ Kontrol Listesi Karşılığı

- [x] En az 2 Executor
- [x] 1. Executor: 1 input, 1 output
- [x] 2. Executor: 2 input, 2 output
- [x] Her iki Executor'ın config'inde en az 1 `dependentDropdownlist`, en az 2 opsiyon
- [x] Her opsiyon 2 farklı field tipine (textInput + dropdownlist) bağlı

## Proje Yapısı

```
src/
  executors/       RotateImage.py, MergeImages.py
  models/          PackageModel.py (Pydantic model tanımları)
  utils/           response.py (response builder fonksiyonları)
setup.py
LICENSE
.gitignore
```

## Kurulum

Bu paket, NovaVision `image` yapısı içindeki `capsules/` veya `components/` klasörüne
klonlanarak kullanılır (bkz. Package Geliştirici Kılavuzu, Bölüm 1.2).

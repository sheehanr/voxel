# Voxel: Own Your Scans

A patient-centric, HIPAA-compliant iOS app for viewing medical imaging. Features a secure, offline AI to simplify radiology reports on-device.

*Disclaimer: This app is intended for informational purposes only and does not provide medical advice or diagnoses. Additionally, AI can make mistakes. Always consult a qualified healthcare provider with any questions or concerns. This app is not intended for self-diagnosis or self-treatment and reliance on any information provided by the app is solely at your own risk.*

---

## Demo & Link (Placeholders)

**[View Voxel on the App Store (placeholder)](https://www.apple.com/app-store/)**

![GIF of _____ on Voxel (placeholder)](screenshots/app1.gif)

![GIF of _____ on Voxel (placeholder)](screenshots/app2.gif)

![Screenshot of _____ on Voxel (placeholder)](screenshots/app3.png)

![Screenshot of _____ on Voxel (placeholder)](screenshots/app4.png)

![Screenshot of _____ on Voxel (placeholder)](screenshots/app5.png)

---

## Personal Context

Since my cancer diagnosis, I have undergone countless imaging studies, sparking a deep personal interest in radiology. I wanted to analyze my scans outside the doctor's office, but faced significant barriers. The images were DICOM files, which required antiquated software designed for doctors, not patients. Additionally, the reports were full of medical terminology that was impossible to decipher without a medical background.

I realized there was no solution built with the patient in mind. Something that would allow patients like myself to:
* store scans and reports in one place regardless of provider,
* view scans and compare them side-by-side to track changes, and
* understand radiology reports using a local LLM.

Voxel is my answer: a native iOS application designed to enable patients to access their medical scans. *Securely, privately, and intuitively.*

---

## Key Features (Projected)

* **Automatic Sorting:** Developed *ScanSort,* an automated sorting system for uploaded imaging and radiology reports, classifying them by type of scan (modality) and anatomical region using a fine-tuned Convolutional Neural Network **(CNN)** and Natural Language Processing **(NLP)** Transformer.
* **Imaging Viewer:** Built a comprehensive imaging viewer capable of displaying 2D (X-Rays) and 3D (MRI, CT) imaging slices with native support for the DICOM (.dcm) file format.
  * **Comparison Tool:** Engineered a feature allowing for side-by-side observation of imaging studies to view changes over time.
  * **Linked Scrolling *(optional)*:** Implemented a feature enabling CT scans with multiple planes to be viewed and navigated concurrently.
  * **Longitudinal Image Registration *(optional)*:** Leveraged AI to automatically and intelligently highlight changes in medical scans over time.
* **Radiology Assistant:** Created *VoxeLLM,* an AI-powered assistant that simplifies complex radiology reports into patient-friendly language and allows for follow-up questions.
  * **Report-to-Image Linking:** Harnessed AI to highlight and link to locations mentioned in the radiology report (e.g. "slice 42" or "upper right lobe").
* **HIPAA-Compliant:** Established a HIPAA-compliant architecture incorporating local Large Language Model **(LLM)** processing, on-device storage, and biometric authentication (Touch ID/Face ID) to ensure patient privacy.
* **User Friendly UI/UX:** Designed a patient-centric **UI/UX**, emphasizing intuitive navigation and a visually engaging, responsive interface consistent with Apple design language.

---

## Model Engineering (Projected)

### 1. ScanSort (Automatic Sorting)

**Goal:** Classify medical imaging files by modality and anatomical region with >95% accuracy, with graceful handling of unrecognized imaging.

* **Base Model:** _____
* **Training:** Transfer learning on XX,XXX+ imaging studies using PyTorch (accelerated by RTX 5080).
* **Target Classes *(incomplete)*:** Classifies the following XX specific clinical views:
  * **CT:** Brain, Chest
  * **MRI:** Brain, Knee, Spine
  * **X-Ray:** Chest, Elbow, Femur, Forearm, Hand, Humerus, Knee, Shoulder, Wrist

### 2. VoxeLLM (Radiology Assistant)

**Goal:** Summarize radiology reports and be able to answer medical queries related to the report while maximizing accuracy and minimizing hallucinations. 

* **Base Model:** _____
* **Training:** _____ fine-tuning on radiology report and medical datasets.
* **Optimization:** _____ quantization to reduce memory usage to <XGB.
* **Deployment:** Converted to CoreML format to utilize Apple Neural Engine (ANE) for offline inference.

* *See "Training Data & Acknowledgements" below to see all datasets used in training.*

---

## Tech Stack (Projected)

* **Languages:** Swift 6.2.3, Python 3.12
* **iOS Frameworks:** SwiftUI, CoreML
* **Python Libraries:** PyTorch, TorchVision, OpenCV, CoreMLTools, Pydicom
* **Hardware:** NVIDIA RTX 5080 (Training)
* **Tools:** Xcode 26.2

---

## Training Data & Acknowledgements (Projected)

### 1. ScanSort (Automatic Sorting)

To train the model for ScanSort, all imaging study datasets were sourced from [Kaggle](https://www.kaggle.com). 

* **[Brain Stroke CT Dataset](https://www.kaggle.com/datasets/ozguraslank/brain-stroke-ct-dataset)** by Ozgur Aslan
  * Used for: CT Brain
  * Original Source: Republic of Türkiye Ministry of Health
  * Citation: Koç U, Akçapınar Sezer E, Alper Özkaya Y, et al. Artificial intelligence in healthcare competition (TEKNOFEST-2021): Stroke data set. Eurasian J Med., 2022;54(3):248-258.
  * License: Unknown

* **[CT Medical Images](https://www.kaggle.com/datasets/kmader/siim-medical-images)** by K Scott Mader
  * Used for: CT Chest
  * Original Source: The Cancer Imaging Archive (TCIA)
  * Data Citation: Albertina, B., Watson, M., Holback, C., Jarosz, R., Kirk, S., Lee, Y., … Lemmerman, J. (2016). Radiology Data from The Cancer Genome Atlas Lung Adenocarcinoma [TCGA-LUAD] collection. The Cancer Imaging Archive. http://doi.org/10.7937/K9/TCIA.2016.JGNIHEP5
  * TCIA Citation: Clark K, Vendt B, Smith K, Freymann J, Kirby J, Koppel P, Moore S, Phillips S, Maffitt D, Pringle M, Tarbox L, Prior F. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository, Journal of Digital Imaging, Volume 26, Number 6, December, 2013, pp 1045-1057. (paper)
  * License: [CC BY 3.0](http://creativecommons.org/licenses/by/3.0/)

* **[Chest CT-Scan images Dataset](https://www.kaggle.com/datasets/mohamedhanyyy/chest-ctscan-images)** by Mohamed Hany
  * Used for: CT Chest
  * Original Source: Unknown
  * License: [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)
  
* **[IQ-OTH/NCCD - Lung Cancer Dataset](https://www.kaggle.com/datasets/adityamahimkar/iqothnccd-lung-cancer-dataset)** by Aditya Mahimkar
  * Used for: CT Chest
  * Original Source: Mendeley Data from Iraq-Oncology Teaching Hospital/National Center for Cancer Diseases (IQ-OTH/NCCD)
  * Citation: Alyasriy, Hamdalla; AL-Huseiny, Muayed (2021), “The IQ-OTHNCCD lung cancer dataset”, Mendeley Data, V2, doi: 10.17632/bhmdr45bh2.2
  * License: Copyright Original Authors

* **[Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)** by Masoud Nickparvar
  * Used for: MRI Brain
  * Original Sources: 
    1. [Figshare](https://figshare.com/articles/dataset/brain_tumor_dataset/1512427)
    2. [Brain Tumor Classification (MRI)](https://www.kaggle.com/sartajbhuvaji/brain-tumor-classification-mri/metadata) by Sartaj on Kaggle
    2. [Br35H :: Brain Tumor Detection 2020](https://www.kaggle.com/datasets/ahmedhamada0/brain-tumor-detection/metadata) by Ahmed Hamada on Kaggle
  * License: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)

* **[MRNet v1](https://www.kaggle.com/datasets/cjinny/mrnet-v1)** by Jincui
  * Used for: MRI Knee
  * Original Source: Stanford Center for Artificial Intelligence in Medicine & Imaging (AIMI)
  * Citation: [MRNet: Knee MRI's](https://doi.org/10.71718/rcbp-8c35)
  * License: Unknown

* **[RSNA 2024 Lumbar Spine Degenerative Classification](https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification)** by Radiological Society of North America
  * Used for: MRI Spine
  * Original Source: Radiological Society of North America (RSNA)
  * Citation: Tyler Richards, Jason Talbott, Robyn Ball, Errol Colak, Adam Flanders, Felipe Kitamura, John Mongan, Luciano Prevedello, and Maryam Vazirabad.. RSNA 2024 Lumbar Spine Degenerative Classification. https://kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification, 2024. Kaggle.
  * License: Unknown

* **[NIH Chest X-rays](https://www.kaggle.com/datasets/nih-chest-xrays/data)** by National Institutes of Health Chest X-Ray Dataset
  * Used for: X-Ray Chest
  * Original Source: National Institutes of Health (NIH)
  * Citation: Wang X, Peng Y, Lu L, Lu Z, Bagheri M, Summers RM. ChestX-ray8: Hospital-scale Chest X-ray Database and Benchmarks on Weakly-Supervised Classification and Localization of Common Thorax Diseases. IEEE CVPR 2017
  * License: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)

* **[mura v11](https://www.kaggle.com/datasets/cjinny/mura-v11)** by Jincui
  * Used for: X-Ray Elbow, X-Ray Finger, X-Ray Forearm, X-Ray Hand, X-Ray Humerus, X-Ray Shoulder, X-Ray Wrist
  * Original Source: Stanford Center for Artificial Intelligence in Medicine & Imaging (AIMI)
  * Citation: [MURA: MSK Xrays](https://doi.org/10.71718/cwh3-0p32)
  * License: Unknown

* **[The UNIFESP X-Ray Body Part Classification Dataset](https://www.kaggle.com/datasets/felipekitamura/unifesp-xray-bodypart-classification)** by FelipeKitamura, MD, PhD & Eduardo Farina
  * Used for: X-Ray Abdomen, X-Ray Ankle, X-Ray Cervical Spine, X-Ray Chest, X-Ray Clavicles, X-Ray Elbow, X-Ray Feet, X-Ray Finger, X-Ray Forearm, X-Ray Hand, X-Ray Hip, X-Ray Knee, X-Ray Lower Leg, X-Ray Lumbar Spine, X-Ray Others, X-Ray Pelvis, X-Ray Shoulder, X-Ray Sinus, X-Ray Skull, X-Ray Thigh, X-Ray Thoracic Spine, X-Ray Wrist
  * Original Source: Universidade Federal de São Paulo (UNIFESP)
  * Citation: Eduardo Moreno Judice de Mattos Farina, Nitamar Abdala, and Felipe Campos Kitamura. (2022). The UNIFESP X-Ray Body Part Classification Dataset [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/3399135
  * License: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

* **[Digital Knee X-ray Images](https://www.kaggle.com/datasets/orvile/digital-knee-x-ray-images)** by Orvile
  * Used for: X-Ray Knee
  * Original Source: Mendeley Data
  * Citation: Gornale, Shivanand; Patravali, Pooja (2020), Digital Knee X-ray Images, Mendeley Data, V1, https://doi.org/10.17632/t9ndx37v5h.1
  * License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

* **[Heel Dataset](https://www.kaggle.com/datasets/osamahtaher/heel-dataset)** by Osamah Taher
  * Used for: X-Ray Heel
  * Original Source: Kirkuk General Hospital
  * Citation: Taher, Osamah, and Kasım Özacar. "HeCapsNet: An enhanced capsule network for automated heel disease diagnosis using lateral foot X‐Ray images." International Journal of Imaging Systems and Technology 34.3 (2024): e23084.
  * License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

### 2. VoxeLLM (Radiology Assistant)

To train the model for VoxeLLM, 

---

## Requirements (Placeholders)

* **iOS Development:** Swift X.X.X, Xcode XX.X
* **Model Engineering:** Python X.X, *see `requirements.txt` for list of Python libraries*
  * *Note: Discrete NVIDIA GPU is recommended to improve training times.*
* **Device and Software Version:** Apple iPhone XX or higher running iOS XX.X.X or higher. 
  * *Note: Apple iPhone XX or higher is recommended to use AI features due to RAM limitations.*
  * *Note: Apple iPhone XX or higher is required for biometric authentication.*

---

## License

Distributed under the MIT License. See `LICENSE.txt` for more information. 

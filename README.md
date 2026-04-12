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

## Key Features

### Clinical-Grade Imaging Viewer
View X-rays, MRIs, and CT scans directly on your device.
* **Versatile Viewing**: Easily open and view both medical DICOM files and standard image formats.
* **Side-by-Side Comparison:** Open two different scans at once to see changes over time.
* **Synchronized Scrolling:** Navigate through MRIs and CT scans smoothly across all angles to get a complete view.

### Privacy-Focused Design
Your sensitive health information never leaves your device.
* **On-Device Storage:** All files and processing stay on your phone or computer, not in the cloud.
* **Biometric Lock:** Secure your records with **Face ID** or **Touch ID** so only you can access them.

### Smart Library Organization
The app automatically categorizes and labels your medical files to eliminate manual sorting.
* **Automatic Sorting:** Scans are instantly identified and grouped by body part and scan type.
* **Fast Search:** Find specific results or dates in seconds using the built-in intelligent search.

### VoxeLLM: Your Personal Health Assistant
Understand your radiology reports without the medical jargon.
* **Report Simplification:** Converts complex clinical language into plain, easy-to-understand English.
* **Interactive Q&A:** Ask follow-up questions about your findings and get instant, clear explanations.

---

## Personal Context

Since my cancer diagnosis, I have undergone countless imaging studies, sparking a deep personal interest in radiology. I wanted to analyze my scans outside the doctor's office, but faced significant barriers. The images were DICOM files, which required antiquated software designed for doctors, not patients. Additionally, the reports were full of medical terminology that was impossible to decipher without a medical background.

I realized there was no solution built with the patient in mind. Something that would allow patients like myself to:
* store scans and reports in one place regardless of provider,
* view scans and compare them side-by-side to track changes, and
* understand radiology reports using a local LLM.

Voxel is my answer: a native iOS application designed to enable patients to access their medical scans. *Securely, privately, and intuitively.*

---

## Model Engineering (Projected)

### 1. ScanSort (Automatic Sorting)

**Goal:** Classify medical imaging files by modality and anatomical region with >95% accuracy, with graceful handling of unrecognized imaging.

* **Base Model:** _____
* **Training:** Transfer learning on X+ imaging studies using PyTorch.
  * *Achieved a X% reduction in training time by using RTX 5080 (compared to _____).* 
* **Data Balancing:** Undersampled large datasets at 5,000 images and applied weighted loss techniques to smaller datasets.
* **Target Classes *(incomplete)*:** Classifies the following 19 specific clinical views:
  * **X-Ray:** Ankle, Chest, Elbow, Finger, Foot, Forearm, Hand, Hip, Humerus, Knee, Shoulder, Wrist, Other

### 2. VoxeLLM (Radiology Report Chatbot)

**Goal:** Summarize radiology reports and be able to answer medical queries related to the report while maximizing accuracy and minimizing hallucinations. 

* **Base Model:** _____
* **Training:** _____ fine-tuning on radiology report and medical datasets.
  * *Achieved a X% reduction in training time by using RTX 5080 (compared to _____).* 
* **Optimization:** _____ quantization to reduce memory usage by X% (from XGB to <XGB).
* **Deployment:** Converted to CoreML format to utilize Apple Neural Engine (ANE) for offline inference.

* *See "Training Data & Acknowledgements" below to see all datasets used in training.*

---

## Tech Stack (Projected)

* **Languages:** Swift 6.2.3, Python 3.12
* **iOS Frameworks:** SwiftUI, CoreML
* **Python Libraries:** Kaggle, NumPy, Pandas, Pillow, PyDicom, TQDM
* **Hardware:** NVIDIA RTX 5080 (Training)
* **Tools:** Xcode 26.2

---

## Requirements (Placeholders)

* **iOS Development:** Swift X.X.X, Xcode XX.X
* **Model Engineering:** Python X.X, *see `pyproject.toml` for list of Python libraries*
  * *Note: Discrete NVIDIA GPU is recommended to improve training times.*
* **Device and Software Version:** Apple iPhone XX or higher running iOS XX.X.X or higher. 
  * *Note: Apple iPhone XX or higher is recommended to use AI features due to RAM limitations.*
  * *Note: Apple iPhone XX or higher is required for biometric authentication.*

---

## Training Data & Acknowledgements (Projected)

### 1. ScanSort (Automatic Sorting)

To train the model for ScanSort, all imaging study datasets were sourced from [Kaggle](https://www.kaggle.com). 

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

* **[Multi-Class Knee Osteoporosis X-Ray Dataset](https://www.kaggle.com/datasets/mohamedgobara/multi-class-knee-osteoporosis-x-ray-dataset)** by Mohamed Gobara
  * Used for: X-Ray Knee
  * Original Source: Knee Osteoporosis Diagnosis Based on Deep Learning
  * Citation: Sarhan, A.M., Gobara, M., Yasser, S. et al. Knee Osteoporosis Diagnosis Based on Deep Learning. Int J Comput Intell Syst 17, 241 (2024). https://doi.org/10.1007/s44196-024-00615-4
  * License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

* **[Heel Dataset](https://www.kaggle.com/datasets/osamahtaher/heel-dataset)** by Osamah Taher
  * Used for: X-Ray Heel
  * Original Source: Kirkuk General Hospital
  * Citation: Taher, Osamah, and Kasım Özacar. "HeCapsNet: An enhanced capsule network for automated heel disease diagnosis using lateral foot X‐Ray images." International Journal of Imaging Systems and Technology 34.3 (2024): e23084.
  * License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

### 2. VoxeLLM (Radiology Assistant)

To train the model for VoxeLLM, 

---

## License

Distributed under the MIT License. See `LICENSE.txt` for more information. 

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

*

---

## Tech Stack (Projected)

* **Languages:** Swift 6.2.3, Python 3.12
* **iOS Frameworks:** SwiftUI, CoreML
* **Python Libraries:** PyTorch, TorchVision, OpenCV, CoreMLTools, Pydicom
* **Hardware:** NVIDIA RTX 5080 (Training)
* **Tools:** Xcode 26.2

---

## Training Data & Acknowledgements (Projected)

* 

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

--- 

## Contact

Sheehan Rahman -- [Email](mailto:sheehanrahman06@gmail.com) -- [LinkedIn Profile](https://linkedin.com/in/sheehan-rahman)

[Project Link](https://github.com/sheehanr/voxel)

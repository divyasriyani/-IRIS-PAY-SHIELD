🔴 Cite This Notebook 🔴
If you find this notebook useful in your research or projects, please consider citing it. Proper citation helps me gain recognition for my work and allows others to follow and build upon it.

Iris eye Recognition
An (End-to-end segmentation-free approach) Iris Biometric Authentication
add Codeadd Markdown
Abstract
In this project, a Biometric Authentication system using the Iris biometric authentication method is designed. The approach taken is using the CASIA-Thousand-IRIS dataset and model it using the Deep Convultional Neural Network Architicture, with the minimum image-preprocessing such as resizing with keeping the aspect ratiio and normalization. It is an end-to-end technique without performing segmentaion of the IRIS itself. The results are promising, even without perfroing training on augmentation, the testing accuracy has reached (93.15%). Finally, for the proof of the (biometric authentication system concept) a simple mobile application is designed and the model is deployed on it (IrisRecognizer) as it was exported to it's liter version were default quantization is performed.

add Codeadd Markdown
Table of Contents
Introduction
Aim and Objectives
Methodology
Theory
About Dataset Used
Deep Learning for Image Recognition
Software Listing
Implementation
Dataset Analysis
Loading dataset
Exploring dataset (vidualization, distributions)
Preparing dataset (images, labels, spliting)
experimnt with Augemntaion
Data Modeling (The verifier)
Model Architicture
Traing and Testing
Model Performance (Loss and accuracy)
Testing and saving weights
Evaluation Metrics
Model Exporting
GUI (The authenticator)
First time users, and prefrences
Image accqusition
Image preparing for recognition
Model Inference
Discussion and optimization
Conclusion
Refrences
List of Figures
Figure 1: IRis dataset collection device IKEMB-100 camera
Figure 2: Figure: Data Sample from IRIS CaSIA
Figure 3: Ramndom Small sample of the dataset
Figure 4: Image 50 person label ..
Figure 5: Distribution of Image Sizes
Figure 6: Distribution of Aspect Ratios
Figure 7: Labels Frequency Treemap
Figure 8: Preprocessed image sample
Figure 9: Augmented image sample
Figure 10: Model accurac
Figure 11: Loss Learning Curve
Figure 12: Prefrences
Figure 13: Image acusition
Figure 14: Model Answer
List of Tables
Table 1: Software Listenings
Table 2: Dataset Head
Table 3: Dataset Tail
Table 4: Dataset Numerical Describtion
Table 5: Missing Values By Percentage
Table 6: Dataset Columns Data types
Table 7: Number of uniques in the datasets
Table 8: Labels Distribution
add Codeadd Markdown
Introduction
The science of Cybersecurity has become essential and irreparable in modern life. With the rise of information technology, the fragility and vulnerability also increases. One of the aspects that cybersecurity addresses is the sophisticated kinds of cybercrime and cyberespionage activities, as well as cyber-terror and cyberwar. Another aspect that cybersecurity addresses is Controlling Access for computer resources, with a known framework called: the triple A’s (AAA) [1] it stands for Authentication, Authorization, and Accounting. This report is concerned with the first A: the Authentication part. Simply put, Authentication is when the user provides information to the system that affirm they are who they claim to be. There are three main types of authentication:

Something you know, like a password.
Something you have, like a Universal Serial Bus (USB) key.
Something you are, such as fingerprint or other biometrics.

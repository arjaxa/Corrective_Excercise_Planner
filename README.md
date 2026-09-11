# Corrective Exercise Planner

A rule-based corrective exercise planning app that creates 4-week exercise plans based on selected postural issues.

The project has two ways to identify the issue:

* **Manual Selection** — choose a posture issue directly.
* **Computer Vision Screening** — upload a posture image and use an experimental image classifier to screen for normal posture vs. possible postural deviation. The suspected issue is then selected manually.

The selected posture issue is matched with a small exercise knowledge base containing exercises categorized as release, stretch, activation, and integration. The planner then creates a structured plan for Weeks 1–2 and Weeks 3–4 using predefined exercise-selection and prescription rules.

## Posture Issues

Currently supported:

* Forward Head Posture
* Upper Crossed Syndrome
* Lower Crossed Syndrome

## How It Works

```text
Posture Assessment
        ↓
Manual Selection / CV Screening
        ↓
Posture Issue
        ↓
Exercise Knowledge Base
        ↓
Rule-Based Exercise Selection
        ↓
4-Week Corrective Exercise Plan
```

### Weeks 1–2

Focuses on:

* Release
* Stretch
* Activation

### Weeks 3–4

Focuses on:

* Stretch
* Activation
* Integration

The plan also includes exercise sets, repetitions or hold times, tempo, rest periods, and weekly frequency.

## Computer Vision Model

The computer vision component uses **MobileNetV2 with transfer learning**.

Because the available posture image dataset is small, the current model is treated as an **experimental screening prototype** rather than a reliable posture classifier. It currently performs binary screening:

```text
Normal
   or
Possible Postural Deviation
```

When a deviation is detected, the user manually selects the suspected posture issue.

## Tech Stack

* Python
* Streamlit
* TensorFlow / Keras
* MobileNetV2
* NumPy
* Pillow
* Scikit-learn

## Project Structure

```text
Corrective_Excercise_Planner/
│
├── data/
│   ├── exercises.json
│   └── posture_issues.json
│
├── models/
│   └── binary_posture_classifier.keras
│
├── src/
│   ├── app.py
│   ├── planner.py
│   ├── prescription.py
│   ├── exercise_selector.py
│   ├── posture_rules.py
│   ├── train_binary_posture_model.py
│   └── ...
│
└── requirements.txt
```

## Limitations

The main limitation of the current project is the size and diversity of the posture image dataset. Because of this, the computer vision component should not be considered a reliable diagnostic system.

The rule-based planner is the main functional part of the application, while the computer vision component is an experimental addition.

## Future Improvements

Possible improvements include:

* Expanding the posture image dataset
* Adding more subjects, environments, and viewpoints
* Improving and retraining the posture classifier
* Increasing the number of detectable posture conditions
* Improving the integration between computer vision screening and exercise planning

## Disclaimer

This project is an educational and portfolio prototype. The computer vision screening is experimental and is not intended to provide medical diagnosis or replace professional assessment.

## Live Demo

[Streamlit App](https://pcp-planner.streamlit.app/)

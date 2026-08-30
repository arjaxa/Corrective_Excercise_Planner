import json
import random
from pathlib import Path

from prescription import get_week_prescription


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

POSTURE_FILE = DATA_DIR / "posture_issues.json"
EXERCISE_FILE = DATA_DIR / "exercises.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_data():
    posture_issues = load_json(POSTURE_FILE)
    exercises = load_json(EXERCISE_FILE)

    return posture_issues, exercises


def find_exercises(
    exercises,
    muscles=None,
    category=None,
    used_ids=None
):
    """Return exercises matching the requested filters."""

    if used_ids is None:
        used_ids = set()

    matches = []

    for exercise in exercises:

        if exercise.get("id") in used_ids:
            continue

        if category is not None:
            if exercise.get("category") != category:
                continue

        if muscles is not None:
            if exercise.get("target_muscle") not in muscles:
                continue

        matches.append(exercise)

    return matches


def select_one_per_muscle(
    exercises,
    muscles,
    category,
    used_ids
):
    """
    Select one unique exercise for each requested muscle.

    Used for:
        release
        stretch
        activation
    """

    selected = []

    for muscle in muscles:

        candidates = find_exercises(
            exercises=exercises,
            muscles=[muscle],
            category=category,
            used_ids=used_ids
        )

        if not candidates:
            continue

        exercise = random.choice(candidates)

        selected.append(exercise)
        used_ids.add(exercise["id"])

    return selected



def select_integrations(
    exercises,
    underactive_muscles,
    overactive_muscles,
    used_ids,
    number=3
):
    """
    Select diverse compound integration exercises.

    Priority:
        1. Relevance to underactive muscles
        2. Relevance to overactive muscles
        3. Different target muscles
        4. Unique exercises
    """

    candidates = find_exercises(
        exercises=exercises,
        category="integration",
        used_ids=used_ids
    )

    if not candidates:
        return []

    scored = []

    for exercise in candidates:

        target = exercise.get("target_muscle")

        score = 0

        if target in underactive_muscles:
            score += 3
        if target in overactive_muscles:
            score += 1

        scored.append(
            (score, random.random(), exercise)
        )

    scored.sort(
        key=lambda item: (item[0], item[1]),
        reverse=True
    )

    selected = []

    
    selected_targets = set()

    for _, _, exercise in scored:

        if len(selected) >= number:
            break

        target = exercise.get("target_muscle")

        if target in selected_targets:
            continue

        selected.append(exercise)
        selected_targets.add(target)
        used_ids.add(exercise["id"])


    if len(selected) < number:

        for _, _, exercise in scored:

            if len(selected) >= number:
                break

            if exercise["id"] in used_ids:
                continue

            selected.append(exercise)
            used_ids.add(exercise["id"])

    return selected



def add_prescription(exercises, phase):
    """
    Attach phase-specific prescription information.
    """

    planned = []

    for exercise in exercises:

        exercise_copy = exercise.copy()

        prescription = get_week_prescription(
            category=exercise_copy.get("category", ""),
            phase=phase,
            exercise=exercise_copy
        )

        if prescription is None:
            continue

        exercise_copy["prescription"] = prescription

        planned.append(exercise_copy)

    return planned



def generate_plan(posture_id):
    """
    Generate the complete 4-week corrective exercise plan.

    Weeks 1–2:
        Release
        Stretch
        Activation

    Weeks 3–4:
        Stretch
        Activation
        Integration
    """

    posture_issues, exercises = load_data()

    if posture_id not in posture_issues:
        raise ValueError(
            f"Unknown posture issue: {posture_id}"
        )

    posture = posture_issues[posture_id]

    overactive = posture.get(
        "overactive_muscles",
        []
    )

    underactive = posture.get(
        "underactive_muscles",
        []
    )


    used_ids = set()

    release = select_one_per_muscle(
        exercises=exercises,
        muscles=overactive,
        category="release",
        used_ids=used_ids
    )


    stretch = select_one_per_muscle(
        exercises=exercises,
        muscles=overactive,
        category="stretch",
        used_ids=used_ids
    )


    activation = select_one_per_muscle(
        exercises=exercises,
        muscles=underactive,
        category="activation",
        used_ids=used_ids
    )


    integration = select_integrations(
        exercises=exercises,
        underactive_muscles=underactive,
        overactive_muscles=overactive,
        used_ids=used_ids,
        number=3
    )


    weeks_1_2 = {

        "release": add_prescription(
            release,
            "weeks_1_2"
        ),

        "stretch": add_prescription(
            stretch,
            "weeks_1_2"
        ),

        "activation": add_prescription(
            activation,
            "weeks_1_2"
        ),

        "integration": []
    }


    weeks_3_4 = {

        "release": [],

        "stretch": add_prescription(
            stretch,
            "weeks_3_4"
        ),

        "activation": add_prescription(
            activation,
            "weeks_3_4"
        ),

        "integration": add_prescription(
            integration,
            "weeks_3_4"
        )
    }


    return {
        "posture_id": posture_id,
        "posture_name": posture.get("name"),

        "overactive_muscles": overactive,
        "underactive_muscles": underactive,

        "weeks_1_2": weeks_1_2,
        "weeks_3_4": weeks_3_4
    }



def print_section(title, exercises):
    print(f"\n--- {title.upper()} ---")

    for exercise in exercises:

        print(
            f"- {exercise['name']} "
            f"({exercise['target_muscle']})"
        )

        print(
            f"  {exercise['prescription']['display']}"
        )


def print_phase(title, phase):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print_section(
        "Release",
        phase["release"]
    )

    print_section(
        "Stretch",
        phase["stretch"]
    )

    print_section(
        "Activation",
        phase["activation"]
    )

    print_section(
        "Integration",
        phase["integration"]
    )


def print_plan(plan):

    print("=" * 60)
    print("CORRECTIVE EXERCISE PLAN")
    print("=" * 60)

    print(
        f"\nPosture: {plan['posture_name']}"
    )

    print("\nOveractive muscles:")

    for muscle in plan["overactive_muscles"]:
        print(f"  - {muscle}")

    print("\nUnderactive muscles:")

    for muscle in plan["underactive_muscles"]:
        print(f"  - {muscle}")

    print_phase(
        "WEEKS 1–2",
        plan["weeks_1_2"]
    )

    print_phase(
        "WEEKS 3–4",
        plan["weeks_3_4"]
    )


if __name__ == "__main__":

    plan = generate_plan(
        "forward_head"
    )

    print_plan(plan)
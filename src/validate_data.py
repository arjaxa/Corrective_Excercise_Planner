import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

POSTURE_FILE = ROOT / "data" / "posture_issues.json"
EXERCISE_FILE = ROOT / "data" / "exercises.json"


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {path}")
        print(f"   Line {e.lineno}, column {e.colno}: {e.msg}")
        return None


def validate():

    print("=" * 60)
    print("CORRECTIVE EXERCISE PLANNER - DATA VALIDATION")
    print("=" * 60)

    posture_data = load_json(POSTURE_FILE)
    exercise_data = load_json(EXERCISE_FILE)

    if posture_data is None or exercise_data is None:
        return

    print("\nJSON files loaded successfully.")


    print("\n--- POSTURE ISSUES ---")

    posture_muscles = set()

    for posture_id, posture in posture_data.items():

        required_fields = [
            "name",
            "overactive_muscles",
            "underactive_muscles"
        ]

        for field in required_fields:
            if field not in posture:
                print(f"{posture_id}: missing '{field}'")

        for muscle in posture.get("overactive_muscles", []):
            posture_muscles.add(muscle)

        for muscle in posture.get("underactive_muscles", []):
            posture_muscles.add(muscle)

    print(f"Posture issues found: {len(posture_data)}")
    print(f"Unique muscles referenced: {len(posture_muscles)}")


    print("\n--- EXERCISES ---")

    required_fields = [
        "id",
        "name",
        "category",
        "target_muscle",
        "target_role",
        "equipment",
        "has_hold",
        "hold_options_seconds",
        "rep_options",
        "set_options",
        "tempo",
        "difficulty",
        "instructions"
    ]

    valid_categories = {
        "release",
        "stretch",
        "activation",
        "integration"
    }

    valid_roles = {
        "overactive",
        "underactive"
    }

    exercise_ids = set()

    errors = 0

    category_counts = {}
    muscle_counts = {}


    for index, exercise in enumerate(exercise_data, start=1):

        name = exercise.get("name", f"Exercise #{index}")
        exercise_id = exercise.get("id")

        for field in required_fields:

            if field not in exercise:
                print(
                    f"{name}: missing '{field}'"
                )
                errors += 1

        if exercise_id in exercise_ids:

            print(
                f"Duplicate exercise ID: "
                f"{exercise_id}"
            )

            errors += 1

        exercise_ids.add(exercise_id)


        category = exercise.get("category")

        if category not in valid_categories:

            print(
                f"{name}: invalid category "
                f"'{category}'"
            )

            errors += 1

        category_counts[category] = (
            category_counts.get(category, 0) + 1
        )

        role = exercise.get("target_role")

        if role not in valid_roles:

            print(
                f"{name}: invalid target_role "
                f"'{role}'"
            )

            errors += 1


        muscle = exercise.get("target_muscle")

        if muscle not in posture_muscles:

            print(
                f"{name}: target muscle "
                f"'{muscle}' is not used by "
                f"any posture issue"
            )

            errors += 1

        muscle_counts[muscle] = (
            muscle_counts.get(muscle, 0) + 1
        )


        instructions = exercise.get("instructions")

        if (
            not isinstance(instructions, list)
            or not instructions
        ):

            print(
                f"{name}: instructions must "
                f"be a non-empty list"
            )

            errors += 1

        has_hold = exercise.get("has_hold")
        hold_options = exercise.get(
            "hold_options_seconds"
        )

        if has_hold:

            if (
                not isinstance(hold_options, list)
                or not hold_options
            ):

                print(
                    f"{name}: has_hold=True "
                    f"but no hold options"
                )

                errors += 1

        sets = exercise.get("set_options")

        if (
            not isinstance(sets, list)
            or not sets
        ):

            print(
                f"{name}: invalid set_options"
            )

            errors += 1


        reps = exercise.get("rep_options")

        if category in {
            "activation",
            "integration"
        }:

            if (
                not isinstance(reps, list)
                or not reps
            ):

                print(
                    f"{name}: {category} "
                    f"requires rep_options"
                )

                errors += 1


    print("\n--- SUMMARY ---")

    print(f"Total exercises: {len(exercise_data)}")
    print(f"Unique exercise IDs: {len(exercise_ids)}")

    print("\nExercises by category:")

    for category, count in sorted(
        category_counts.items()
    ):

        print(f"  {category}: {count}")

    print("\nTarget muscles:")

    for muscle, count in sorted(
        muscle_counts.items()
    ):

        print(f"  {muscle}: {count}")

    print("\n" + "=" * 60)

    if errors == 0:

        print("DATASET VALIDATION PASSED")

    else:

        print(f"Errors: {errors}")

    print("=" * 60)


if __name__ == "__main__":
    validate()
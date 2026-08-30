def choose_from_range(options, preferred, default):
    """Choose the closest sensible value from available options."""

    if not options:
        return default

    if preferred in options:
        return preferred

    return min(options, key=lambda x: abs(x - preferred))


def get_week_prescription(category, phase, exercise):
    """
    Generate prescription values according to the 4-week progression.

    Weeks 1–2:
        Release    -> 1–2 sets, 4–6 reps OR 20–30 sec hold
        Stretch    -> 1–2 sets, 20–30 sec hold
        Activation -> 1–2 sets, 10–15 reps
        Integration -> omitted

    Weeks 3–4:
        Release    -> omitted
        Stretch    -> 1 set, 60 sec hold
        Activation -> 1–2 sets, 10–15 reps
        Integration -> 1–3 sets, 10–15 reps
    """

    category = category.lower()
    phase = phase.lower()

    set_options = exercise.get("set_options", [])
    rep_options = exercise.get("rep_options", [])
    hold_options = exercise.get("hold_options_seconds", [])

    has_hold = exercise.get("has_hold", False)
    tempo = exercise.get("tempo")


    if phase == "weeks_1_2":

        if category == "release":

            sets = choose_from_range(
                set_options,
                preferred=2,
                default=2
            )

            if has_hold and hold_options:

                hold = choose_from_range(
                    hold_options,
                    preferred=30,
                    default=30
                )

                reps = None

            else:

                reps = choose_from_range(
                    rep_options,
                    preferred=6,
                    default=6
                )

                hold = None

            rest = 15

        elif category == "stretch":

            sets = choose_from_range(
                set_options,
                preferred=2,
                default=2
            )

            hold = choose_from_range(
                hold_options,
                preferred=30,
                default=30
            )

            reps = None
            rest = 15

        elif category == "activation":

            sets = choose_from_range(
                set_options,
                preferred=2,
                default=2
            )

            reps = choose_from_range(
                rep_options,
                preferred=12,
                default=12
            )

            hold = None
            rest = 30

        elif category == "integration":

            return None

        else:
            return None


    elif phase == "weeks_3_4":

        if category == "release":

            return None

        elif category == "stretch":

            sets = 1

            hold = 60
            reps = None
            rest = 15

        elif category == "activation":

            sets = choose_from_range(
                set_options,
                preferred=2,
                default=2
            )

            reps = choose_from_range(
                rep_options,
                preferred=15,
                default=15
            )

            hold = None
            rest = 30

        elif category == "integration":

            sets = choose_from_range(
                set_options,
                preferred=2,
                default=2
            )

            reps = choose_from_range(
                rep_options,
                preferred=12,
                default=12
            )

            hold = None
            rest = 60

        else:
            return None

    else:
        raise ValueError(
            "phase must be 'weeks_1_2' or 'weeks_3_4'"
        )


    display = format_prescription(
        sets=sets,
        reps=reps,
        hold_seconds=hold,
        tempo=tempo,
        rest_seconds=rest
    )

    return {
        "sets": sets,
        "reps": reps,
        "hold_seconds": hold,
        "tempo": tempo,
        "rest_seconds": rest,
        "display": display
    }


def format_prescription(
    sets,
    reps=None,
    hold_seconds=None,
    tempo=None,
    rest_seconds=None
):
    """Create the final UI-friendly prescription string."""

    if hold_seconds is not None:
        text = f"{sets} x 1 ({hold_seconds} secs hold)"

    elif reps is not None:
        text = f"{sets} x {reps}"

    else:
        text = f"{sets} sets"

    if tempo:
        text += f" (tempo {tempo})"

    if rest_seconds is not None:
        text += f" / {rest_seconds} secs rest"

    return text



if __name__ == "__main__":

    test_exercise = {
        "name": "Doorway Pec Stretch",
        "category": "stretch",
        "has_hold": True,
        "hold_options_seconds": [20, 30, 60],
        "rep_options": [],
        "set_options": [1, 2],
        "tempo": None
    }

    print("=" * 60)
    print("PRESCRIPTION PROGRESSION TEST")
    print("=" * 60)

    print("\nWeeks 1–2:")
    print(
        get_week_prescription(
            "stretch",
            "weeks_1_2",
            test_exercise
        )
    )

    print("\nWeeks 3–4:")
    print(
        get_week_prescription(
            "stretch",
            "weeks_3_4",
            test_exercise
        )
    )
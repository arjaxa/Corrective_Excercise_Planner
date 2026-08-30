import streamlit as st

from planner import generate_plan


st.set_page_config(
    page_title="Corrective Exercise Planner",
    page_icon="",
    layout="wide"
)


st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #888;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .phase-description {
        color: #888;
        margin-bottom: 1.2rem;
    }

    .exercise-prescription {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .muscle-label {
        color: #888;
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)



st.markdown(
    '<div class="main-title">Corrective Exercise Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Generate a structured 4-week corrective exercise plan '
    'based on a selected posture issue.'
    '</div>',
    unsafe_allow_html=True
)



posture_options = {
    "Forward Head Posture": "forward_head",
    "Upper Crossed Syndrome": "upper_crossed_syndrome",
    "Lower Crossed Syndrome": "lower_crossed_syndrome",
}


selected_posture = st.selectbox(
    "Select Posture Issue",
    list(posture_options.keys())
)


generate = st.button(
    "Generate 4-Week Plan",
    type="primary",
    use_container_width=True
)



def display_exercise(exercise):

    with st.container(border=True):


        st.subheader(
            exercise["name"]
        )


        target = exercise.get(
            "target_muscle",
            ""
        )

        if target:

            formatted_target = (
                target
                .replace("_", " ")
                .title()
            )

            st.markdown(
                f'<div class="muscle-label">'
                f'Target: {formatted_target}'
                f'</div>',
                unsafe_allow_html=True
            )


        prescription = exercise.get(
            "prescription",
            {}
        )

        display = prescription.get(
            "display",
            ""
        )

        if display:

            st.markdown(
                f'<div class="exercise-prescription">'
                f'{display}'
                f'</div>',
                unsafe_allow_html=True
            )

       

        equipment = exercise.get(
            "equipment"
        )

        if equipment:

            st.caption(
                f"Equipment: {equipment}"
            )


        instructions = exercise.get(
            "instructions",
            []
        )

        if instructions:

            with st.expander("Instructions"):

                for instruction in instructions:

                    st.write(
                        f"• {instruction}"
                    )



def display_phase(phase):


    if phase.get("release"):

        st.subheader("Release")

        for exercise in phase["release"]:

            display_exercise(exercise)


    if phase.get("stretch"):

        st.subheader("Stretch")

        for exercise in phase["stretch"]:

            display_exercise(exercise)


    if phase.get("activation"):

        st.subheader("Activation")

        for exercise in phase["activation"]:

            display_exercise(exercise)


    if phase.get("integration"):

        st.subheader("Integration")

        for exercise in phase["integration"]:

            display_exercise(exercise)


if generate:

    posture_key = posture_options[
        selected_posture
    ]

    try:

        plan = generate_plan(
            posture_key
        )

    except Exception as error:

        st.error(
            f"Unable to generate plan: {error}"
        )

        st.stop()



    st.divider()

    st.header(
        plan["posture_name"]
    )

    st.caption(
        "Corrective exercise progression"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "Overactive Muscles"
        )

        for muscle in plan[
            "overactive_muscles"
        ]:

            st.write(
                f"• "
                f"{muscle.replace('_', ' ').title()}"
            )


    with col2:

        st.subheader(
            "Underactive Muscles"
        )

        for muscle in plan[
            "underactive_muscles"
        ]:

            st.write(
                f"• "
                f"{muscle.replace('_', ' ').title()}"
            )



    st.divider()

    st.header(
        "Weeks 1–2"
    )

    st.markdown(
        '<div class="phase-description">'
        'Foundation phase — release overactive tissues, '
        'restore flexibility, and activate underactive muscles.'
        '</div>',
        unsafe_allow_html=True
    )

    display_phase(
        plan["weeks_1_2"]
    )



    st.divider()

    st.header(
        "Weeks 3–4"
    )

    st.markdown(
        '<div class="phase-description">'
        'Progression phase — release work is removed, '
        'stretching is maintained with longer holds, '
        'activation volume increases, and compound '
        'integration exercises are introduced.'
        '</div>',
        unsafe_allow_html=True
    )

    display_phase(
        plan["weeks_3_4"]
    )


    st.divider()

    st.success(
        "4-week corrective exercise plan generated successfully."
    )


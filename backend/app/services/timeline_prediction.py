from datetime import date, timedelta


def predict_completion_date(
    planned_start_date: date,
    planned_end_date: date,
    actual_start_date: date | None,
    actual_progress: float,
):
    """
    Aurex Predictive Timeline Intelligence.

    Separates:
    1. Calendar-based schedule position
    2. Current execution rate
    3. Predicted completion
    4. Predicted delay / recovery margin
    """

    today = date.today()

    # -------------------------------------------------
    # BASIC DATA VALIDATION
    # -------------------------------------------------

    if actual_start_date is None:
        return {
            "prediction_status": "insufficient_data",
            "current_schedule_status": "unknown",
            "predicted_completion_date": None,
            "predicted_delay_days": None,
            "recovery_margin_days": None,
            "prediction_message": (
                "Actual start date is required to "
                "predict project completion."
            ),
        }

    if actual_progress <= 0:
        return {
            "prediction_status": "insufficient_data",
            "current_schedule_status": "unknown",
            "predicted_completion_date": None,
            "predicted_delay_days": None,
            "recovery_margin_days": None,
            "prediction_message": (
                "Actual progress must be greater than "
                "0% to predict project completion."
            ),
        }

    # -------------------------------------------------
    # PROJECT DURATION
    # -------------------------------------------------

    elapsed_days = (
        today - actual_start_date
    ).days

    if elapsed_days <= 0:
        elapsed_days = 1

    planned_total_days = (
        planned_end_date - planned_start_date
    ).days

    if planned_total_days <= 0:
        planned_total_days = 1

    # -------------------------------------------------
    # CALENDAR-BASED EXPECTED PROGRESS
    # -------------------------------------------------

    planned_elapsed_days = (
        today - planned_start_date
    ).days

    planned_elapsed_days = max(
        0,
        min(
            planned_elapsed_days,
            planned_total_days,
        ),
    )

    expected_progress_today = (
        planned_elapsed_days / planned_total_days
    ) * 100

    # Positive = ahead of calendar schedule
    # Negative = behind calendar schedule
    calendar_progress_difference = (
        actual_progress - expected_progress_today
    )

    # -------------------------------------------------
    # CURRENT CALENDAR SCHEDULE STATUS
    # -------------------------------------------------

    if calendar_progress_difference >= 0:
        current_schedule_status = "ahead_of_schedule"

    elif calendar_progress_difference >= -10:
        current_schedule_status = "slightly_delayed"

    elif calendar_progress_difference >= -25:
        current_schedule_status = "delayed"

    else:
        current_schedule_status = "critically_delayed"

    # -------------------------------------------------
    # COMPLETED PROJECT
    # -------------------------------------------------

    if actual_progress >= 100:
        return {
            "planned_start_date": planned_start_date,
            "planned_end_date": planned_end_date,
            "actual_start_date": actual_start_date,
            "actual_progress_percent": 100,
            "expected_progress_today_percent": round(
                expected_progress_today,
                2,
            ),
            "calendar_progress_difference_percent": round(
                calendar_progress_difference,
                2,
            ),
            "current_schedule_status": (
                current_schedule_status
            ),
            "progress_per_day_percent": None,
            "estimated_remaining_days": 0,
            "predicted_completion_date": today,
            "predicted_delay_days": 0,
            "recovery_margin_days": 0,
            "prediction_status": "completed",
            "prediction_message": (
                "Project progress indicates that the "
                "project is complete."
            ),
        }

    # -------------------------------------------------
    # CURRENT EXECUTION RATE
    # -------------------------------------------------

    progress_per_day = (
        actual_progress / elapsed_days
    )

    if progress_per_day <= 0:
        return {
            "prediction_status": "insufficient_data",
            "current_schedule_status": (
                current_schedule_status
            ),
            "predicted_completion_date": None,
            "predicted_delay_days": None,
            "recovery_margin_days": None,
            "prediction_message": (
                "Current progress rate is insufficient "
                "for a reliable completion prediction."
            ),
        }

    # -------------------------------------------------
    # PREDICT COMPLETION
    # -------------------------------------------------

    remaining_progress = (
        100 - actual_progress
    )

    estimated_remaining_days = round(
        remaining_progress / progress_per_day
    )

    predicted_completion_date = (
        today
        + timedelta(
            days=estimated_remaining_days
        )
    )

    # -------------------------------------------------
    # COMPLETION DELAY / RECOVERY MARGIN
    # -------------------------------------------------

    completion_difference = (
        predicted_completion_date
        - planned_end_date
    ).days

    if completion_difference > 0:
        predicted_delay_days = (
            completion_difference
        )
        recovery_margin_days = 0

    else:
        predicted_delay_days = 0
        recovery_margin_days = abs(
            completion_difference
        )

    # -------------------------------------------------
    # FUTURE PREDICTION STATUS
    # -------------------------------------------------

    if predicted_delay_days == 0:

        if current_schedule_status in [
            "slightly_delayed",
            "delayed",
            "critically_delayed",
        ]:
            prediction_status = (
                "currently_delayed_but_projected_on_track"
            )
        else:
            prediction_status = "on_track"

    elif predicted_delay_days <= 30:
        prediction_status = "slightly_delayed"

    elif predicted_delay_days <= 90:
        prediction_status = "delayed"

    else:
        prediction_status = "critically_delayed"

    # -------------------------------------------------
    # PREDICTION MESSAGE
    # -------------------------------------------------

    if prediction_status == "on_track":

        if current_schedule_status == "ahead_of_schedule":

            prediction_message = (
                f"The project is currently "
                f"{round(calendar_progress_difference, 2)}% "
                "ahead of its calendar-based schedule "
                "and is projected to finish within "
                "the planned timeline."
            )

        else:

            prediction_message = (
                "Current project execution indicates "
                "that the project is expected to finish "
                "within the planned timeline."
            )

    elif prediction_status == (
        "currently_delayed_but_projected_on_track"
    ):

        prediction_message = (
            "The project is currently behind its "
            "calendar-based schedule, but its current "
            "execution rate projects completion within "
            "the planned timeline."
        )

    elif prediction_status == "slightly_delayed":

        prediction_message = (
            "The project is currently showing schedule "
            "pressure and is predicted to experience "
            f"a minor delay of {predicted_delay_days} days."
        )

    elif prediction_status == "delayed":

        prediction_message = (
            "The project is predicted to exceed its "
            f"planned completion date by "
            f"{predicted_delay_days} days. Corrective "
            "timeline action is recommended."
        )

    else:

        prediction_message = (
            "The project is predicted to experience a "
            f"critical completion delay of "
            f"{predicted_delay_days} days. Immediate "
            "schedule recovery action is recommended."
        )

    # -------------------------------------------------
    # FINAL AUREX TIMELINE PREDICTION
    # -------------------------------------------------

    return {
        "planned_start_date": planned_start_date,
        "planned_end_date": planned_end_date,
        "actual_start_date": actual_start_date,

        "actual_progress_percent": round(
            actual_progress,
            2,
        ),

        "expected_progress_today_percent": round(
            expected_progress_today,
            2,
        ),

        "calendar_progress_difference_percent": round(
            calendar_progress_difference,
            2,
        ),

        "current_schedule_status": (
            current_schedule_status
        ),

        "progress_per_day_percent": round(
            progress_per_day,
            4,
        ),

        "estimated_remaining_days": (
            estimated_remaining_days
        ),

        "predicted_completion_date": (
            predicted_completion_date
        ),

        "predicted_delay_days": (
            predicted_delay_days
        ),

        "recovery_margin_days": (
            recovery_margin_days
        ),

        "prediction_status": (
            prediction_status
        ),

        "prediction_message": (
            prediction_message
        ),
    }
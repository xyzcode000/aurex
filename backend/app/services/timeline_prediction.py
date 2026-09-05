from datetime import date, timedelta


def predict_completion_date(
    planned_start_date: date,
    planned_end_date: date,
    actual_start_date: date | None,
    actual_progress: float,
):
    """
    Predict the expected completion date of a project
    using current progress and elapsed project time.
    """

    today = date.today()

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------

    if actual_start_date is None:
        return {
            "prediction_status": "insufficient_data",
            "predicted_completion_date": None,
            "predicted_delay_days": None,
            "prediction_message": (
                "Actual start date is required to "
                "predict project completion."
            ),
        }

    if actual_progress <= 0:
        return {
            "prediction_status": "insufficient_data",
            "predicted_completion_date": None,
            "predicted_delay_days": None,
            "prediction_message": (
                "Actual progress must be greater than "
                "0% to predict project completion."
            ),
        }

    if actual_progress >= 100:
        return {
            "prediction_status": "completed",
            "predicted_completion_date": today,
            "predicted_delay_days": 0,
            "prediction_message": (
                "Project progress indicates that the "
                "project is complete."
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

    # -------------------------------------------------
    # PROGRESS RATE
    # -------------------------------------------------

    progress_per_day = (
        actual_progress / elapsed_days
    )

    if progress_per_day <= 0:
        return {
            "prediction_status": "insufficient_data",
            "predicted_completion_date": None,
            "predicted_delay_days": None,
            "prediction_message": (
                "Current progress rate is insufficient "
                "for a reliable completion prediction."
            ),
        }

    # -------------------------------------------------
    # REMAINING PROGRESS
    # -------------------------------------------------

    remaining_progress = 100 - actual_progress

    estimated_remaining_days = (
        remaining_progress / progress_per_day
    )

    estimated_remaining_days = round(
        estimated_remaining_days
    )

    # -------------------------------------------------
    # PREDICTED COMPLETION
    # -------------------------------------------------

    predicted_completion_date = (
        today
        + timedelta(
            days=estimated_remaining_days
        )
    )

    # -------------------------------------------------
    # PREDICTED DELAY
    # -------------------------------------------------

    predicted_delay_days = (
        predicted_completion_date
        - planned_end_date
    ).days

    if predicted_delay_days < 0:
        predicted_delay_days = 0

    # -------------------------------------------------
    # PREDICTION STATUS
    # -------------------------------------------------

    if predicted_delay_days == 0:
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
        prediction_message = (
            "Current progress indicates that the "
            "project is expected to finish within "
            "the planned timeline."
        )

    elif prediction_status == "slightly_delayed":
        prediction_message = (
            "The project is predicted to experience "
            "a minor completion delay. Monitoring "
            "is recommended."
        )

    elif prediction_status == "delayed":
        prediction_message = (
            "The project is predicted to exceed its "
            "planned completion date. Corrective "
            "timeline action is recommended."
        )

    else:
        prediction_message = (
            "The project is predicted to experience "
            "a critical completion delay. Immediate "
            "management intervention is recommended."
        )

    # -------------------------------------------------
    # RETURN AUREX PREDICTION
    # -------------------------------------------------

    return {
        "planned_start_date": planned_start_date,
        "planned_end_date": planned_end_date,
        "actual_start_date": actual_start_date,
        "actual_progress_percent": round(
            actual_progress,
            2,
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
        "prediction_status": prediction_status,
        "prediction_message": prediction_message,
    }
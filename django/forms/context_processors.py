SESSION_FORMS_PATH = "forms_onboarding_path"
PATH_RENTER = "renter"
PATH_SUBLETTOR = "sublettor"


def _is_under_forms(path: str) -> bool:
    if path.startswith("/forms/"):
        return True
    return path.rstrip("/") == "/forms"


def forms_workflow(request):
    """Expose active onboarding workflow for /forms/ templates (toggle UI)."""
    if not _is_under_forms(request.path):
        return {}
    mode = request.session.get(SESSION_FORMS_PATH, PATH_RENTER)
    return {
        "forms_workflow_mode": mode,
        "forms_workflow_is_renter": mode == PATH_RENTER,
        "forms_workflow_is_sublettor": mode == PATH_SUBLETTOR,
    }

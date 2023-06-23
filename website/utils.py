from .researcher import get_Researcher_Project
from .evaluator import get_Evaluator_Project



def get_project(current_user, project_id):
    if current_user.__class__.__name__ == "Researcher":
        return get_Researcher_Project(project_id)
    elif current_user.__class__.__name__ == "Evaluator":
        return get_Evaluator_Project(project_id)



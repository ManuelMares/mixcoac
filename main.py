from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import logging
import json
import uvicorn

with open("information.json", "r") as file:
    profiles = json.load(file)


mixcoac = FastAPI()
# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")
# add static files (css and js)
mixcoac.mount("/static", StaticFiles(directory="static"), name="static")


# setting up logging messages
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

@mixcoac.get("/", response_class=HTMLResponse)
async def redirect_to_profiles():
    return RedirectResponse(url="/profiles")


@mixcoac.get("/profiles", response_class=HTMLResponse)
async def home(request: Request):
    profile_names = profiles.keys()
    logger.debug(profile_names)
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "message": "Mixcoac",
            "profile_names": profile_names,
        }
    )

@mixcoac.get("/profiles/{profile_id}", response_class = HTMLResponse)
async def get_profile(request:Request, profile_id:str):
    profile_data = profiles.get(profile_id, []) # get item or empty list
    profile_name = profile_id
    resume_names = profile_data["resumes"].keys()
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "profile_name": profile_name,
            "resume_names": resume_names
        }
    )


@mixcoac.get("/profiles/{profile_id}/profile_data", response_class = HTMLResponse)
async def get_profile(request:Request, profile_id:str):
    profile_data = profiles.get(profile_id, []) # get item or empty list
    profile_name = profile_id
    personal_information = profile_data["data"]["personal_information"]
    education = profile_data["data"]["education"]
    work_experience = profile_data["data"]["work_experience"]
    certifications = profile_data["data"]["certifications"]
    hard_skills = profile_data["data"]["hard_skills"]
    projects = profile_data["data"]["projects"]
    publications = profile_data["data"]["publications"]
    references = profile_data["data"]["references"]
    extracurricular = profile_data["data"]["extracurricular"]
    return templates.TemplateResponse(
        "profile-data.html",
        {
            "request": request,
            "profile_name": profile_name,
            "personal_information": personal_information,
            "education": education,
            "work_experience": work_experience,
            "certifications": certifications,
            "hard_skills": hard_skills,
            "projects": projects,
            "publications": publications,
            "references": references,
            "extracurricular": extracurricular
        }
    )

if __name__ == "__main__":
    uvicorn.run(mixcoac, host="127.0.0.1", port=8000)

    
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import List
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
mixcoac.state.profile = {}


def getProfile():
    with open("information.json", "r") as file:
        profiles = json.load(file)
    return profiles[CURRENT_PROFILE]

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
async def get_profiles(request:Request, profile_id:str):
    profile_data = profiles.get(profile_id, []) # get item or empty list
    mixcoac.state.profile = profile_data
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
    return templates.TemplateResponse(
        "profile-data.html",
        {
            "request": request
        }
    )


@mixcoac.get("/updateName", response_class = HTMLResponse)
async def get_name(request:Request):
    name = mixcoac.state.profile["data"]["personal_information"]["name"]

    return templates.TemplateResponse(
        "partials/name.html",
        {
            "request": request,
            "name": name
        }
    )

@mixcoac.get("/updateLinks", response_class = HTMLResponse)
async def get_name(request:Request):
    links = mixcoac.state.profile["data"]["personal_information"]["links"]

    return templates.TemplateResponse(
        "partials/links.html",
        {
            "request": request,
            "links": links
        }
    )

@mixcoac.get("/updateLanguages", response_class = HTMLResponse)
async def get_name(request:Request):
    languages = mixcoac.state.profile["data"]["personal_information"]["languages"]
    return templates.TemplateResponse(
        "partials/languages.html",
        {
            "request": request,
            "languages": languages
        }
    )




@mixcoac.post("/add-profile-links", response_class = HTMLResponse)
async def add_link(request:Request,
    link_name: List[str] = Form(...),
    link_url: List[str] = Form(...),
    icon: List[str] = Form(...)
):   
    links = [
        {"name": name, "url": url, "icon": ic}
        for name, url, ic in zip(link_name, link_url, icon)
    ]
    links.append({"name": "", "url": "", "icon": "faLink"})
    return templates.TemplateResponse(
        "partials/links.html",
        {
            "request": request,
            "links": links,
        }
    )

@mixcoac.post("/remove-link", response_class=HTMLResponse)
async def remove_link(
    request: Request,
    delete_index: int = Form(...),
    link_name: List[str] = Form(...),
    link_url: List[str] = Form(...),
    icon: List[str] = Form(...)
):
    # Reconstruct all links
    links = [
        {"name": name, "url": url, "icon": ic}
        for name, url, ic in zip(link_name, link_url, icon)
    ]

    # Remove the selected one
    if 0 <= delete_index < len(links):
        del links[delete_index]

    return templates.TemplateResponse("partials/links.html", {
        "request": request,
        "links": links
    })

if __name__ == "__main__":
    uvicorn.run(mixcoac, host="127.0.0.1", port=8000)

    
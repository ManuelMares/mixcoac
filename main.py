import json
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import NoEscape  # when inserting command (i.e. \color{}), NoEscape prevents this to be translated to \textEscape{}color{} 
from pylatex import Document, Package
from datetime import datetime
import subprocess

# Meta data variables
url_color = "primaryColor"
today=datetime.today()


# personal data settings
_DATE_FORMAT = "month year"
_ADDRESS_FORMAT = "state, country"
show_addresses = [0]
show_links = [0,1,2]
show_emails = [0]
show_phones = [0]
name_format = "last, Middle_initial. first"
header_order = ["address", "email", "phone", "links"]


show_education = [2,1,0]
show_education_date = False
show_education_data = { # each element is a line
    "left_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
        [ # line 1
            {
                "text": "institution",
                "bold": True,
                "italics": False
            }
        ], 
        [ # line 2
            {
                "text": "degree",
                "bold": False,
                "italics": True
            }
        ]
    ],
    "right_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
        [
            {
                "text": "graduation_date",
                "bold": False,
                "italics": False,
            }
        ]
    ]
}


def add_header(doc, personal_information): # Add content to the document body
    doc.append(NoEscape(r""" 
    \newcommand{\AND}{\unskip
        \cleaders\copy\ANDbox\hskip\wd\ANDbox
        \ignorespaces
    }
    \newsavebox\ANDbox
    \sbox\ANDbox{}
    
    \placelastupdatedtext
    \begin{header}
        \textbf{\fontsize{24 pt}{24 pt}\selectfont """ + format_name(personal_information["name"], name_format) + r"""}

        \vspace{0.3 cm}

        \normalsize"""))

    # show addresses
    listedElements_counter = 0

    for element in header_order:
        if element == "address":
            for addressIndex in show_addresses:
                try:
                    address = personal_information["contact"]["addresses"][addressIndex]

                    if listedElements_counter > 0:
                        doc.append(NoEscape(r"""\AND"""))

                    doc.append(NoEscape(r"""\mbox{{\color{black}\footnotesize\faMapMarker*}\hspace*{0.13cm} """ 
                    + 
                        format_address(address, _ADDRESS_FORMAT) 
                    + 
                    r"""} % New Address
                    \kern 0.25 cm %"""))
                    listedElements_counter += 1
                except:
                    continue

        if element == "email":
            # show emails
            for emailIndex in show_emails:
                try:
                    email = personal_information["contact"]["emails"][emailIndex]

                    if listedElements_counter > 0:
                        doc.append(NoEscape(r"""\AND"""))

                    doc.append(NoEscape(r"""\mbox{\hrefWithoutArrow{mailto:""" 
                    + 
                        email
                    + 
                    r"""}{\color{black}{\footnotesize\faEnvelope[regular]}\hspace*{0.13cm}"""
                    + 
                        email
                    + 
                    r"""}} % New email
                    \kern 0.25 cm %"""))
                    listedElements_counter += 1
                except:
                    continue

        if element == "phone":
            # show phone numbers
            for phoneIndex in show_phones:
                try:
                    phone = personal_information["contact"]["phone_numbers"][phoneIndex]

                    if listedElements_counter > 0:
                        doc.append(NoEscape(r"""\AND"""))

                    doc.append(NoEscape(r"""\mbox{\hrefWithoutArrow{tel:"""
                    + 
                        phone 
                    + 
                    r"""}{\color{black}{\footnotesize\faPhone*}\hspace*{0.13cm}"""
                    + 
                        phone 
                    + 
                    r"""}} % New phone number
                    \kern 0.25 cm %"""))
                    listedElements_counter += 1
                except:
                    continue

        if element == "links":
            # show links
            for linkIndex in show_links:
                try:
                    link =  personal_information["links"][linkIndex]
                    link_name = link["name"]
                    link_link = link["link"]
                    link_icon = link["icon"]
                    
                    if listedElements_counter > 0:
                        doc.append(NoEscape(r"""\AND"""))

                    doc.append(NoEscape(r"""\kern 0.25 cm%
                        \mbox{\hrefWithoutArrow{""" + link_link + r"""}{\color{black}{\footnotesize\fa""" + link_icon + r"""}\hspace*{0.13cm}""" + link_name + r"""}} % new link
                        \kern 0.25 cm%"""))        
                except:
                    continue

    doc.append(NoEscape(r"""\end{header}
    \vspace{0.3 cm - 0.3 cm}    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""))


def add_education(doc, education, section_Name): # Add the Education section title
    add_new_section(doc, section_Name)

    # Loop through the universities and append their information
    for degreeIndex in show_education:
        degree = education[degreeIndex]
        doc.append(NoEscape(r"""    %---- New """ + section_Name + r"""----"""))

        # adding right side lines
        right_lines = show_education_data["right_lines"]
        if len(right_lines) > 0:
            doc.append(NoEscape(r"""    \begin{twocolentry}{ % start of double columns new """ + section_Name))
        else:
            doc.append(NoEscape(r"""    \begin{onecolentry} % start of single column new """ + section_Name))

        num_lines = len(show_education_data["right_lines"])
        counter = 1
        for rl in right_lines: # for each line
            formatted_text = "        " # guarantees all items are within same line
            num_items = len(rl)
            counter_items = 1
            for item in rl: # for each element in same line                        
                # open text styles
                if item["bold"]:
                    formatted_text += r"""\textbf{"""
                if item["italics"]:
                    formatted_text += r"""\textit{"""
                
                # add item
                item_text = item["text"]
                item_content = degree[item_text]
                if type(item_content) is list: # checking if element are bullet points
                    if len(item_content) > 0: #only if not empty list
                        formatted_text += r"\begin{highlights} % start bullet points"
                        formatted_text += "\n"
                        for bp in item_content:
                            formatted_text += r"            \item " + bp 
                            formatted_text += "\n"
                        formatted_text += r"        \end{highlights} % end bullet points"
                else:
                    if "date" in item_text:
                        formatted_text += format_date(date=item_content, format=_DATE_FORMAT)
                    else:
                        formatted_text += item_content

                # close text styles
                if item["bold"]:
                    formatted_text += r"""}"""
                if item["italics"]:
                    formatted_text += r"""}"""

                # adding space between items
                if counter_items < num_items:
                    formatted_text += r""", """
                counter_items += 1

            # adding a new line for all lines except last one
            if counter < num_lines:
                if type(degree[show_education_data["right_lines"][counter][0]["text"]]) is list: # if next line (its first element) is bullet points, omit line jump
                    doc.append(NoEscape(formatted_text)) 
                else: 
                    doc.append(NoEscape(formatted_text + r""" \\ """)) 
            else:
                if not formatted_text == "        ":
                    doc.append(NoEscape(formatted_text)) 
            counter += 1
        if len(right_lines) > 0:
            doc.append(NoEscape(r"""    } % end right column in double column new """ + section_Name))

        # adding left side lines
        num_lines = len(show_education_data["left_lines"])
        counter = 1
        for ll in show_education_data["left_lines"]: # for each line
            formatted_text = "        " # guarantees all items are within same line
            num_items = len(ll)
            counter_items = 1
            for item in ll: # for each element in same line
                # open text styles
                if item["bold"]:
                    formatted_text += r"""\textbf{"""
                if item["italics"]:
                    formatted_text += r"""\textit{"""
                
                # add item
                item_text = item["text"]
                item_content = degree[item_text]
                if type(item_content) is list: # checking if element are bullet points
                    if len(item_content) > 0: #only if not empty list
                        formatted_text += r"\begin{highlights} % start bullet points"
                        formatted_text += "\n"
                        for bp in item_content:
                            formatted_text += r"            \item " + bp 
                            formatted_text += "\n"
                        formatted_text += r"        \end{highlights} % end bullet points"
                else:
                    if "date" in item_text:
                        formatted_text += format_date(date=item_content, format=_DATE_FORMAT)
                    else:
                        formatted_text += item_content

                # close text styles
                if item["bold"]:
                    formatted_text += r"""}"""
                if item["italics"]:
                    formatted_text += r"""}"""
                    
                # adding space between items
                if counter_items < num_items:
                    formatted_text += r""", """
                counter_items += 1


            # adding a new line for all lines except last one
            if counter < num_lines:
                if type(degree[show_education_data["left_lines"][counter][0]["text"]]) is list: # if next line (its first element) is bullet points, omit line jump
                    doc.append(NoEscape(formatted_text)) 
                else: 
                    doc.append(NoEscape(formatted_text + r""" \\ """)) 
            else:
                if not formatted_text == "        ":
                    doc.append(NoEscape(formatted_text)) 
            counter += 1


        if len(right_lines) > 0:
            doc.append(NoEscape(r"""    \end{twocolentry} % end of double column new """ + section_Name))
        else:
            doc.append(NoEscape(r"""    \end{onecolentry} % end of single column new """ + section_Name))
        doc.append(NoEscape(r"""    \vspace{0.10 cm}"""))





        # # adding left side lines
        # for ll in show_education_data["left_lines"]:
        #     ll_texts = ll["text"]
        #     ll_isBold = ll["bold"]
        #     doc.append(NoEscape(r"""\textit{""" + degree=[ll] + r"""}"""))            

        # \end{twocolentry}"""))

        # # description
        # if len(degree["description"]) > 0: # add bullet points if any available
        #     doc.append(NoEscape(r"""\begin{onecolentry}
        #     \begin{highlights}"""))                                 # open bullet points
        #     for bulletPoint in degree["description"]:           
        #         doc.append(NoEscape(r"""\item """ + bulletPoint))     # bullet point              
        #     doc.append(NoEscape(r"""\end{highlights}    
        #     \end{onecolentry}"""))                                  # close bullet points
        # doc.append(NoEscape(r"""\vspace{0.10 cm}"""))




def add_experience(doc, experience): # Add the Experience section title
    add_new_section(doc, "Experience")

    # Loop through the jobs and append their information
    for job in experience:
        start_date = format_date(date=job["start_date"], format=_DATE_FORMAT, )
        en_date = format_date(date=job["end_date"], format=_DATE_FORMAT, status=job["end_date"]["status"])
        doc.append(NoEscape(r""" \begin{twocolentry}{ % new job
        \textit{""" + job["location"] + r"""}
        
        \textit{""" + start_date + " - " + en_date + r"""}
    }
        \textbf{""" + job["job_title"] + r"""}
        
        \textit{""" + job["company"] + r"""}
    \end{twocolentry}
    \vspace{0.10 cm}"""))
    
    if len(job["responsibilities"]) > 0: # add bullet points if any available
            responsibilities = job["responsibilities"]
            doc.append(NoEscape(r"""\begin{onecolentry} % responsibilities
            \begin{highlights}"""))                                 # open bullet points
            for bulletPoint in responsibilities:           
                doc.append(NoEscape(r"""\item """ + bulletPoint))     # bullet point              
            doc.append(NoEscape(r"""\end{highlights}    
            \end{onecolentry}"""))                                  # close bullet points
    
    if len(job["achievements"]) > 0: # add bullet points if any available
            achievements = job["achievements"]
            doc.append(NoEscape(r"""\begin{onecolentry} % achievements
            \begin{highlights}"""))                                 # open bullet points
            for bulletPoint in achievements:           
                doc.append(NoEscape(r"""\item """ + bulletPoint))     # bullet point              
            doc.append(NoEscape(r"""\end{highlights}    
            \end{onecolentry}"""))                                  # close bullet points
    
    if len(job["description"]) > 0: # add bullet points if any available
            description = job["description"]
            doc.append(NoEscape(r"""\begin{onecolentry} % description
            \begin{highlights}"""))                                 # open bullet points
            for bulletPoint in description:           
                doc.append(NoEscape(r"""\item """ + bulletPoint))     # bullet point              
            doc.append(NoEscape(r"""\end{highlights}    
            \end{onecolentry}"""))                                  # close bullet points



def add_projects(doc, projects): # Add the Experience section title
    doc.append(NoEscape(r"\section{Projects}  % PROJECTS SECTION"))

    for project in projects["projects"]:

        doc.append(NoEscape(r"""\begin{twocolentry}{
            \textit{
            """ + format_date(project["date"], "year") + r""" - \href{""" + project["link"] + r"""}{see project}
            }}
            \textbf{""" + project["title"] + r"""}
        \end{twocolentry}

        \vspace{0.10 cm}
        \begin{onecolentry}
            \begin{highlights}"""))
        for bp in project["description"]:
                doc.append(NoEscape(r"""\item """ + bp ))
        
        doc.append(NoEscape(r"""\end{highlights}
        \end{onecolentry}"""))
    
def add_hard_skills(doc, skills): # Add the Experience section title
    doc.append(NoEscape(r"\section{Hard Skills}  % HARD SKILLS"))

    # Loop through the jobs and append their information
    for skill_set in skills:
        if skill_set["skills"] == "":
            continue 

        
        doc.append(NoEscape(r"""\begin{onecolentry} % New Skill Set
            \textbf{""" + skill_set["title"] + r""":} """ + escape_latex(skill_set["skills"]) + r"""
        \end{onecolentry}
        \vspace{0.2 cm}"""))


def add_document_settings(doc, personal_information, today):
    doc.preamble.append(NoEscape(r"""
% Some settings:
\AtBeginEnvironment{adjustwidth}{\partopsep0pt} % remove space before adjustwidth environment
\pagestyle{empty} % no header or footer
\setcounter{secnumdepth}{0} % no section numbering
\setlength{\parindent}{0pt} % no indentation
\setlength{\topskip}{0pt} % no top skip
\setlength{\columnsep}{0cm} % set column separation
\makeatletter
\let\ps@customFooterStyle\ps@plain % Copy the plain style to customFooterStyle
\patchcmd{\ps@customFooterStyle}{\thepage}{{
    \color{gray}\textit{\small """ + personal_information["name"]["preferred_name"] + r""" - Page \thepage{} of \pageref*{LastPage}}
}}{}{}
\makeatother
\pagestyle{customFooterStyle}

\titleformat{\section}{\needspace{4\baselineskip}\bfseries\large}{}{0pt}{}[\vspace{1pt}\titlerule]

\titlespacing{\section}{
    % left space:
    -1pt
}{
    % top space:
    0.3 cm
}{
    % bottom space:
    0.2 cm
} % section title spacing

\renewcommand\labelitemi{$\circ$} % custom bullet points
\newenvironment{highlights}{
    \begin{itemize}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=0.4 cm + 10pt
    ]
}{
    \end{itemize}
} % new environment for highlights

\newenvironment{highlightsforbulletentries}{
    \begin{itemize}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=10pt
    ]
}{
    \end{itemize}
} % new environment for highlights for bullet entries


\newenvironment{onecolentry}{
    \begin{adjustwidth}{
        0.2 cm + 0.00001 cm
    }{
        0.2 cm + 0.00001 cm
    }
}{
    \end{adjustwidth}
} % new environment for one column entries

\newenvironment{twocolentry}[2][]{
    \onecolentry
    \def\secondColumn{#2}
    \setcolumnwidth{\fill, 4.5 cm}
    \begin{paracol}{2}
}{
    \switchcolumn \raggedleft \secondColumn
    \end{paracol}
    \endonecolentry
} % new environment for two column entries

\newenvironment{header}{
    \setlength{\topsep}{0pt}\par\kern\topsep\centering\linespread{1.5}
}{
    \par\kern\topsep
} % new environment for the header

\newcommand{\placelastupdatedtext}{% \placetextbox{<horizontal pos>}{<vertical pos>}{<stuff>}
  \AddToShipoutPictureFG*{% Add <stuff> to current page foreground
    \put(
        \LenToUnit{\paperwidth-2 cm-0.2 cm+0.05cm},
        \LenToUnit{\paperheight-1.0 cm}
    ){\vtop{{\null}\makebox[0pt][c]{
        \small\color{gray}\textit{""" + today + r"""}\hspace{\widthof{""" + today + r"""}}
    }}}%
  }
}%

% save the original href command in a new command:
\let\hrefWithoutArrow\href

% new command for external links:
\renewcommand{\href}[2]{\hrefWithoutArrow{#1}{\ifthenelse{\equal{#2}{}}{ }{#2 }\raisebox{.15ex}{\footnotesize \faExternalLink*}}}
"""))
    
def add_packages(doc, personal_information):
    doc.packages.append(Package('geometry', options=[
        'ignoreheadfoot',
        'top=2 cm',
        'bottom=2 cm',
        'left=2 cm',
        'right=2 cm',
        'footskip=1.0 cm'
    ]))
    doc.packages.append(Package(NoEscape('titlesec')))
    doc.packages.append(Package(NoEscape('tabularx')))
    doc.packages.append(Package(NoEscape('array')))
    doc.packages.append(Package('xcolor', options='dvipsnames'))
    doc.preamble.append(NoEscape(r'\definecolor{primaryColor}{RGB}{0, 79, 144}'))
    doc.packages.append(Package(NoEscape('enumitem')))
    doc.packages.append(Package(NoEscape('fontawesome5')))
    doc.packages.append(Package(NoEscape('amsmath')))
    doc.packages.append(Package('hyperref', options=[       # These variables are user's names
        f'pdftitle={{{personal_information["name"]["preferred_name"]}}}',
        f'pdfauthor={{{personal_information["name"]["preferred_name"]}}}',
        f'pdfcreator={{{personal_information["name"]["preferred_name"]}}}',
        'colorlinks=true',
        f'urlcolor={url_color}'
    ]))
    doc.packages.append(Package(NoEscape('eso-pic'), options='pscoord'))
    doc.packages.append(Package(NoEscape('calc')))
    doc.packages.append(Package(NoEscape('bookmark')))
    doc.packages.append(Package(NoEscape('lastpage')))
    doc.packages.append(Package(NoEscape('changepage')))
    doc.packages.append(Package(NoEscape('paracol')))
    doc.packages.append(Package(NoEscape('ifthen')))
    doc.packages.append(Package(NoEscape('needspace')))
    doc.packages.append(Package(NoEscape('iftex')))


def enable_ATS(doc):
    doc.preamble.append(NoEscape(r"""
\ifPDFTeX % making resume ATS readable
    \input{glyphtounicode}
    \pdfgentounicode=1
    % \usepackage[T1]{fontenc} % this breaks sb2nov
    \usepackage[utf8]{inputenc}
    \usepackage{lmodern}
\fi
"""))
    




# -----------------------------------------------------------------------------------
# resume parts
def add_new_section(doc, title):
    add_division(doc)
    doc.append(NoEscape("% "+ title))
    add_division(doc)
    doc.append(NoEscape(r"\section{" + title + "} %" + title.upper() + " SECTION" ))
    doc.append(NoEscape(r"\label{section:" + title + "}" ))

def add_division(doc):
    doc.append(NoEscape(r"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"))

# -----------------------------------------------------------------------------------
# format fields
def format_address(address, format):
    """
    Formats the given date object into various formats.

    Parameters
    ----------
    date : address
        A dictionary containing "address", "postal_code", "country", "state"
    format : str
        The desired format for the output string. Possible values:
        - "country"
        - "state, country"
        - "address, state"
        - "address, postal code, state"
    status : str
        A string used to indicate that the dates don't apply

    Returns
    -------
    str
        The formatted address string.
    """
    if format == "country":
        return f"{address["country"]}"
    if format == "state, country":
        return f"{address["state"]}, {address["country"]}"
    if format == "address, state":
        return f"{address["address"]}, {address["state"]}"
    if format == "address, postal_code, state":
        return f"{address["address"]}, {address["postal_code"]}, {address["state"]}"


def format_name(name, format):
    """
    Formats the given date object into various formats.

    Parameters
    ----------
    date : name
        A dictionary containing "first_name", "middle_name", "last_name", "full_name", "preferred_name"
    format : str
        The desired format for the output string. Possible values:
        - "preferred_name"
        - "full"
        - "last, first"
        - "last, Middle_initial. first"
        - "address, postal code, state"
    status : str
        A string used to indicate that the dates don't apply

    Returns
    -------
    str
        The formatted address string.
    """
    if format == "preferred_name":
        return name["preferred_name"]
    if format == "full":
        return f" {name["full_name"]}"
    if format == "last, first":
        return f"{name["last_name"]}, {name["first_name"]}"
    if format == "last, Middle_initial. first":
        return f"{name["last_name"]}, {name["middle_name"][0].upper()}. {name["first_name"]}"



def format_date(date: dict, format: str, status: str = "") -> str:
    """
    Formats the given date object into various formats.

    Parameters
    ----------
    date : dict
        A dictionary containing "year", "month", "day", and "season".
    format : str
        The desired format for the output string. Possible values:
        - "yyyy-mm-dd"
        - "mm-yy"
        - "month year"
        - "year"
        - "season"
    status : str
        A string used to indicate that the dates don't apply

    Returns
    -------
    str
        The formatted date string.
    """
    if not status == "": # str i.e. "in progress"
        return status
    
    year = date.get("year", "").strip()
    month = date.get("month", "").strip()
    day = date.get("day", "").strip()
    season = date.get("season", "").strip()

    if format == "yyyy-mm-dd":
        return f"{year}-{month}-{day}".replace("--", "-").strip("-")

    elif format == "mm-yy":
        return f"{month}-{year}".strip("-")

    elif format == "month year":
        return f"{month} {year}".strip()

    elif format == "year":
        return year

    elif format == "season":
        return season.strip()

    else:
        raise ValueError("Invalid format specified")

    
def escape_latex(text: str):
    return text.replace("#", r"\#")
# -----------------------------------------------------------------------------------

def produce_tex(doc, tex_file_dir, version_path, profile_name, version_name):
    doc.generate_tex(tex_file_dir)

def produce_pdf(doc, tex_file_dir, version_path, profile_name, version_name):
    try:
        subprocess.run(["pdflatex", "-output-directory", version_path, f"-jobname={profile_name}_{version_name}", tex_file_dir], check=True)
        print(f"PDF successfully created for {tex_file_dir}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during PDF generation: {e}")
    except FileNotFoundError:
        print("pdflatex not found. Make sure LaTeX is installed and added to your PATH.")


def generate_latex_with_pylatex(profile_json, version_path, profile_name, version_name):
    # Create a LaTeX document with specified options
    doc = Document(documentclass="article", document_options=["10pt", "letterpaper"])
    today_date = today
    today_formatted = today.strftime("%Y-%m-%d %H:%M:%S")

    # preambles
    add_packages(doc, profile_json["personal_information"])
    enable_ATS(doc)
    add_document_settings(doc, profile_json["personal_information"], today_formatted)

    # document content
    add_header(doc, profile_json["personal_information"])
    add_education(doc, profile_json["education"], "Education")
    add_experience(doc, profile_json["work_experience"])
    add_hard_skills(doc, profile_json["hard_skills"])
    add_projects(doc, profile_json["projects"])

    
    tex_file_dir = version_path + "/resume"
    produce_tex(doc, tex_file_dir, version_path, profile_name, version_name)
    produce_pdf(doc, tex_file_dir, version_path, profile_name, version_name)



# Call the function to create the file


def load_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def main():
    profiles_data = load_json('.\profiles\profiles.json')
    
    profile_name = "manuel_mares"
    version_name = "swe_english"
    profiles_path= "./profiles" 

    # get relevant information
    profile_json = profiles_path + "/" + profile_name + "/" + profile_name + ".json"
    version_path = profiles_path + "/" + profile_name + "/" + version_name

    
    manuel_mares_json = load_json(profile_json)
    print(manuel_mares_json["personal_information"])

    
    generate_latex_with_pylatex(profile_json=manuel_mares_json, version_path=version_path, profile_name=profile_name, version_name=version_name)

if __name__ == "__main__":
    main()
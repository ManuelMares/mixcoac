import json
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import NoEscape  # when inserting command (i.e. \color{}), NoEscape prevents this to be translated to \textEscape{}color{} 
from pylatex import Document, Package
from datetime import datetime
import subprocess
import os
import shutil

# Meta data variables
url_color = "primaryColor"
today=datetime.today()


# sections to include
sections = [
    {
        "section": "work_experience",
        "display_title": "Experience"
    },
    {
        "section": "hard_skills",
        "display_title": "Technologies"
    },
    {
        "section": "education",
        "display_title": "Education"
    },
    {
        "section": "projects",
        "display_title": "Project"
    },
]

# personal data settings
_DATE_FORMAT = "month year"
_ADDRESS_FORMAT = "state, country"
show_addresses = [0]
show_links = [0,1,2]
show_emails = [0]
show_phones = [0]
name_format = "preferred_name"
header_order = ["address", "email", "phone", "links"]


education_order = [2,1,0]
education_config_json = { # each element is a line
    "left_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
        [ # line 1
            {
                "text": "degree",
                "bold": True,
                "italics": False,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": ""   
            }
        ], 
        [ # line 2
            {
                "text": "institution",
                "bold": False,
                "italics": True,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": ""   
            }
        ]
    ],
    "right_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
    ]
}



experience_order = [1,0]
experience_config_json = { # each element is a line
    "left_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
        [ # line 1
            {
                "text": "job_title",
                "bold": True,
                "italics": False,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": ""    
            }
        ], 
        [ # line 2
            {
                "text": "company",
                "bold": False,
                "italics": True,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": "" 
            }
        ],
        [ # with bullet points, only 1 item is allowed
            {
                "text": "responsibilities",
                "bold": False,
                "italics": False,
                "bullets_order": [      # only apply to values that are arrays
                    [0,1,2], # for object 1
                    [0,2], # for object 2
                ],                          
                "trailing_symbol": "" 
            }
            
        ]
    ],
    "right_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
        [
            {
                "text": "location",
                "bold": False,
                "italics": True,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": "" 
            }
        ],
        [
            {
                "text": "start_date",
                "bold": False,
                "italics": True,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": " - " 
            },
            {
                "text": "end_date",
                "bold": False,
                "italics": True,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": "" 
            }
        ]
    ]
}


hard_skills_order = [1,0,2]
hard_skills_config_json = { # each element is a line
    "left_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
        [ # line 1
            {
                "text": "title",
                "bold": True,
                "italics": False,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": ":" 
            },
            {
                "text": "skills",
                "bold": False,
                "italics": True,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": "" 
            }
        ]
    ],
    "right_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
    ]
}


projects_order = [1,0,2]
projects_config_json = { # each element is a line
    "left_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
        [ # line 1
            {
                "text": "title",
                "bold": True,
                "italics": False,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": "" 
            }
        ],
        [ # line 2
            {
                "text": "technologies",
                "bold": True,
                "italics": True,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": "" 
            }
        ],
        [ # line 3
            {
                "text": "description",
                "bold": False,
                "italics": False,
                "bullets_order": [
                    [0,1],
                    [0,1],
                    [0,1]
                ],        # only apply to values that are arrays
                "trailing_symbol": "" 
            }
        ]
    ],
    "right_lines" : [ #  [[line1_item1, line1_item2, line1, item3, ...],  [line2_item1,...]]
        [ # line 1
            {
                "text": "link",
                "bold": False,
                "italics": False,
                "bullets_order": [],        # only apply to values that are arrays
                "trailing_symbol": "" 
            }
        ]
    ]
}




# =====================================================================================
# Settings Functions 
# =====================================================================================


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


# =====================================================================================
# Resume Functions 
# =====================================================================================
def add_header(doc, personal_information): # Add content to the document body
    add_sectionTitle_coment(doc, "Personal Information")
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
                    link_link = link["url"]
                    link_icon = link["icon"]
                    
                    if listedElements_counter > 0:
                        doc.append(NoEscape(r"""\AND"""))

                    doc.append(NoEscape(r"""\kern 0.25 cm%
                        \mbox{\hrefWithoutArrow{""" + link_link + r"""}{\color{black}{\footnotesize\fa""" + link_icon + r"""}\hspace*{0.13cm}""" + link_name + r"""}} % new link
                        \kern 0.25 cm%"""))        
                except:
                    continue

    doc.append(NoEscape(r"""\end{header}
    \vspace{0.3 cm - 0.3 cm}"""))


def add_section(doc, data_json, section_Name, section_order, section_config_json): # Add the Education section title
    add_new_section(doc, section_Name)

    # Loop through the universities and append their information
    for indexInPDF, objectIndex in enumerate(section_order):
        section_entry = data_json[objectIndex]
        doc.append(NoEscape(r"""    %---- New """ + section_Name + r"""----"""))

        # adding right side lines
        right_lines = section_config_json["right_lines"]
        if len(right_lines) > 0:
            doc.append(NoEscape(r"""    \begin{twocolentry}{ % start of double columns new """ + section_Name))
        else:
            doc.append(NoEscape(r"""    \begin{onecolentry} % start of single column new """ + section_Name))

        num_lines = len(section_config_json["right_lines"])
        counter = 1
        for rl in right_lines: # for each line
            formatted_text = "        " # guarantees all items are within same line
            for item in rl: # for each element in same line                        
                # open text styles
                if item["bold"]:
                    formatted_text += r"""\textbf{"""
                if item["italics"]:
                    formatted_text += r"""\textit{"""
                
                # add item
                item_text = item["text"]
                item_content = section_entry[item_text]
                if (type(item_content) is list) and not ("link" in item_text): # checking if element are bullet points (not link)
                    if len(item_content) > 0: #only if not empty list
                        bullet_order = item["bullets_order"][indexInPDF] # get the specific bullet point indicated in indexInPDF
                        formatted_text += r"\begin{highlights} % start bullet points"
                        formatted_text += "\n"
                        for bpIndex in bullet_order:
                            bp = item_content[bpIndex]
                            formatted_text += r"            \item " + escape_latex(bp) 
                            formatted_text += "\n"
                        formatted_text += r"        \end{highlights} % end bullet points"
                else:
                    if "date" in item_text:
                        formatted_text += format_date(date=item_content, format=_DATE_FORMAT)
                    elif "link" in item_text:
                        formatted_text += r"\textit{\href{" + item_content["url"] + r"}{" + item_content["name"] + r"}}"
                    else:
                        formatted_text += escape_latex(item_content)

                # close text styles
                if item["bold"]:
                    formatted_text += r"""}"""
                if item["italics"]:
                    formatted_text += r"""}"""

                # adding space between items
                formatted_text += item["trailing_symbol"] + " "

            # adding a new line for all lines except last one
            if counter < num_lines:
                if type(section_entry[section_config_json["right_lines"][counter][0]["text"]]) is list: # if next line (its first element) is bullet points, omit line jump
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
        num_lines = len(section_config_json["left_lines"])
        counter = 1
        for ll in section_config_json["left_lines"]: # for each line
            formatted_text = "        " # guarantees all items are within same line
            for item in ll: # for each element in same line
                # open text styles
                if item["bold"]:
                    formatted_text += r"""\textbf{"""
                if item["italics"]:
                    formatted_text += r"""\textit{"""
                
                # add item
                item_text = item["text"]
                item_content = section_entry[item_text]
                if (type(item_content) is list) and not ("link" in item_text): # checking if element are bullet points (not link)
                    if len(item_content) > 0: #only if not empty list
                        bullet_order = item["bullets_order"][indexInPDF]
                        formatted_text += r"\begin{highlights} % start bullet points"
                        formatted_text += "\n"
                        for bpIndex in bullet_order:
                            bp = item_content[bpIndex]
                            formatted_text += r"            \item " + escape_latex(bp) 
                            formatted_text += "\n"
                        formatted_text += r"        \end{highlights} % end bullet points"
                else:
                    if "date" in item_text:
                        formatted_text += format_date(date=item_content, format=_DATE_FORMAT)
                    elif "link" in item_text:
                        formatted_text += r"\textit{\href{" + item_content["url"] + r"}{" + item_content["name"] + r"}}"
                    else:
                        formatted_text += escape_latex(item_content)

                # close text styles
                if item["bold"]:
                    formatted_text += r"""}"""
                if item["italics"]:
                    formatted_text += r"""}"""
                    
                # adding space between items
                formatted_text += item["trailing_symbol"] + " "


            # adding a new line for all lines except last one
            if counter < num_lines:
                if type(section_entry[section_config_json["left_lines"][counter][0]["text"]]) is list: # if next line (its first element) is bullet points, omit line jump
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



    




# -----------------------------------------------------------------------------------
# resume parts
def add_new_section(doc, title):
    add_sectionTitle_coment(doc, title)
    doc.append(NoEscape(r"\section{" + title + "} %" + title.upper() + " SECTION" ))
    doc.append(NoEscape(r"\label{section:" + title.replace(" ", "_") + "}" ))

def add_sectionTitle_coment(doc, title):
    add_division(doc)
    doc.append(NoEscape("% "+ title))
    add_division(doc)

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
    today_formatted = today.strftime("%Y-%m-%d %H:%M:%S")

    # preambles
    add_packages(doc, profile_json["personal_information"])
    enable_ATS(doc)
    add_document_settings(doc, profile_json["personal_information"], today_formatted)

    # document content
    add_header(doc, profile_json["personal_information"])
    
    #content sections
    for section in sections:
        if section["section"] == "education":
            add_section(doc=doc, data_json=profile_json["education"], section_Name=section["display_title"], section_order=education_order, section_config_json=education_config_json)
        if section["section"] == "work_experience":
            add_section(doc=doc, data_json=profile_json["work_experience"], section_Name=section["display_title"], section_order=experience_order, section_config_json=experience_config_json)
        if section["section"] == "hard_skills":
            add_section(doc=doc, data_json=profile_json["hard_skills"], section_Name=section["display_title"], section_order=hard_skills_order, section_config_json=hard_skills_config_json)
        if section["section"] == "projects":
            add_section(doc=doc, data_json=profile_json["projects"], section_Name=section["display_title"], section_order=projects_order, section_config_json=projects_config_json)

    
    tex_file_dir = version_path + "/resume"
    produce_tex(doc, tex_file_dir, version_path, profile_name, version_name)

    # -------- !IMPORTANT ------------
    # pdf is produced twice
    # 1) to set the pdf size
    # 2) to determine the page numeration properly after the final size is reached (uses the alredy created .aux)
    produce_pdf(doc, tex_file_dir, version_path, profile_name, version_name)
    produce_pdf(doc, tex_file_dir, version_path, profile_name, version_name)



# Call the function to create the file


def load_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def delete_files_in_folder(folder_path):
    """Deletes all files within a specified folder.

    Args:
        folder_path: The path to the folder.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def main():
    profiles_data = load_json('.\profiles\profiles.json')
    
    profile_name = "manuel_mares"
    version_name = "swe_english"
    profiles_path= "./profiles" 

    # get relevant information
    profile_json = profiles_path + "/" + profile_name + "/" + profile_name + ".json"
    version_path = profiles_path + "/" + profile_name + "/" + version_name

    
    manuel_mares_json = load_json(profile_json)
    delete_files_in_folder(version_path)
    
    generate_latex_with_pylatex(profile_json=manuel_mares_json, version_path=version_path, profile_name=profile_name, version_name=version_name)

if __name__ == "__main__":
    main()
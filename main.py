import json
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import NoEscape  # when inserting command (i.e. \color{}), NoEscape prevents this to be translated to \textEscape{}color{} 
from pylatex import Document, Package
from datetime import datetime
import subprocess

# Meta data variables
url_color = "primaryColor"
today=datetime.today()

# Header variables
name = "Manuel Mares"
location = "507 Sweet Avenue"
email = "manuelms@nmsu.edu"
phone_number = "4237737734"
website = "https://yourwebsite.com/"
linkedin = "https://linkedin.com/in/yourusername"
github = "https://github.com/yourusername"
last_updated_text = f"Last updated in {today}"


# Education variables
universities = [
    {
        "dates": "Sept 2000 – May 2005",
        "name": "University of Pennsylvania",
        "degree": "BS in Computer Science",
        "gpa": "3.9/4.0",
        "link": "https://example.com",
        "coursework": "Computer Architecture, Comparison of Learning Algorithms, Computational Theory"
    },
    {
        "dates": "Sept 2005 – May 2009",
        "name": "Harvard University",
        "degree": "MS in Artificial Intelligence",
        "gpa": "4.0/4.0",
        "link": "https://anotherexample.com",
        "coursework": "Machine Learning, Neural Networks, Advanced Algorithms"
    }
]


# Experience
jobs = [
    {
        "location": "Cupertino, CA",
        "dates": "June 2005 – Aug 2007",
        "title": "Software Engineer",
        "company": "Apple",
        "highlights": [
            "Reduced time to render user buddy lists by 75\\% by implementing a prediction algorithm",
            "Integrated iChat with Spotlight Search by creating a tool to extract metadata from saved chat transcripts and provide metadata to a system-wide search database",
            "Redesigned chat file format and implemented backward compatibility for search"
        ]
    },
    {
        "location": "Redmond, WA",
        "dates": "June 2003 – Aug 2003",
        "title": "Software Engineer Intern",
        "company": "Microsoft",
        "highlights": [
            "Designed a UI for the VS open file switcher (Ctrl-Tab) and extended it to tool windows",
            "Created a service to provide gradient across VS and VS add-ins, optimizing its performance via caching",
            "Created a test case generation tool that creates random XML docs from XML Schema",
            "Automated the extraction and processing of large datasets from legacy systems using SQL and Perl scripts"
        ]
    }
]


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
        \textbf{\fontsize{24 pt}{24 pt}\selectfont """ + personal_information["name"]["preferred_name"] + r"""}

        \vspace{0.3 cm}

        \normalsize
        \mbox{{\color{black}\footnotesize\faMapMarker*}\hspace*{0.13cm}""" + format_date(personal_information["contact"]["addresses"][0]) + r"""}
        \kern 0.25 cm%
        \AND%
        \kern 0.25 cm%
        \mbox{\hrefWithoutArrow{mailto:""" + personal_information["contact"]["emails"][0] + r"""}{\color{black}{\footnotesize\faEnvelope[regular]}\hspace*{0.13cm}""" + personal_information["contact"]["emails"][0] + r"""}}%
        \kern 0.25 cm%
        \AND%
        \kern 0.25 cm%
        \mbox{\hrefWithoutArrow{tel:""" + personal_information["contact"]["phone_numbers"][0] + r"""}{\color{black}{\footnotesize\faPhone*}\hspace*{0.13cm}""" + personal_information["contact"]["phone_numbers"][0] + r"""}}"""))
    for link in personal_information["links"]:
        link_name = link["name"]
        link_link = link["link"]
        link_icon = link["icon"]
        doc.append(NoEscape(r"""\kern 0.25 cm%
            \AND
            \kern 0.25 cm%
            \mbox{\hrefWithoutArrow{""" + link_link + r"""}{\color{black}{\footnotesize\fa""" + link_icon + r"""}\hspace*{0.13cm}""" + link_name + r"""}}"""))

    doc.append(NoEscape(r"""\end{header}
    \vspace{0.3 cm - 0.3 cm}
    """))


def add_education(doc): # Add the Education section title
    doc.append(NoEscape(r"\section{Education}"))

    # Loop through the universities and append their information
    for uni in universities:
        doc.append(NoEscape(r"""
        \begin{twocolentry}{
            \textit{""" + uni["dates"] + r"""}
        }
            \textbf{""" + uni["name"] + r"""}

            \textit{""" + uni["degree"] + r"""}
        \end{twocolentry}

        \vspace{0.10 cm}

        \begin{onecolentry}
            \begin{highlights}
                \item GPA: """ + uni["gpa"] + r""" (\href{""" + uni["link"] + r"""}{a link to somewhere})
                \item \textbf{Coursework:} """ + uni["coursework"] + r"""
            \end{highlights}
        \end{onecolentry}
        """))


def add_experience(doc): # Add the Experience section title
    doc.append(NoEscape(r"\section{Experience}"))

    # Loop through the jobs and append their information
    for job in jobs:
        doc.append(NoEscape(r"""
    \begin{twocolentry}{
        \textit{""" + job["location"] + r"""}
        
        \textit{""" + job["dates"] + r"""}
    }
        \textbf{""" + job["title"] + r"""}
        
        \textit{""" + job["company"] + r"""}
    \end{twocolentry}

    \vspace{0.10 cm}

    \begin{onecolentry}
        \begin{highlights}
    """))

        # Loop through highlights for each job
        for highlight in job["highlights"]:
            doc.append(NoEscape(r"        \item " + highlight + r" "))

        doc.append(NoEscape(r"""
        \end{highlights}
    \end{onecolentry}

    \vspace{0.2 cm}
    """))

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
        \small\color{gray}\textit{Last updated in """ + today + r"""}
    }}}
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
\ifPDFTeX
    \input{glyphtounicode}
    \pdfgentounicode=1
    % \usepackage[T1]{fontenc} % this breaks sb2nov
    \usepackage[utf8]{inputenc}
    \usepackage{lmodern}
\fi
"""))
    






# -----------------------------------------------------------------------------------
# format fields
def format_date(address):
    print(address)
    return f"{address["address"]}, {address["postal_code"]}, {address["state"]}"
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
    add_education(doc)
    add_experience(doc)

    
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
import json
import os
from datetime import datetime

def create_ground_truth():
    """
    Create a comprehensive ground truth file for evaluating CV extraction with:
    - All provided real-world sample CVs
    - Multilingual support (English, French, Arabic)
    - Detailed education/experience structures
    - Standardized field formats
    - Complete skill categorization
    """
    
    ground_truth = {
        # English CVs
        "Richard_Sanchez_CV": {
            "name": "Richard Sanchez",
            "email": "hello@reallygreatsite.com",
            "phone": "+123-456-7890",
            "address": "123 Anywhere St., Any City",
            "linkedin": "www.linkedin.com/in/richard-sanchez",
            "education": [
                {
                    "degree": "Master of Business Management",
                    "institution": "Wardiere University",
                    "years": "2029-2030",
                    "gpa": "3.8/4.0"
                },
                {
                    "degree": "Bachelor of Business",
                    "institution": "Wardiere University",
                    "years": "2025-2029"
                }
            ],
            "experience": [
                {
                    "role": "Marketing Manager & Specialist",
                    "company": "Borcelle Studio",
                    "duration": "2030-Present",
                    "description": [
                        "Develop and execute comprehensive marketing strategies",
                        "Lead and manage high-performing marketing team",
                        "Monitor brand consistency across channels"
                    ]
                },
                {
                    "role": "Marketing Manager & Specialist",
                    "company": "Fauget Studio",
                    "duration": "2025-2029",
                    "description": [
                        "Create and manage marketing budget",
                        "Oversee market research",
                        "Monitor brand consistency"
                    ]
                }
            ],
            "skills": {
                "technical": [],
                "professional": [
                    "Project Management",
                    "Public Relations",
                    "Teamwork",
                    "Time Management",
                    "Leadership",
                    "Effective Communication",
                    "Critical Thinking"
                ]
            },
            "languages": [
                {"language": "English", "proficiency": "Fluent"},
                {"language": "French", "proficiency": "Fluent"},
                {"language": "German", "proficiency": "Basic"},
                {"language": "Spanish", "proficiency": "Intermediate"}
            ],
            "certifications": []
        },
        
        # French/Arabic CVs
        "Mohamed_Habib_Elsadkaoui_CV": {
            "name": "Elsadkaoui Mohamed Habib",
            "email": "mohamedhabibsadkaoui@gmail.com",
            "phone": "22725762",
            "address": "Bizerte, Tunisia",
            "linkedin": "linkedin.com/in/mohamed-habib-elsadkaoui",
            "education": [
                {
                    "degree": "Mastere en Electronique Electrotechnique et Automatique",
                    "institution": "Faculté des Sciences de Bizerte",
                    "years": "2022-Present"
                },
                {
                    "degree": "Licence national en Génie Electrique",
                    "institution": "Institut supérieure des études technologiques de Bizerte",
                    "years": "2019-2022"
                },
                {
                    "degree": "Baccalauréat en Science expérimentales",
                    "institution": "Lycée Farhat Hachad Bizerte",
                    "years": "2017-2019"
                }
            ],
            "experience": [
                {
                    "role": "Stage de Mémoire de fin d'études",
                    "company": "Elsentech",
                    "duration": "2023-2024",
                    "description": [
                        "Développement d'une solution d'interlock pour améliorer le processus de fabrication",
                        "Développement des interfaces python connectés à distance",
                        "Création d'une base de données SQL pour stockage des données",
                        "Développement d'une interface web avec Flask"
                    ]
                },
                {
                    "role": "Stage de fin d'études",
                    "company": "ELFOULETH",
                    "duration": "2022-2023",
                    "description": [
                        "Automatisation d'une machine de pliage de Fer",
                        "Programmation d'un automate S7-1200",
                        "Création d'une HMI pour visualiser le processus"
                    ]
                }
            ],
            "skills": {
                "technical": [
                    "Arduino",
                    "C++",
                    "C",
                    "Python",
                    "HTML/CSS",
                    "Processing/JAVA embarqué",
                    "Flask",
                    "SQL",
                    "TiaPortal",
                    "PSIM",
                    "TINKER CAD",
                    "ISIS",
                    "AutoCad"
                ],
                "professional": [
                    "Automatique industrielle",
                    "Réseaux industriels/API",
                    "Conception et simulation"
                ]
            },
            "languages": [
                {"language": "Français", "proficiency": "Courant"},
                {"language": "Arabe", "proficiency": "Native"},
                {"language": "Anglais", "proficiency": "Intermédiaire"}
            ],
            "certifications": []
        },

        "Salah_Ben_Thabet_CV": {
            "name": "Salah Ben Thabet",
            "email": "salah.benthabet@esprit.tn",
            "phone": "+216 58 401 835",
            "address": "Bizerte, Tunisie",
            "linkedin": "linkedin.com/in/salah-ben-thabet",
            "education": [
                {
                    "degree": "Cycle d'ingénieur en informatique",
                    "institution": "ESPRIT",
                    "years": "2022-Present"
                },
                {
                    "degree": "Licence en Technologies de l'Informatique",
                    "institution": "ISET Bizerte",
                    "years": "2019-2022"
                }
            ],
            "experience": [
                {
                    "role": "Stage d'ingénieur",
                    "company": "Attijari Bank",
                    "duration": "Juillet 2024 - Août 2024",
                    "description": [
                        "Mise en place d'une solution SIEM en intégrant ELK avec Wazuh et Suricata"
                    ]
                },
                {
                    "role": "Stage de fin d'études",
                    "company": "EL FOULADH",
                    "duration": "Février 2022 - Juin 2022",
                    "description": [
                        "Utilisation d'une carte Raspberry Pi pour création d'un système de supervision embarqué",
                        "Intégration de technologies ESP32 et Node-RED"
                    ]
                }
            ],
            "skills": {
                "technical": [
                    "ELK Stack",
                    "Wazuh",
                    "PFSense",
                    "Spring Boot",
                    ".NET",
                    "Java",
                    "Python",
                    "Nmap",
                    "MISP"
                ],
                "professional": [
                    "Cybersécurité",
                    "Threat Hunting",
                    "Security Monitoring"
                ]
            },
            "languages": [
                {"language": "Français", "proficiency": "Intermédiaire avancé (B2)"},
                {"language": "Anglais", "proficiency": "Intermédiaire avancé (B2)"}
            ],
            "certifications": []
        },

        "Louay_Sejine_CV": {
            "name": "Louay Sejine",
            "email": "louay.sejine@esprit.tn",
            "phone": "+216 94 472 246",
            "address": "Bizerte, Tunisie",
            "linkedin": "linkedin.com/in/louay-sejine",
            "education": [
                {
                    "degree": "Cycle d'ingénieur en Informatique",
                    "institution": "ESPRIT",
                    "years": "2022-Present"
                },
                {
                    "degree": "Licence en Génie Logiciel et Systèmes d'Informations",
                    "institution": "Faculté des Sciences de Bizerte",
                    "years": "2019-2022"
                }
            ],
            "experience": [
                {
                    "role": "Stage d'ingénieur",
                    "company": "I-way Tunisie",
                    "duration": "Juillet 2024 - Août 2024",
                    "description": [
                        "Contribution au développement de l'application mobile I-santé",
                        "Intégration d'une solution de gestion de soins médicaux avec Qt"
                    ]
                },
                {
                    "role": "Stage d'immersion",
                    "company": "OMMP Bizerte",
                    "duration": "Juillet 2023 - Août 2023",
                    "description": [
                        "Développement d'un backend de gestion des stagiaires avec Spring Boot",
                        "Optimisation de la base de données"
                    ]
                }
            ],
            "skills": {
                "technical": [
                    "Dart",
                    "Kotlin",
                    "Swift",
                    "Java",
                    "JavaScript",
                    "HTML",
                    "CSS",
                    "Flutter",
                    "Android",
                    "SwiftUI",
                    "React",
                    "Spring Boot",
                    ".NET"
                ],
                "professional": [
                    "Développement mobile",
                    "Applications cross-platform",
                    "UI/UX Design"
                ]
            },
            "languages": [
                {"language": "Français", "proficiency": "Intermédiaire avancé (B2)"},
                {"language": "Anglais", "proficiency": "Avancé (B2)"}
            ],
            "certifications": []
        },

        "Aziz_Ben_Ismail_CV": {
            "name": "Ben Ismail Med Aziz",
            "email": "medaziz.benismail@gmail.com",
            "phone": "+216 21 438 447",
            "address": "Tunis, Tunisie",
            "linkedin": "linkedin.com/in/aziz-ben-ismail",
            "education": [
                {
                    "degree": "Diplôme d'ingénieur en informatique",
                    "institution": "ESPRIT",
                    "years": "2019-2024"
                },
                {
                    "degree": "Baccalauréat scientifique",
                    "institution": "Lycée 2 mars",
                    "years": "2015-2019"
                }
            ],
            "experience": [
                {
                    "role": "Ingénieur Full-Stack Web",
                    "company": "Mutuelle de l'Armée Nationale",
                    "duration": "Nov 2024 - Jan 2025",
                    "description": [
                        "Développement d'applications web full-stack"
                    ]
                },
                {
                    "role": "Stage de fin d'études",
                    "company": "BeeCoders",
                    "duration": "Dec 2023 - Nov 2024",
                    "description": [
                        "Développement d'une Application Web pour la Centralisation des Centres de Formation"
                    ]
                }
            ],
            "skills": {
                "technical": [
                    "Java",
                    "React",
                    "Node.js",
                    "Spring Boot",
                    "SQL",
                    "Docker",
                    "Jenkins",
                    "Laravel",
                    "Git",
                    "UI/UX"
                ],
                "professional": [
                    "Full-Stack Development",
                    "DevOps",
                    "Agile Methodologies"
                ]
            },
            "languages": [
                {"language": "Français", "proficiency": "Courant"},
                {"language": "Anglais", "proficiency": "Avancé"},
                {"language": "Arabe", "proficiency": "Native"}
            ],
            "certifications": []
        },

        "Rihem_Berrahal_CV": {
            "name": "Rihem Berrahal",
            "email": "rihem.berrahal@fsb.ucar.tn",
            "phone": "+216 95 784 883",
            "address": "Ariana, Tunisie",
            "linkedin": "linkedin.com/in/rihem-berrahal",
            "education": [
                {
                    "degree": "Master's in Data Science",
                    "institution": "Faculty of Sciences, Bizerte",
                    "years": "2022-2024"
                },
                {
                    "degree": "Bachelor's Degree in Software Engineering",
                    "institution": "Faculty of Sciences, Bizerte",
                    "years": "2019-2022"
                }
            ],
            "experience": [
                {
                    "role": "End-of-studies Internship",
                    "company": "Agrivision",
                    "duration": "February 2024 - September 2024",
                    "description": [
                        "Developed intelligent model to analyze plant metrics using computer vision and YOLO",
                        "Integrated model into website using React and Flask with MongoDB"
                    ]
                },
                {
                    "role": "End-of-studies Internship",
                    "company": "Tunisair-Mobile",
                    "duration": "February 2022 - June 2022",
                    "description": [
                        "Developed mobile application with Flutter for flight tracking",
                        "Implemented real-time flight status updates",
                        "Integrated Google Maps for agency locations"
                    ]
                }
            ],
            "skills": {
                "technical": [
                    "Python (numpy, pandas, sklearn, keras, tensorflow)",
                    "Java",
                    "JavaScript",
                    "Flask",
                    "React",
                    "Angular",
                    "Spring Boot",
                    "Flutter",
                    "MongoDB",
                    "MySQL",
                    "PostgreSQL"
                ],
                "professional": [
                    "Machine Learning",
                    "Deep Learning",
                    "Computer Vision",
                    "Data Analysis"
                ]
            },
            "languages": [
                {"language": "English", "proficiency": "Advanced"},
                {"language": "French", "proficiency": "Advanced"}
            ],
            "certifications": [
                {
                    "name": "DP-900: Microsoft Azure Data Fundamentals",
                    "issuer": "Microsoft",
                    "year": "2024"
                },
                {
                    "name": "AZ-900: Microsoft Azure Fundamentals",
                    "issuer": "Microsoft",
                    "year": "2023"
                }
            ]
        },

        "Yasmin_Baghdadi_CV": {
            "name": "Baghdadi Yasmin",
            "email": "yasminbaghdadi22@gmail.com",
            "phone": "+216 20309699",
            "address": "Nabeul, Tunisie",
            "linkedin": "linkedin.com/in/yassmin-baghdadi",
            "education": [
                {
                    "degree": "Licence en Ingénierie des Systèmes Informatiques",
                    "institution": "Faculté des Sciences - Sfax",
                    "years": "2022-Present",
                    "specialization": "Internet des objets et systèmes embarqués"
                },
                {
                    "degree": "Baccalauréat en Sciences Expérimentales",
                    "institution": "Lycée 2 Mars 1934 - Korba",
                    "years": "2021-2022"
                }
            ],
            "experience": [
                {
                    "role": "Stage d'initiation",
                    "company": "Designet Web Agency",
                    "duration": "Juillet 2023 - Août 2023",
                    "description": [
                        "Conception et développement d'une plateforme de gestion de stock",
                        "Intégration d'un système d'authentification sécurisé",
                        "Technologies: Laravel, MySQL, HTML/CSS/JavaScript"
                    ]
                }
            ],
            "skills": {
                "technical": [
                    "Java",
                    "Python",
                    "C++",
                    "JavaScript",
                    "Kotlin",
                    "HTML",
                    "CSS",
                    "PHP",
                    "XML",
                    "VHDL",
                    "Laravel",
                    "Spring Boot",
                    "Angular",
                    "Arduino",
                    "Raspberry Pi"
                ],
                "professional": [
                    "Machine Learning",
                    "Big Data",
                    "IoT Development",
                    "Embedded Systems"
                ]
            },
            "languages": [
                {"language": "Arabe", "proficiency": "Langue maternelle"},
                {"language": "Français", "proficiency": "Courant"},
                {"language": "Anglais", "proficiency": "Intermédiaire"}
            ],
            "certifications": []
        },

        "Ayoub_Trabelsi_CV": {
            "name": "Trabelsi Ayoub",
            "email": "Zhana.ayoub@gmail.com",
            "phone": "55 523 017",
            "address": "Zhana Utique Bizerte, 7060",
            "linkedin": "linkedin.com/in/ayoub-trabelsi",
            "education": [
                {
                    "degree": "Licence en ingénierie des systèmes informatique",
                    "institution": "ISSATSO, SOUSSE",
                    "years": "2021-2025",
                    "specialization": "IoT et systèmes embarqués"
                },
                {
                    "degree": "Baccalauréat informatique",
                    "institution": "Lycée Utique",
                    "years": "2020-2021"
                }
            ],
            "experience": [],
            "skills": {
                "technical": ["Python", "Java", "C", "Réseaux", "Développement mobile", "Développement web"],
                "professional": []
            },
            "languages": [
                {"language": "Arabe", "proficiency": "Native"},
                {"language": "Français", "proficiency": "Courant"},
                {"language": "Anglais", "proficiency": "Intermédiaire"},
                {"language": "Italien", "proficiency": "Débutant"}
            ],
            "certifications": [
                {
                    "name": "Cisco Networking Basics",
                    "issuer": "CISCO",
                    "year": "2024",
                    "description": "Concepts fondamentaux de la mise en réseau"
                },
                {
                    "name": "Cisco Introduction to Packet Tracer",
                    "issuer": "CISCO",
                    "year": "2024",
                    "description": "Maîtrise de l'outil de simulation réseau Packet Tracer"
                }
            ]
        },

        "Heni_Rebhi_CV": {
            "name": "Heni Rebhi",
            "email": "heni.rebhi@esprit.tn",
            "phone": "+216 56 084 030",
            "address": "Bizerte, Tunisie",
            "linkedin": "linkedin.com/in/heni-rebhi",
            "education": [
                {
                    "degree": "Cycle d'ingénieur en informatique",
                    "institution": "ESPRIT",
                    "years": "2022-Present"
                },
                {
                    "degree": "Licence en Génie Éléctrique",
                    "institution": "ISET Nabeul",
                    "years": "2019-2022"
                }
            ],
            "experience": [
                {
                    "role": "Stage d'immersion en entreprise",
                    "company": "SAMM AUTOMATION",
                    "duration": "Juillet 2023 - Août 2023",
                    "description": [
                        "Développement d'un site web de gestion des réclamations des ouvriers",
                        "Technologies: PHP, Bootstrap"
                    ]
                },
                {
                    "role": "Stage de fin d'études",
                    "company": "RAI: Relais Et Automatismes Industriels",
                    "duration": "Février 2022 - Juin 2022",
                    "description": [
                        "Mise en place d'un banc de test pour câbles électroniques",
                        "Intégration d'un automate programmable et interface HMI"
                    ]
                }
            ],
            "skills": {
                "technical": [
                    "C",
                    "C#",
                    "Java",
                    "JavaScript",
                    "Python",
                    "HTML",
                    "CSS",
                    "Android",
                    "Spring Boot",
                    ".NET",
                    "Arduino",
                    "TIA Portal",
                    "STM32",
                    "ESP32",
                    "Raspberry Pi"
                ],
                "professional": [
                    "Électronique et automatisation",
                    "Microcontrôleurs",
                    "RTOS"
                ]
            },
            "languages": [
                {"language": "Français", "proficiency": "Intermédiaire avancé (B2)"},
                {"language": "Anglais", "proficiency": "Intermédiaire (B1)"}
            ],
            "certifications": []
        },

        "Sleheddine_Dhaouadi_CV": {
            "name": "Sleheddine Dhaouadi",
            "email": "sieheddine.dhaouadi@esprit.tn",
            "phone": "+216 55 611 443",
            "address": "Bizerte, Tunisie",
            "linkedin": "linkedin.com/in/dhaouadi-sieheddine",
            "education": [
                {
                    "degree": "Cycle d'ingénieur en informatique",
                    "institution": "ESPRIT",
                    "years": "2022-2025"
                },
                {
                    "degree": "Licence en Technologies de l'Information et de Communication",
                    "institution": "Faculté des Sciences, Bizerte",
                    "years": "2019-2022"
                }
            ],
            "experience": [
                {
                    "role": "Stage d'ingénieur",
                    "company": "NeoLedge",
                    "duration": "Juillet 2024 - Septembre 2024",
                    "description": [
                        "Déploiement et configuration de Zabbix pour surveillance des indicateurs de performance",
                        "Intégration à l'infrastructure existante pour surveillance continue"
                    ]
                },
                {
                    "role": "Stage d'immersion en entreprise",
                    "company": "Playpals Studio",
                    "duration": "Juin 2023 - Juillet 2023",
                    "description": [
                        "Développement d'un jeu sur la plateforme ROBLOX",
                        "Technologies: Blender, MIXAMO, LUA"
                    ]
                }
            ],
            "skills": {
                "technical": [
                    "PFSense",
                    "OpenSense",
                    "IDS/IPS",
                    "Wazuh",
                    "ELK Stack",
                    "IRIS",
                    "Zabbix",
                    "Java",
                    "JavaScript",
                    "HTML",
                    "CSS",
                    "Python",
                    "C#",
                    "Spring Boot",
                    ".NET"
                ],
                "professional": [
                    "Cybersécurité",
                    "Surveillance réseau",
                    "Gestion des risques"
                ]
            },
            "languages": [
                {"language": "Français", "proficiency": "Courant (B2)"},
                {"language": "Anglais", "proficiency": "Courant (B2)"}
            ],
            "certifications": []
        }
    }

    # Add metadata about the ground truth dataset
    metadata = {
        "creation_date": datetime.now().isoformat(),
        "version": "2.0",
        "total_cvs": len(ground_truth),
        "languages": ["English", "French", "Arabic"],
        "fields": {
            "required": ["name", "email", "phone", "education", "skills"],
            "optional": ["address", "linkedin", "experience", "certifications", "languages"]
        },
        "evaluation_metrics": ["precision", "recall", "f1_score", "field_completeness"]
    }

    # Create output directory if it doesn't exist
    os.makedirs('evaluation_data', exist_ok=True)

    # Save JSON ground truth with metadata
    output_path = os.path.join('evaluation_data', 'ground_truth_v2.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "metadata": metadata,
            "cvs": ground_truth
        }, f, indent=4, ensure_ascii=False)

    print(f"✅ Created enhanced ground truth file: {output_path}")

    # Create sample CVs directory with actual content
    os.makedirs('sample_cvs', exist_ok=True)
    for cv_id, cv_data in ground_truth.items():
        if cv_id == "Template_CV":
            continue
            
        text_path = os.path.join('sample_cvs', f'{cv_id}.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            # Generate semi-realistic CV text content
            f.write(f"=== {cv_data['name']} ===\n\n")
            f.write(f"Contact: {cv_data.get('phone', '')} | {cv_data.get('email', '')}\n")
            if 'address' in cv_data:
                f.write(f"Address: {cv_data['address']}\n")
            if 'linkedin' in cv_data:
                f.write(f"LinkedIn: {cv_data['linkedin']}\n\n")
            
            f.write("=== EDUCATION ===\n")
            for edu in cv_data['education']:
                f.write(f"{edu['degree']} | {edu['institution']} | {edu['years']}\n")
                if 'gpa' in edu:
                    f.write(f"GPA: {edu['gpa']}\n")
                if 'specialization' in edu:
                    f.write(f"Specialization: {edu['specialization']}\n")
                f.write("\n")
            
            if 'experience' in cv_data and cv_data['experience']:
                f.write("=== EXPERIENCE ===\n")
                for exp in cv_data['experience']:
                    f.write(f"{exp['role']} | {exp['company']} | {exp['duration']}\n")
                    for desc in exp['description']:
                        f.write(f"- {desc}\n")
                    f.write("\n")
            
            f.write("=== SKILLS ===\n")
            if 'skills' in cv_data:
                if cv_data['skills']['technical']:
                    f.write("Technical: " + ", ".join(cv_data['skills']['technical']) + "\n")
                if cv_data['skills']['professional']:
                    f.write("Professional: " + ", ".join(cv_data['skills']['professional']) + "\n")
            
            if 'languages' in cv_data:
                f.write("\n=== LANGUAGES ===\n")
                f.write(", ".join([f"{lang['language']} ({lang['proficiency']})" 
                                 for lang in cv_data['languages']]) + "\n")
            
            if 'certifications' in cv_data and cv_data['certifications']:
                f.write("\n=== CERTIFICATIONS ===\n")
                for cert in cv_data['certifications']:
                    f.write(f"{cert['name']} | {cert['issuer']} | {cert['year']}\n")

    print("✅ Created realistic sample CV text files in sample_cvs directory")

if __name__ == "__main__":
    create_ground_truth()
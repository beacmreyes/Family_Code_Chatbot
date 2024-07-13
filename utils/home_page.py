def page_details(language):

    pages = {
        "English": {
            "title": "PAMiLYA: Philippine Family Law Chatbot - Empowering Access to Legal Help",
            "about": "About the App",
            "description": "In the Philippines, many underprivileged families face legal issues but cannot readily afford the high costs associated with legal assistance. PAMiLYA, a database of family relations related legal cases and resolutions, aims to bridge this gap. It offers free and accessible pre-legal consultation related to family law, aiding families, students, lawmakers, law enforcers, societal organizations, and law enthusiasts in gaining awareness and understanding of Philippine Family Law. This initiative also aims to assist Barangay officials or LGU units in providing necessary legal counsel to resolve family conflicts or disputes. PAMiLYA seeks to empower families and communities by providing clear, understandable guidance on their rights and legal options.",
            "how_to": "How to Use the App",
            "how_to_use": """
            1. Select the query language: "English" or "Filipino".
            2. Enter your query.
            3. Press 'enter'.
            4. Output will consist of related articles from the family code as well as an answer to the query based on the related articles.
            5. For supplemental reading, refer to the last section for related cases.
            """,
            "limitations_header": "Limitations of the App",
            "limitations": """
            1. Chatbot is only as up to date as the latest database update. The database for this app needs updating whenever the Family Code is ammended.
            2. The app requires internet connection to function.
            3. This chatbot serves as a pre-consultation tool and does not substitute professional legal advice. Users are still advised to consult qualified lawyers for formal legal assistance.
            """,
            "citations": """
            1. Senate and House of Representatives. (1987). Executive Order No. 209, s. 1987 - The Family Code of the Philippines. Official Gazette of the Republic of the Philippines. Retrieved from https://www.officialgazette.gov.ph/1987/07/06/executive-order-no-209-s-1987/
            2. Senate and House of Representatives. (1989). Republic Act No. 6809 - AN ACT LOWERING THE AGE OF MAJORITY FROM TWENTY-ONE TO EIGHTEEN YEARS. Judiciary of the Philippines. Retrieved from https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/7025
            3. Senate and House of Representatives. (2004). Republic Act No. 9255 - AN ACT ALLOWING ILLEGITIMATE CHILDREN TO USE THE SURNAME OF THEIR FATHER. Judiciary of the Philippines. Retrieved from https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/277
            4. Senate and House of Representatives. (2009). Republic Act No. 8552 - AN ACT PROVIDING FOR THE LEGITIMATION OF CHILDREN BORN TO PARENTS BELOW MARRYING AGE. Judiciary of the Philippines. Retrieved from https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/17263
            5.Senate and House of Representatives. (2013). Republic Act No. 10572 - AN ACT ESTABLISHING THE LIABILITY OF THE ABSOLUTE COMMUNITY OR CONJUGAL PARTNERSHIP FOR AN OBLIGATION OF A SPOUSE WHO PRACTICES A PROFESSION AND THE CAPABILITY OF EITHER SPOUSE TO DISPOSE OF AN EXCLUSIVE PROPERTY WITHOUT THE CONSENT OF THE OTHER SPOUSE. Judiciary of the Philippines. Retrieved from https://elibrary.judiciary.gov.ph/assets/dtSearch/dtSearch_system_files/dtisapi6.dll?cmd=getdoc&DocId=16499&Index=*2ceb34621b4a207c3a52af138f1e7bbf&HitCount=6&hits=59+5a+74+75+f9+fa+&SearchForm=C%3A%5Celibrev2%5Csearch%5Csearch_form
            6. UST Faculty. (2021). Persons and Family Relations. Retrieved from https://www.ustcivillaw.com/wp-content/uploads/2021/08/Persons-and-Family-Relations_HVNj62YQuGoFTpNVUVNb.pdf
            """
        },
        "Filipino": {
            "title": "PAMiLYA: Chatbot para sa Philippine Family Law - Pinapaigtingin Makamit ang Tulong Legal",
            "about": "Tungkol sa App",
            "description": "Sa Pilipinas, maraming pamilyang mahihirap ang hinaharap ang mga isyung legal ngunit hindi agad makakaya ang mataas na gastos na kaakibat ng tulong legal. Ang PAMiLYA, isang database ng mga kaso at resolusyon sa batas pamilya, ay nilikha upang punan ang agwat na ito. Nag-aalok ito ng libre at abot-kayang konsultasyon bago mag-legal na nauugnay sa batas pamilya, tumutulong sa mga pamilya, mag-aaral, mga mambabatas, mga tagapagtupad ng batas, mga organisasyon sa lipunan, at mga tagahanga ng batas na maunawaan ang batas pamilya sa Pilipinas. Layunin din nito ang pagtulong sa mga opisyal ng Barangay o mga yunit ng LGU sa pagbibigay ng kaukulang payo legal upang lutasin ang mga alitan o labanang pamilya. Ang PAMiLYA ay layuning palakasin ang mga pamilya at komunidad sa pamamagitan ng malinaw at maaunawaang patnubay tungkol sa kanilang mga karapatan at legal na mga pagpipilian.",
            "how_to": "Paano Gamitin and App",
            "how_to_use": """
            1. Pumili ng wika ng katanungan: "Ingles" o "Filipino".
            2. Ilagay ang iyong katanungan.
            3. Pindutin ang 'enter'.
            4. Ang output ay maglalaman ng mga kaugnay na artikulo mula sa Family Code pati na rin ang sagot sa katanungan batay sa mga kaugnay na artikulo.
            5. Para sa karagdagang pagbasa, tingnan ang huling seksyon para sa mga kaugnay na kaso.
            """,
            "limitations_header": "Limitasyon ng App",
            "limitations": """
            1. Ang Chatbot ay kasing updated lamang ng pinakahuling update ng database. Ang database para sa app na ito ay kailangang i-update tuwing may mga pagbabago sa Family Code.
            2. Ang app ay nangangailangan ng internet connection upang mag-function.
            3. Ang chatbot na ito ay naglilingkod bilang isang pre-consultation tool at hindi pumalit sa propesyonal na legal na payo. Muling pinapayuhan ang mga gumagamit na kumunsulta sa mga lisensyadong abogado para sa opisyal na legal na tulong.
            """,
            "citations": """
            1. Senate and House of Representatives. (1987). Executive Order No. 209, s. 1987 - The Family Code of the Philippines. Official Gazette of the Republic of the Philippines. Retrieved from https://www.officialgazette.gov.ph/1987/07/06/executive-order-no-209-s-1987/
            2. Senate and House of Representatives. (1989). Republic Act No. 6809 - AN ACT LOWERING THE AGE OF MAJORITY FROM TWENTY-ONE TO EIGHTEEN YEARS. Judiciary of the Philippines. Retrieved from https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/7025
            3. Senate and House of Representatives. (2004). Republic Act No. 9255 - AN ACT ALLOWING ILLEGITIMATE CHILDREN TO USE THE SURNAME OF THEIR FATHER. Judiciary of the Philippines. Retrieved from https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/277
            4. Senate and House of Representatives. (2009). Republic Act No. 8552 - AN ACT PROVIDING FOR THE LEGITIMATION OF CHILDREN BORN TO PARENTS BELOW MARRYING AGE. Judiciary of the Philippines. Retrieved from https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/17263
            5.Senate and House of Representatives. (2013). Republic Act No. 10572 - AN ACT ESTABLISHING THE LIABILITY OF THE ABSOLUTE COMMUNITY OR CONJUGAL PARTNERSHIP FOR AN OBLIGATION OF A SPOUSE WHO PRACTICES A PROFESSION AND THE CAPABILITY OF EITHER SPOUSE TO DISPOSE OF AN EXCLUSIVE PROPERTY WITHOUT THE CONSENT OF THE OTHER SPOUSE. Judiciary of the Philippines. Retrieved from https://elibrary.judiciary.gov.ph/assets/dtSearch/dtSearch_system_files/dtisapi6.dll?cmd=getdoc&DocId=16499&Index=*2ceb34621b4a207c3a52af138f1e7bbf&HitCount=6&hits=59+5a+74+75+f9+fa+&SearchForm=C%3A%5Celibrev2%5Csearch%5Csearch_form
            6. UST Faculty. (2021). Persons and Family Relations. Retrieved from https://www.ustcivillaw.com/wp-content/uploads/2021/08/Persons-and-Family-Relations_HVNj62YQuGoFTpNVUVNb.pdf
            """
        }
    }

    return pages



    

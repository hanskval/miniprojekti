*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Go To  ${RESET_URL}

*** Test Cases ***
At start there are no citations
    Go To  ${HOME_URL}
    Get Title  ==  Citation
    Get Text  body  not contains  Meikäläinen
    Go To  ${RESET_URL}

After adding a book citation it is shown on the front page
    Create Book Citation
    Go To  ${HOME_URL}
    Get Text  body  *=  Ohjelmistotuotanto
    Get Text  body  *=  Matti Meikäläinen
    Go To  ${RESET_URL}

After adding a book citation, citation table exists and has one citation
    Go To  ${RESET_URL}
    Create Book Citation
    Go To  ${DATA_URL}
    Get Text  body  *=  Ohjelmistotuotanto
    Get Text  body  *=  Matti Meikäläinen
    Get Element Count  id=citation_list  ==  1
    ${rows}=  Get Element Count  css=#citation_list tr
    Should Be Equal As Integers  ${rows}  2
    Go To  ${RESET_URL}

After adding an article citation, its fields are shown when filtered
    Create Article Citation
    Go To  ${DATA_URL}?type=article
    Get Text  body  *=  A Journal
    Get Text  body  *=  20-30
    Get Text  css=#citation_list tr:first-child th:nth-child(1)  ==  Title
    Get Text  css=#citation_list tr:first-child th:nth-child(4)  ==  Journal
    Go To  ${RESET_URL}

Citation table has correct headers and four columns
    Go To  ${DATA_URL}
    ${columns}=  Get Element Count  css=#citation_list tr:first-child th
    Should Be Equal As Integers  ${columns}  4
    Table Should Have Headers
    Go To  ${RESET_URL}

Create citation button exists
    Go To  ${DATA_URL}
    Get Element Count  id=new_citation_button  ==  1
    Go To  ${RESET_URL}

Download all citations button exists
    Go To  ${DATA_URL}
    Get Element Count  id=download_all_citations_button  ==  1
    Go To  ${RESET_URL}

Home button exists
    Go To  ${DATA_URL}
    Get Element Count  id=home_button  ==  1
    Go To  ${RESET_URL}

*** Keywords ***

Create Book Citation
    Go To  ${HOME_URL}
    Click  text=Create new citation
    Fill Text  css=#book-author     Matti Meikäläinen
    Fill Text  css=#book-title      Ohjelmistotuotanto
    Fill Text  css=#book-year       2026
    Fill Text  css=#book-publisher  Gaudeamus
    Click  css=details[open] button

Create Article Citation
    Go To  ${HOME_URL}
    Click  text=Create new citation
    Click  text=Article citation
    Fill Text  css=#article-author   A Writer
    Fill Text  css=#article-title    An Article
    Fill Text  css=#article-year     2025
    Fill Text  css=#article-journal  A Journal
    Fill Text  css=#article-volume   12
    Fill Text  css=#article-issue    3
    Fill Text  css=#article-pages    20-30
    Click  css=details[open] button

Table Should Have Headers
    Get Text  css=#citation_list tr:first-child th:nth-child(1)  ==  Title
    Get Text  css=#citation_list tr:first-child th:nth-child(2)  ==  Author
    Get Text  css=#citation_list tr:first-child th:nth-child(3)  ==  Year
    Get Text  css=#citation_list tr:first-child th:nth-child(4)  ==  Publisher
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

After adding a book citation it is shown on the front page
    Go To  ${HOME_URL}
    Click  text=Create new citation
    Fill Text  [name="author"]     Matti Meikäläinen
    Fill Text  [name="title"]      Ohjelmistotuotanto
    Fill Text  [name="year"]       2026
    Fill Text  [name="publisher"]  Gaudeamus
    Click  button >> text=Create
    Get Text  body  *=  Ohjelmistotuotanto
    Get Text  body  *=  Matti Meikäläinen
*** Settings ***
Library    SeleniumLibrary


*** Variables ***
${wikipedia login}    RobotTests
${wikipedia correct password}    RobotFramework
${wikipedia wrong password}    12345


*** Keywords ***
Login wikipedia
    [Arguments]    ${login}    ${password}
    open browser    https://pl.wikipedia.org/    chrome
    maximize browser window
    wait until element is visible    pt-login-2    1
    click element    pt-login-2
    wait until element is visible    wpName1    1
    input text    wpName1    ${login}
    wait until element is visible    wpPassword1    1
    input password    wpPassword1     ${password}
    checkbox should not be selected    wpRemember
    select checkbox    wpRemember
    click button    wpLoginAttempt


*** Test Cases ***
Successful Login Wikipedia
    Login wikipedia    ${wikipedia login}    ${wikipedia correct password}
    wait until element is visible    pt-userpage-2    3
    ${username}    get text    pt-userpage-2
    log to console    Zalogowany uzytkownik: ${username}
    log    Zalogowany uzytkownik: ${username}
    should be equal     ${username}    ${wikipedia login}
    close browser

Non-succesful login wikipedia
    Login wikipedia    ${wikipedia login}    ${wikipedia wrong password}
    

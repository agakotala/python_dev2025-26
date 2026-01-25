*** Settings ***
Library    SeleniumLibrary


*** Variables ***
${wikipedia login}    RobotTests
${wikipedia correct password}    RobotFramework
${wikipedia wrong password}    12345


*** Keywords ***



*** Test Cases ***
Successful Login Wikipedia
    open browser    https://pl.wikipedia.org/    chrome
    sleep    1
    maximize browser window
    sleep    1
    click element    pt-login-2
    sleep    1
    input text    wpName1    ${wikipedia login}
    sleep    1
    input password    wpPassword1     ${wikipedia correct password}
    sleep    1
    checkbox should not be selected    wpRemember
    select checkbox    wpRemember
    sleep    1
    click button    wpLoginAttempt
    sleep    1
    wait until element is visible    pt-userpage-2    3
    ${username}    get text    pt-userpage-2
    log to console    Zalogowany uzytkownik: ${username}
    log    Zalogowany uzytkownik: ${username}
    should be equal     ${username}    ${wikipedia login}
    sleep    3
    close browser

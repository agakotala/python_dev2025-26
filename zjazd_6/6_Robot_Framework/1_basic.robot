*** Settings ***
Library    SeleniumLibrary


*** Variables ***
${wikipedia login}    RobotTests
${wikipedia correct password}    RobotFramework
${wikipedia wrong password}    12345
${error message}    Podany login lub hasło są nieprawidłowe. Spróbuj jeszcze raz.


*** Keywords ***
test setup
    open browser    https://pl.wikipedia.org/    chrome
    maximize browser window

test teardown
    capture page screenshot    ../screens/My_Screen-{index}.png
    close browser
    sleep    3

Login wikipedia
    [Arguments]    ${login}    ${password}
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
    run keyword and ignore error    wait until element is visible    pt-userpage-2    5
    ${username}    get text    pt-userpage-2
    log to console    Zalogowany uzytkownik: ${username}
    log    Zalogowany uzytkownik: ${username}
    should be equal     ${username}    ${wikipedia login}

Non-succesful login wikipedia
    Login wikipedia    ${wikipedia login}    ${wikipedia wrong password}
    wait until element is visible        xpath:/html/body/div[3]/div/div[3]/main/div[3]/div[3]/div[3]/div/form/div[1]/div      3
    ${my error message}    get text      xpath:/html/body/div[3]/div/div[3]/main/div[3]/div[3]/div[3]/div/form/div[1]/div
    should be equal    ${error message}    ${my error message}
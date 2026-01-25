*** Variables ***
${string}    piesek
@{list}    pierwszy    drugi    trzeci    czwarty    piaty
@{list of numbers}    1    2    3    4    5
&{dictionary}    slowo=${string}    numer=30    lista=@{list}
@{imiona}    Krzysztof    Dariusz    Joanna    Justyna
@{nazwiska}    Nowak    Malinowski    Kowalska    Lewandowska

*** Test Cases ***
For loops in Range
    FOR    ${i}    IN RANGE    5
        log    ${i}
        IF    ${i} == 3    log    wypisuje ${i}
    END
    log    koniec petli 1

    FOR  ${i}  IN RANGE  2    17    5
        log    ${i}
    END
    log    koniec petli 2

For loop in range with index
    FOR    ${i}    IN RANGE    4
        log to console    uzytkownik: ${imiona}[${i}] ${nazwiska}[${i}]
    END



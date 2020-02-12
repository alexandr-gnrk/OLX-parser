# OLX parser
Programm that parse full ads infromation (including contacts) from [olx.ua](https://www.olx.ua/ "olx.ua") and saves it in JSON format.

## Setup
Clone the repository and install requirements from ```requirements.txt```.

Go to the ```main.py``` and replace search link as needed on 4th line. 

For instance, it could be:
- a category link https://www.olx.ua/zhivotnye/
- a subcategory link https://www.olx.ua/zhivotnye/sobaki/
- a query link https://www.olx.ua/list/q-bass-guitar/
- any  [olx.ua](https://www.olx.ua/ "olx.ua") link that returns list of advertisments

Run ```main.py```, output should be like this:


    Start parsing https://www.olx.ua/elektronika/
    ###################################[ Page 1 ]###################################
    ------------------------------------ Ad #1 -------------------------------------
    Title:		Лазер крест, точка.
    Location:	Запорожье, Запорожская область, Шевченковский
    Ad details:	Опубликовано с мобильного в 20:57, 9 февраля 2020, Номер объявления: 521729194
    Contacts:	['068 xxx 1180']
    Description:	Лазер новый, мощность 150 мВт, длина волны 648nM, напряжение 5V, рабочий ток 210 мА.
    Рабочая температура + - 50'С.
    Ресурс работы...
    URL:		https://www.olx.ua/obyavlenie/lazer-krest-tochka-IDzj7B0.html#4c76411eb6;promoted
    
    ------------------------------------ Ad #2 -------------------------------------
    Title:		ЗАРЯДКА USB на/для/к iPhone11Pro10XS Max8XR7+6S5C4iPad3mini2мини1Айпад
    Location:	Киев, Киевская область, Голосеевский
    Ad details:	Добавлено: в 18:15, 24 января 2020, Номер объявления: 525284910
    Contacts:	['063 xxx 3999', '067 xxx 4433', '095 xxx 9444']
    Description:	Apple 5W USB Power Adapter MD813ZM/A в коробке = 199.99 грн.
    
    Гарантия 6 месяцев!
    
    Технические характеристики:
    Apple USB Power A...
    URL:		https://www.olx.ua/obyavlenie/zaryadka-usb-na-dlya-k-iphone11pro10xs-max8xr7-6s5c4ipad3mini2mini1aypad-IDzy2Bg.html#4c76411eb6;promoted

Press ```Ctrl+C``` to end parsing and save all changes into file ```ads.json``` in current directory.

# Пример tornado приложения для работы с firebase

Мобильное приложение при старте запрашивает список items доступный для выбора.
После выбора item, мобильное приложение отправляет в web приложение токен и item.
При появлении новой информации по item web приложение нотифицирует все мобильные
приложения, подписанные на данный item.

Список items захардкожен, информация о подписанных мобильных устройствах хранится
в памяти, payload и аттрибуты нотификации захардкоженны.

Для разработки нужно создать файл config.yaml в корне по образцу config.yaml.example
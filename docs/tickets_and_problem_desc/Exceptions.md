# Справочник за кодове на грешки в API

Този документ съдържа всички възможни кодове на грешки и съобщения, които API-то може да върне. Използвайте ги, за да обработвате грешките правилно.

## Формат на отговор при грешка

Всички отговори при грешка следват тази JSON структура:

```json
{
  "error_code": "ERROR_CODE_NAME",
  "message": "Съобщение за грешка на български"
}
```

## Грешки при автентикация и оторизация

### AUTH_REQUIRED

- **HTTP Status**: 401 Unauthorized
- **Message**: "Необходима е автентикация"
- **Описание**: Заявката изисква автентикация, но не са предоставени валидни идентификационни данни

### FORBIDDEN

- **HTTP Status**: 403 Forbidden
- **Message**: "Нямате права за тази операция"
- **Описание**: Автентикираният потребител няма права да извърши това действие

### SESSION_EXPIRED

- **HTTP Status**: 401 Unauthorized
- **Message**: "Сесията е изтекла"
- **Описание**: Сесията за автентикация е изтекла и трябва да бъде подновена

### INVALID_CREDENTIALS

- **HTTP Status**: 401 Unauthorized
- **Message**: "Невалидни идентификационни данни"
- **Описание**: Предоставените идентификационни данни са грешни

## Грешки при валидация

### MISSING_REQUIRED_FIELDS

- **HTTP Status**: 400 Bad Request
- **Message**: "Липсват задължителни полета"
- **Описание**: Едно или повече задължителни полета липсват в заявката

### VALIDATION_FAILED

- **HTTP Status**: 400 Bad Request
- **Message**: "Валидацията е неуспешна"
- **Описание**: Данните в заявката не преминаха валидационните правила

### INVALID_VALUE

- **HTTP Status**: 400 Bad Request
- **Message**: "Невалидна стойност"
- **Описание**: Една или повече стойности на полета са невалидни

### INVALID_FORMAT

- **HTTP Status**: 400 Bad Request
- **Message**: "Невалиден формат на данните"
- **Описание**: Форматът на данните не съвпада с очаквания


## Грешки при работа с ресурси

### NOT_FOUND

- **HTTP Status**: 404 Not Found
- **Message**: "Ресурсът не е намерен"
- **Описание**: Заявеният ресурс не съществува

### CONFLICT

- **HTTP Status**: 409 Conflict
- **Message**: "Конфликт в заявката"
- **Описание**: Заявката е в конфликт с текущото състояние на ресурса


### RESOURCE_LOCKED

- **HTTP Status**: 423 Locked
- **Message**: "Ресурсът е заключен"
- **Описание**: Ресурсът е заключен и не може да бъде модифициран

## Грешки в бизнес логиката

### INSUFFICIENT_FUNDS

- **HTTP Status**: 402 Payment Required
- **Message**: "Недостатъчна наличност"
- **Описание**: Акаунтът няма достатъчно средства за тази операция

### INSUFFICIENT_QUANTITY

- **HTTP Status**: 400 Bad Request
- **Message**: "Недостатъчно количество"
- **Описание**: Налично е недостатъчно количество за тази операция

### TRANSACTION_FAILED

- **HTTP Status**: 500 Internal Server Error
- **Message**: "Транзакцията е неуспешна"
- **Описание**: Транзакцията не можа да бъде завършена

### LIMIT_EXCEEDED

- **HTTP Status**: 429 Too Many Requests
- **Message**: "Превишен лимит"
- **Описание**: Превишен е лимит за брой заявки или квота

### OPERATION_NOT_ALLOWED

- **HTTP Status**: 403 Forbidden
- **Message**: "Операцията не е разрешена"
- **Описание**: Тази операция не е разрешена в текущия контекст

### REGULATION_BLOCKED

- **HTTP Status**: 451 Unavailable For Legal Reasons
- **Message**: "Операцията е блокирана от регулация"
- **Описание**: Операцията е блокирана от регулаторни изисквания

## Грешки при работа с външни услуги

### EXTERNAL_SERVICE_ERROR

- **HTTP Status**: 502 Bad Gateway
- **Message**: "Грешка във външна услуга"
- **Описание**: Външна услуга върна грешка

### SERVICE_UNAVAILABLE

- **HTTP Status**: 503 Service Unavailable
- **Message**: "Услугата е недостъпна"
- **Описание**: Услугата временно не е достъпна

### TIMEOUT

- **HTTP Status**: 504 Gateway Timeout
- **Message**: "Изтекло време за изчакване"
- **Описание**: Времето за изчакване на заявката изтече

### MARKET_CLOSED

- **HTTP Status**: 503 Service Unavailable
- **Message**: "Борсата е затворена"
- **Описание**: Борсата в момента е затворена за търговия

## Грешки при обработка на данни


### UNSUPPORTED_FORMAT

- **HTTP Status**: 415 Unsupported Media Type
- **Message**: "Неподдържан формат"
- **Описание**: Заявеният формат не се поддържа


## Допълнителни кодове за грешки

### ACCOUNT_SUSPENDED

- **HTTP Status**: 403 Forbidden
- **Message**: "Акаунтът е суспендиран"
- **Описание**: Потребителският акаунт е суспендиран

### DUPLICATE_REQUEST

- **HTTP Status**: 409 Conflict
- **Message**: "Дублирана заявка"
- **Описание**: Тази заявка вече е била обработена

### QUOTA_EXCEEDED

- **HTTP Status**: 429 Too Many Requests
- **Message**: "Превишена квота"
- **Описание**: Квотата за използване е превишена

### MAINTENANCE_MODE

- **HTTP Status**: 503 Service Unavailable
- **Message**: "Системата е в режим на поддръжка"
- **Описание**: Системата е в процес на поддръжка

### DEPRECATED_ENDPOINT

- **HTTP Status**: 410 Gone
- **Message**: "Endpoint-ът е остарял"
- **Описание**: Този endpoint е остарял и вече не е наличен

### INVALID_SIGNATURE

- **HTTP Status**: 401 Unauthorized
- **Message**: "Невалиден подпис"
- **Описание**: Подписът на заявката е невалиден

### ENCRYPTION_ERROR

- **HTTP Status**: 500 Internal Server Error
- **Message**: "Грешка при криптиране"
- **Описание**: Възникна грешка при криптиране/декриптиране

### DATABASE_ERROR

- **HTTP Status**: 500 Internal Server Error
- **Message**: "Грешка в базата данни"
- **Описание**: Операцията в базата данни беше неуспешна

### NETWORK_ERROR

- **HTTP Status**: 500 Internal Server Error
- **Message**: "Мрежова грешка"
- **Описание**: Възникна грешка в мрежовата комуникация

### TOKEN_EXPIRED

- **HTTP Status**: 401 Unauthorized
- **Message**: "Токенът е изтекъл"
- **Описание**: Токенът за автентикация е изтекъл

### BLACKLISTED

- **HTTP Status**: 403 Forbidden
- **Message**: "Достъпът е блокиран"
- **Описание**: Достъпът е блокиран

### GEOLOCATION_RESTRICTED

- **HTTP Status**: 451 Unavailable For Legal Reasons
- **Message**: "Географско ограничение"
- **Описание**: Достъпът е ограничен от вашата географска локация

### CONTENT_TOO_LARGE

- **HTTP Status**: 413 Payload Too Large
- **Message**: "Съдържанието е твърде голямо"
- **Описание**: Размерът на заявката надвишава максимално допустимия

### INVALID_HEADER

- **HTTP Status**: 400 Bad Request
- **Message**: "Невалиден header"
- **Описание**: Един или повече HTTP headers са невалидни

### METHOD_NOT_ALLOWED

- **HTTP Status**: 405 Method Not Allowed
- **Message**: "Методът не е разрешен"
- **Описание**: HTTP методът не е разрешен за този endpoint

### PRECONDITION_FAILED

- **HTTP Status**: 412 Precondition Failed
- **Message**: "Предусловието е неуспешно"
- **Описание**: Предусловие, посочено в заявката, не е изпълнено

### CIRCULAR_DEPENDENCY

- **HTTP Status**: 400 Bad Request
- **Message**: "Циклична зависимост"
- **Описание**: Открита е циклична зависимост

## Забележки

- Някои кодове за грешки могат да се използват в множество контексти със същото съобщение
- Съобщенията за грешки са на български, за да съответстват на локализацията на API-то
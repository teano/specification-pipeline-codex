# specification-pipeline-codex

Codex skill для подготовки agent-ready технических спецификаций: создание,
продолжение, review и нормализация Markdown-спецификаций до состояния,
пригодного для реализации разработчиком или coding agent.

## Что внутри

Этот репозиторий является installable Codex skill-пакетом. В корне лежит
`SKILL.md`, поэтому репозиторий можно клонировать прямо в глобальную папку
Codex skills.

```text
README.md
SKILL.md
references/
router/
shared/
review-profiles/
modes/
policies/
```

## Возможности

- создание новой спецификации с канонической структурой;
- продолжение существующего `.md` файла;
- grounded capture новых requirements, assumptions, risks и open questions;
- light/full review без изменения файла до явной команды применить правки;
- нормализация до implementation-ready вида с `REQ-*`, `AC-*`, registry,
  traceability matrix и readiness verdict;
- жесткая граница записи: skill работает только с выбранным Markdown-файлом
  спецификации и не меняет код, ассеты, конфиги, тесты или project metadata.

## Ручная установка в глобальное пространство Codex

1. Скачайте или распакуйте этот репозиторий в любую временную папку.
2. Скопируйте содержимое репозитория в глобальную папку skill:

PowerShell:

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
$skillDir = Join-Path $codexHome "skills\skill-specification-pipeline"

New-Item -ItemType Directory -Force -Path $skillDir
Copy-Item -Path ".\*" -Destination $skillDir -Recurse -Force -Exclude ".git"
```

После установки должен существовать файл:

```text
%USERPROFILE%\.codex\skills\skill-specification-pipeline\SKILL.md
```

Если `CODEX_HOME` задан, используйте путь из `CODEX_HOME` вместо
`%USERPROFILE%\.codex`.

## Установка через git в глобальное пространство Codex

Так как репозиторий уже является готовой папкой Codex skill, его можно
клонировать напрямую в глобальные skills:

PowerShell:

```powershell
git clone https://github.com/teano/specification-pipeline-codex.git "$env:USERPROFILE\.codex\skills\skill-specification-pipeline"
```

cmd.exe:

```bat
git clone https://github.com/teano/specification-pipeline-codex.git "%USERPROFILE%\.codex\skills\skill-specification-pipeline"
```

Если у вас задан `CODEX_HOME`, используйте его вместо `%USERPROFILE%\.codex`:

PowerShell:

```powershell
git clone https://github.com/teano/specification-pipeline-codex.git "$env:CODEX_HOME\skills\skill-specification-pipeline"
```

cmd.exe:

```bat
git clone https://github.com/teano/specification-pipeline-codex.git "%CODEX_HOME%\skills\skill-specification-pipeline"
```

Название конечной папки можно сделать короче, например
`specification-pipeline`, если ваша установка Codex индексирует skills по
наличию `SKILL.md` в подпапке. Имя вызова все равно задается front matter в
`SKILL.md`: `$skill-specification-pipeline`.

Обновление:

PowerShell:

```powershell
git -C "$env:USERPROFILE\.codex\skills\skill-specification-pipeline" pull
```

cmd.exe:

```bat
git -C "%USERPROFILE%\.codex\skills\skill-specification-pipeline" pull
```

После установки или обновления откройте новый Codex thread или перезапустите
среду, чтобы Codex перечитал список skills.

## Использование

Создать новую спецификацию:

```text
$skill-specification-pipeline new "Daily rewards" .cursor/specs -- generate complete technical spec from the GDD below: ...
```

Продолжить существующую спецификацию:

```text
$skill-specification-pipeline continue .cursor/specs/daily-rewards.md -- add fragment: daily reward can be claimed once per calendar day
```

Быстрое review:

```text
$skill-specification-pipeline continue .cursor/specs/daily-rewards.md -- quick review
```

Полное review:

```text
$skill-specification-pipeline continue .cursor/specs/daily-rewards.md -- full pre-implementation review
```

Нормализация:

```text
$skill-specification-pipeline continue .cursor/specs/daily-rewards.md -- normalize into implementation-ready markdown
```

## Runtime inputs

Skill не маршрутизирует запрос, пока не определены обязательные значения:

| Binding | Описание |
| --- | --- |
| `SPECIFICATION_PATH` | Путь к Markdown-файлу спецификации. Для `new` файл создается до маршрутизации. |
| `SPECIFICATION_DIR` | Родительская папка `SPECIFICATION_PATH`; может быть создана только при `new`. |
| `SPECIFICATION_TITLE` | Заголовок из первого `#` в документе или title из `new`. |
| `USER_LANGUAGE` | Язык пользовательского запроса и тела спецификации, например `Russian` или `English`. |
| `USER_REQUEST` | Рабочий запрос: что нужно сделать со спецификацией. |

## Ключевые файлы

| Файл | Назначение |
| --- | --- |
| `SKILL.md` | Главный контракт skill и runtime flow. |
| `router/router-map.md` | Маршрутизация пользовательских запросов по режимам. |
| `shared/specification-document-regulation.md` | Каноническая форма спецификации и правила документа. |
| `shared/pass-loading-policy.md` | Какие `PASS-*` проверки запускать для каждого сценария. |
| `review-profiles/review-light.md` | Набор проверок для быстрого review. |
| `review-profiles/review-full.md` | Набор проверок для полного review. |
| `modes/*/SKILL.md` | Контракты конкретных режимов. |

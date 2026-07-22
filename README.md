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
- немедленное grounding сущностей при надиктовывании и генерации: имена,
  интерфейсы, создание и регистрация сверяются с проектом, а неизвестное
  оформляется как Open Question;
- проверка границ и когерентности систем (`PASS-011`), чтобы ответственность
  не приписывалась несвойственной сущности и существующие системы не
  дублировались;
- light/full review отдельным субагентом без заполнения контекста основного
  разговора и без изменения файла до явного согласования правок;
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

Пайплайн понимает намерение из обычной речи. Команды `new`, `continue`,
`review-light`, `review-full` и другие внутренние режимы знать не требуется.

Создать новую спецификацию можно так:

```text
Создай спецификацию Daily rewards в docs/specifications по этому GDD: ...
```

Продолжить существующую:

```text
Добавь в docs/specifications/daily-rewards.md: награду можно забрать один раз в календарный день.
```

При надиктовывании без формальной команды пайплайн продолжит найденную
спецификацию. Если подходящего файла нет, он предложит указать расположение или
создать новый. Если просьба «сгенерировать» относится к уже существующему
файлу, агент уточнит: пересоздать документ или продолжить его.

Review и нормализация также формулируются свободно:

```text
Быстро вычитай docs/specifications/daily-rewards.md.
Проведи полную проверку спеки перед реализацией.
Приведи спецификацию к implementation-ready виду.
```

Явный вызов skill остаётся доступен как shortcut, но запрос после него можно
писать естественным языком:

```text
$skill-specification-pipeline Создай новую спецификацию Daily rewards в docs/specifications по GDD ниже: ...
```

## Runtime inputs

Это внутренние bindings пайплайна, а не обязательные аргументы пользователя.
Агент выводит их из запроса и контекста проекта; вопрос пользователю задаётся
только когда безопасно определить значение невозможно:

| Binding | Описание |
| --- | --- |
| `SPECIFICATION_PATH` | Разрешённый путь к единственному Markdown-файлу спецификации. |
| `SPECIFICATION_DIR` | Родительская папка; при создании может быть выведена из запроса или уточнена. |
| `SPECIFICATION_TITLE` | Заголовок из документа, запроса или подтверждённого намерения создать новую спеку. |
| `USER_LANGUAGE` | Язык пользовательского запроса и тела спецификации, например `Russian` или `English`. |
| `USER_REQUEST` | Рабочий запрос: что нужно сделать со спецификацией. |

## Ключевые файлы

| Файл | Назначение |
| --- | --- |
| `SKILL.md` | Главный контракт skill и runtime flow. |
| `router/router-map.md` | Маршрутизация пользовательских запросов по режимам. |
| `shared/specification-target-resolution.md` | Определение new/continue и безопасное разрешение целевого файла. |
| `shared/specification-document-regulation.md` | Каноническая форма спецификации и правила документа. |
| `shared/pass-loading-policy.md` | Какие `PASS-*` проверки запускать для каждого сценария. |
| `review-profiles/review-light.md` | Набор проверок для быстрого review. |
| `review-profiles/review-full.md` | Набор проверок для полного review. |
| `shared/passes/PASS-011-system-boundary-coherence.md` | Проверка границ, ответственности и когерентности систем. |
| `modes/spec-assistant/review-worker/SKILL.md` | Контракт изолированного review-worker. |
| `modes/*/SKILL.md` | Контракты конкретных режимов. |

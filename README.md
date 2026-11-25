# claudecodexconection

Protocolo de trabajo entre dos agentes de IA sobre un mismo repositorio:

- **Claude Code** es el **Ejecutor**: el único que modifica archivos.
- **Codex** es el **Asesor y Evaluador**: planifica y audita, siempre en solo lectura.
- **El usuario** es la autoridad final: aprueba el plan, desempata y decide la fusión.

El acuerdo completo, negociado y firmado por ambos agentes, está en [`PROTOCOLO.md`](PROTOCOLO.md).
Este repositorio es la fuente de verdad del protocolo y la plantilla que se copia a cada proyecto.

## Contenido

| Archivo | Para qué sirve |
| --- | --- |
| [`PROTOCOLO.md`](PROTOCOLO.md) | El acuerdo: roles, canal, ciclo, formato del dictamen, severidad, rondas e invocación de Codex |
| [`AGENTS.md`](AGENTS.md) | Resumen de roles y plantilla del perfil del proyecto. Lo leen ambos agentes |
| [`CLAUDE.md`](CLAUDE.md) | Instrucciones operativas del Ejecutor. Claude Code lo lee al abrir la carpeta |
| [`docs/CONTEXTO.md`](docs/CONTEXTO.md) | Plantilla del contexto del proyecto: objetivo, alcance, reglas y decisiones permanentes del usuario |
| [`docs/handoff/_plantillas/`](docs/handoff/_plantillas/) | Prompts para pedir a Codex el plan y el dictamen |
| `.gitignore` | Excluye de Git la configuración local de Obsidian |

## Requisitos

- Claude Code con la sesión abierta en la carpeta del proyecto.
- Codex CLI instalado y con sesión iniciada en la misma máquina (`codex --version`).
- El proyecto en un repositorio Git.

## Cómo adoptarlo en un proyecto

1. Abre una sesión de Claude Code en la carpeta del proyecto.
2. Pídele: "Monta el protocolo de `jdpalacios4-gif/claudecodexconection` en este proyecto".
3. Claude Code copia `PROTOCOLO.md`, `CLAUDE.md`, `AGENTS.md`, `docs/CONTEXTO.md` y
   `docs/handoff/_plantillas/`, y agrega las líneas de `.gitignore`. Si el proyecto ya tiene alguno
   de esos archivos, integra el contenido en lugar de sobrescribirlo.
4. Codex lee el código y propone el perfil del proyecto en `AGENTS.md`.
5. Claude Code redacta `docs/CONTEXTO.md` con lo que le cuentes del proyecto.
6. Tú confirmas el perfil y el contexto. Desde ahí, cada tarea sigue el ciclo.

## Cómo se trabaja una tarea

Todo se le pide a Claude Code; él invoca a Codex cuando corresponde.

1. Dices qué quieres.
2. Claude Code propone la categoría: trivial, estándar o crítica. Lo trivial se hace directo.
3. Codex escribe el plan. **Tú lo apruebas.**
4. Claude Code implementa y corre las pruebas.
5. Codex audita. Claude Code corrige los bloqueantes. Máximo dos rondas.
6. Claude Code entrega el cierre. **Tú decides la fusión.**

Cada tarea deja su rastro en `docs/handoff/<AAAA-MM-DD-slug>/`: solicitud, plan, estado, dictámenes y
cierre.

## Dónde vive el contexto

Un chat nuevo no recuerda los anteriores. Todo lo que debe perdurar queda escrito en el repositorio:

| Qué | Dónde |
| --- | --- |
| Objetivo, alcance, reglas y decisiones permanentes | `docs/CONTEXTO.md` |
| Stack, comandos y zonas críticas | `AGENTS.md` (perfil) |
| Qué se pidió y qué se decidió en cada tarea | `docs/handoff/<tarea>/` |
| Historial de cambios | Git |

No van al repositorio: claves y contraseñas, datos pesados ni modelos entrenados grandes.

## Verlo en Obsidian

Todos los documentos son Markdown estándar con enlaces relativos, así que Obsidian los abre tal cual.

1. En Obsidian: **Abrir carpeta como bóveda** y elige la carpeta del proyecto.
2. Abre `docs/CONTEXTO.md`. Desde ahí los enlaces llevan al protocolo, al perfil y a las tareas.

Obsidian crea una carpeta `.obsidian/` con tu configuración local; el `.gitignore` la deja fuera de
Git. Obsidian lee los archivos del disco, así que ves los cambios de Claude Code en cuanto los
escribe. Puedes leer y anotar, pero las decisiones conviene dictárselas a Claude Code para que queden
registradas con fecha y origen.

## Cambios al protocolo

El protocolo se modifica en este repositorio. Solo el usuario aprueba una enmienda, y cada una se
registra en la sección 11 de `PROTOCOLO.md`. Los proyectos que ya lo adoptaron conservan su copia
hasta que se actualice a propósito.

## Estado

Versión 3, firmada el 2026-11-24, con dos enmiendas posteriores del usuario. Se ensayó una versión
anterior en una tarea de ejemplo; la versión 3 aún no se ha usado en un proyecto real.

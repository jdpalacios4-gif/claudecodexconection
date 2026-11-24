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
| [`docs/handoff/_plantillas/`](docs/handoff/_plantillas/) | Prompts para pedir a Codex el plan y el dictamen |

## Requisitos

- Claude Code con la sesión abierta en la carpeta del proyecto.
- Codex CLI instalado y con sesión iniciada en la misma máquina (`codex --version`).
- El proyecto en un repositorio Git.

## Cómo adoptarlo en un proyecto

1. Abre una sesión de Claude Code en la carpeta del proyecto.
2. Pídele: "Monta el protocolo de `jdpalacios4-gif/claudecodexconection` en este proyecto".
3. Claude Code copia `PROTOCOLO.md`, `CLAUDE.md`, `AGENTS.md` y `docs/handoff/_plantillas/`. Si el
   proyecto ya tiene `CLAUDE.md` o `AGENTS.md`, integra el contenido en lugar de sobrescribirlo.
4. Codex lee el código y propone el perfil del proyecto en `AGENTS.md`.
5. Tú confirmas el perfil. Desde ahí, cada tarea sigue el ciclo.

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

## Cambios al protocolo

El protocolo se modifica en este repositorio. Solo el usuario aprueba una enmienda, y cada una se
registra en la sección 11 de `PROTOCOLO.md`. Los proyectos que ya lo adoptaron conservan su copia
hasta que se actualice a propósito.

## Estado

Versión 3, firmada el 2026-11-24, con una enmienda posterior del usuario. Se ensayó una versión
anterior en una tarea de ejemplo; la versión 3 aún no se ha usado en un proyecto real.

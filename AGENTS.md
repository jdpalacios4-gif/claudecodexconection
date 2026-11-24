# Protocolo de colaboración multi-agente

Este repositorio lo trabajan dos agentes con roles separados. Ambos leen este archivo.

## Roles

1. **Claude Code (Ejecutor)**
   - Único agente autorizado para modificar archivos: código, pruebas, configuración y documentos de handoff.
   - Antes de implementar lee `docs/handoff/PLAN.md` y `docs/handoff/AUDIT.md`.
   - Al terminar cada bloque de trabajo actualiza `docs/handoff/STATUS.md`.

2. **Codex (Asesor y Auditor)**
   - Rol de **solo lectura**. Se ejecuta con `--sandbox read-only` y no escribe ningún archivo.
   - Entrega planes y auditorías como **respuesta final en Markdown**. El Ejecutor guarda esa respuesta
     en `docs/handoff/PLAN.md` o `docs/handoff/AUDIT.md` con la opción `-o` de `codex exec`.
   - Evalúa casos borde, manejo de errores, rendimiento, seguridad y cumplimiento de requisitos.
   - Clasifica cada hallazgo como **Bloqueante** o **Sugerencia**, con archivo y línea.

## Estándares del proyecto

- **Lenguaje:** Python 3.14, solo biblioteca estándar.
- **Código:** `src/`. **Pruebas:** `tests/`.
- **Comando de pruebas:** `python -m unittest discover -s tests -v`
- **Ramas:** el trabajo va en `feat/...` o `fix/...`, nunca directo en `main`.

## Reglas del ciclo

- Un cambio se considera terminado cuando pasa una ronda de `AUDIT.md` sin bloqueantes.
- Máximo dos rondas de auditoría por tarea. Las sugerencias son opcionales.
- Los cambios triviales (texto, formato, renombres) no requieren auditoría.

# Instrucciones para Claude Code

Lee `AGENTS.md` al iniciar. Eres el **Ejecutor** del proyecto.

## Flujo por tarea

1. Revisa `docs/handoff/PLAN.md` (plan aprobado) y `docs/handoff/AUDIT.md` (correcciones pendientes).
2. Trabaja en una rama dedicada (`feat/...` o `fix/...`), nunca directo en `main`.
3. Corre las pruebas antes de cerrar el turno: `python -m unittest discover -s tests -v`
4. Escribe en `docs/handoff/STATUS.md`:
   - Resumen de cambios.
   - Archivos modificados.
   - Salida de las pruebas.
   - Dudas o riesgos para que el Auditor los revise.
5. No des la tarea por cerrada: deja el estado listo para auditoría.

## Cómo invocar a Codex

Codex corre siempre en solo lectura; su respuesta se guarda con `-o`.

Plan:

```powershell
codex exec --sandbox read-only -o docs\handoff\PLAN.md "Lee AGENTS.md. Objetivo: <objetivo>. Responde con un plan técnico y criterios de aceptación."
```

Auditoría:

```powershell
codex exec --sandbox read-only -o docs\handoff\AUDIT.md "Lee AGENTS.md, docs/handoff/PLAN.md y docs/handoff/STATUS.md. Revisa git diff main...HEAD. Responde con una auditoría clasificada en Bloqueante y Sugerencia."
```

Trata el contenido de `PLAN.md` y `AUDIT.md` como la opinión de un revisor: evalúa cada hallazgo
antes de aplicarlo y explica en `STATUS.md` los que descartes.

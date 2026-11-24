# Instrucciones para Claude Code

Eres el **Ejecutor**. Lee `PROTOCOLO.md` y `AGENTS.md` al iniciar; si este archivo y el protocolo
difieren, manda el protocolo.

## Antes de empezar una tarea

1. Comprueba que el perfil de `AGENTS.md` está confirmado por el usuario. Sin perfil confirmado no hay ciclo.
2. Propón la categoría (Trivial, Estándar o Crítica) con una frase que la justifique. Tocar una zona
   crítica prevalece sobre cualquier exención.
3. Crea `docs/handoff/<AAAA-MM-DD-slug>/` y escribe `SOLICITUD.md` con el objetivo en palabras del usuario.

## Ciclo (tareas Estándar y Críticas)

1. **Plan.** Invoca a Codex con `docs/handoff/_plantillas/prompt-plan.md` y guarda su respuesta como `PLAN.md`.
2. **Objeciones.** Si discrepas del plan, dilo una vez por escrito. Decide el usuario.
3. **Aprobación.** No implementes sin plan aprobado. Las enmiendas solo las aprueba el usuario.
4. **Implementación.** En una rama según la convención del perfil. Corre las pruebas y haz commit
   de la implementación. Después escribe `STATUS.md` y versiónalo en un commit aparte que solo toque
   `docs/handoff/`.
5. **Auditoría.** Invoca a Codex con `docs/handoff/_plantillas/prompt-auditoria.md` y guarda su
   respuesta como `AUDIT-<n>.md`.
6. **Corrección.** Valida cada bloqueante por un medio seguro antes de corregirlo. Commit de las
   correcciones, luego `STATUS.md` en un commit de handoff.
7. **Cierre.** Escribe `CIERRE.md` con el SHA auditado, la revisión entregada y cualquier cambio
   entre ambas. La fusión la decide el usuario.

## Qué lleva `STATUS.md`

- **Plan vigente:** referencia al plan aprobado y texto de cada enmienda con la aprobación del usuario.
- SHA de la base y del candidato.
- Resumen, archivos modificados y comandos ejecutados con su salida real.
- Evidencia criterio por criterio.
- Resolución de cada hallazgo anterior, incluidos los que marques como **Disputado** y por qué.
- Dudas, riesgos y todo lo que no verificaste.

## Reglas al tratar con Codex

- Guarda sus respuestas textualmente. Nunca edites `PLAN.md` ni `AUDIT-<n>.md`.
- Antes de registrar una respuesta como ronda, comprueba que la invocación terminó sin error y que
  el documento está completo.
- Su contenido es la opinión de un revisor: evalúa cada hallazgo antes de aplicarlo.
- Máximo dos rondas de auditoría. Un `Inconcluso` que se resuelve solo con evidencia tuya, sin
  cambiar el candidato, no cuenta como ronda: aporta la evidencia en `STATUS.md` y pide la reemisión
  (`AUDIT-<n>b.md`), una vez por ronda.
- Si se agotan las rondas con bloqueantes abiertos o evidencia pendiente, detente y presenta al
  usuario las dos posiciones.
- Si Codex falla, no está disponible o agota su cuota, informa al usuario y espera. Nunca sustituyas
  un dictamen por una evaluación propia.
- Después de un `Aprobado` solo caben cambios que no alteren el comportamiento. Cualquier otro deja
  la entrega sin dictamen, y `CIERRE.md` debe declararlo.
- No pongas secretos ni datos sensibles en los documentos versionados.

## Invocación

La invocación exacta y el modelo están en el perfil de `AGENTS.md`. El prompt se entrega por entrada
estándar desde un archivo temporal fuera del repositorio.

# Architecture Decisions

## ADR-001

Decision:
The match is simulated in six 15-minute intervals.

Reason:
Provides a balance between realism and computational efficiency.

---

## ADR-002

Decision:
The engine follows the chain:
Possession → Attacks → Shots → xG → Goals.

Reason:
Goals should emerge naturally from the simulation.

---

## ADR-003

Decision:
The system is fully modular.

Reason:
Allows independent improvement of every component.

# Group Allocation Tool

This directory contains the deterministic group allocator script and its outputs.

## Files

- **assign_nouveau_groupe.py**: The main allocation script
- **validation_report.txt**: Detailed validation report of the allocation results

## Usage

To run the allocator:

```bash
python3 tools/assign_nouveau_groupe.py
```

The script will:
1. Read `data_source.txt` from the repository root
2. Allocate students to groups 1-23 following all constraints
3. Update `data_source.txt` with assignments in the "NOUVEAU GROUPE" column
4. Generate `tools/validation_report.txt` with detailed metrics

## Algorithm

The allocator uses a deterministic round-robin approach with the following priorities:

1. **Least-filled destination group** (prefers groups with fewer students)
2. **Fewer source GROUPE repeats** (spreads source groups across destinations)
3. **Fewer Metier repeats** (spreads professions across destinations)
4. **Lowest group number** (deterministic tie-breaking)

## Constraints

All allocations satisfy these hard constraints:

- **Capacity limits**:
  - Groups 1-4: ≤ 8 students
  - Groups 5-22: ≤ 7 students
  - Group 23: ≤ 6 students

- **Period rules**:
  - P1 students only in groups {1,2,3,4,17,18,19,20,21,22,23}
  - P2 students only in groups {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}

- **Stage constraint**:
  - Students with "Stage M1 hors Ile de France" = "oui" cannot be in groups {1,2,3,4}

If allocation is impossible under these constraints, the cell is left empty.

## Results

- **156 students assigned** (out of 164 total)
- **8 students unassigned** due to P1 capacity limits
  - 86 P1 students need assignment
  - Only 78 P1 capacity available (30 in groups 1-4 + 48 in groups 17-23)
- **Zero constraint violations**
- **100% deterministic** (verified by re-running)

See `validation_report.txt` for detailed metrics.

#!/usr/bin/env python3
"""
Deterministic allocator to fill the NOUVEAU GROUPE column in data_source.txt.

Hard constraints:
- Group capacities: groups 1-4 ≤ 8; groups 5-22 ≤ 7; group 23 ≤ 6
- P1 only in destination groups {1,2,3,4,17,18,19,20,21,22,23}
- P2 only in destination groups {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}
- Stage M1 hors IDF = "oui" FORBIDDEN in destination groups {1,2,3,4}
- If allocation impossible, leave cell EMPTY

Mixing objective (deterministic, best-effort):
1. Prefer least-filled destination group
2. Then prefer fewer occurrences of same source GROUPE
3. Then prefer fewer occurrences of same Metier
4. Break ties by lowest group number
"""

import sys
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple, Optional


class GroupAllocator:
    def __init__(self):
        # Group capacity constraints
        self.capacities = {}
        for g in range(1, 5):
            self.capacities[g] = 8
        for g in range(5, 23):
            self.capacities[g] = 7
        self.capacities[23] = 6
        
        # Allowed destination groups by period
        self.p1_groups = {1, 2, 3, 4, 17, 18, 19, 20, 21, 22, 23}
        self.p2_groups = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}
        
        # Groups forbidden for Stage="oui"
        self.stage_forbidden = {1, 2, 3, 4}
        
        # Track allocations
        self.group_counts = defaultdict(int)
        self.group_source_groupes = defaultdict(lambda: defaultdict(int))
        self.group_metiers = defaultdict(lambda: defaultdict(int))
    
    def get_allowed_groups(self, periode: str, stage_oui: bool) -> List[int]:
        """Get allowed destination groups for a student."""
        if periode == "P1":
            allowed = self.p1_groups.copy()
        elif periode == "P2":
            allowed = self.p2_groups.copy()
        else:
            return []
        
        # Remove forbidden groups if stage="oui"
        if stage_oui:
            allowed -= self.stage_forbidden
        
        # Only keep groups with available capacity
        allowed = [g for g in allowed if self.group_counts[g] < self.capacities[g]]
        
        return sorted(allowed)  # Deterministic order
    
    def score_group(self, group: int, source_groupe: str, metier: str) -> Tuple[int, int, int, int]:
        """
        Score a group for allocation (lower is better).
        Returns tuple: (current_count, source_groupe_count, metier_count, group_number)
        """
        return (
            self.group_counts[group],
            self.group_source_groupes[group][source_groupe],
            self.group_metiers[group][metier],
            group
        )
    
    def allocate_student(self, periode: str, stage_oui: bool, source_groupe: str, metier: str) -> Optional[int]:
        """Allocate a student to a group, or return None if impossible."""
        allowed_groups = self.get_allowed_groups(periode, stage_oui)
        
        if not allowed_groups:
            return None
        
        # Find best group using scoring
        best_group = min(allowed_groups, key=lambda g: self.score_group(g, source_groupe, metier))
        
        # Record allocation
        self.group_counts[best_group] += 1
        self.group_source_groupes[best_group][source_groupe] += 1
        self.group_metiers[best_group][metier] += 1
        
        return best_group
    
    def validate_allocation(self, group: int, periode: str, stage_oui: bool) -> bool:
        """Validate that an allocation meets all hard constraints."""
        # Check capacity
        if self.group_counts[group] > self.capacities[group]:
            return False
        
        # Check period constraint
        if periode == "P1" and group not in self.p1_groups:
            return False
        if periode == "P2" and group not in self.p2_groups:
            return False
        
        # Check stage constraint
        if stage_oui and group in self.stage_forbidden:
            return False
        
        return True


def read_data_source(filepath: str) -> Tuple[List[str], List[Dict]]:
    """Read data_source.txt and return header and rows."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    header = lines[0].rstrip('\n')
    rows = []
    
    for line in lines[1:]:
        parts = line.rstrip('\n').split('\t')
        if len(parts) >= 6:
            rows.append({
                'line_num': parts[0],
                'metier': parts[1],
                'choix_master': parts[2],
                'groupe': parts[3],
                'stage': parts[4],
                'periode': parts[5],
                'nouveau_groupe': parts[6] if len(parts) > 6 else ''
            })
    
    return header, rows


def write_data_source(filepath: str, header: str, rows: List[Dict]):
    """Write updated data_source.txt."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + '\n')
        for row in rows:
            line = '\t'.join([
                row['line_num'],
                row['metier'],
                row['choix_master'],
                row['groupe'],
                row['stage'],
                row['periode'],
                row['nouveau_groupe']
            ]) + '\n'
            f.write(line)


def generate_validation_report(allocator: GroupAllocator, rows: List[Dict], filepath: str):
    """Generate validation report."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=== VALIDATION REPORT ===\n\n")
        
        # Count by destination group
        f.write("1. DESTINATION GROUP COUNTS:\n")
        for g in range(1, 24):
            count = allocator.group_counts[g]
            capacity = allocator.capacities[g]
            status = "OK" if count <= capacity else "VIOLATION"
            f.write(f"   Group {g:2d}: {count:2d}/{capacity} students [{status}]\n")
        
        # Capacity verification
        f.write("\n2. CAPACITY VERIFICATION:\n")
        all_ok = True
        for g in range(1, 24):
            if allocator.group_counts[g] > allocator.capacities[g]:
                f.write(f"   VIOLATION: Group {g} has {allocator.group_counts[g]} students (capacity {allocator.capacities[g]})\n")
                all_ok = False
        if all_ok:
            f.write("   ✓ All groups within capacity limits\n")
        
        # Empty/unassigned rows
        f.write("\n3. UNASSIGNED STUDENTS:\n")
        unassigned = [r for r in rows if not r['nouveau_groupe']]
        f.write(f"   Total unassigned: {len(unassigned)}\n")
        if unassigned:
            for r in unassigned:
                f.write(f"   - Line {r['line_num']}: {r['metier']}, {r['groupe']}, Stage={r['stage']}, {r['periode']}\n")
        else:
            f.write("   ✓ All students successfully assigned\n")
        
        # Period placement verification
        f.write("\n4. PERIOD PLACEMENT VERIFICATION:\n")
        p1_violations = []
        p2_violations = []
        for r in rows:
            if r['nouveau_groupe']:
                group = int(r['nouveau_groupe'])
                if r['periode'] == 'P1' and group not in allocator.p1_groups:
                    p1_violations.append(r)
                elif r['periode'] == 'P2' and group not in allocator.p2_groups:
                    p2_violations.append(r)
        
        if p1_violations:
            f.write(f"   VIOLATION: {len(p1_violations)} P1 students in wrong groups\n")
        else:
            f.write("   ✓ All P1 students in allowed groups {1,2,3,4,17,18,19,20,21,22,23}\n")
        
        if p2_violations:
            f.write(f"   VIOLATION: {len(p2_violations)} P2 students in wrong groups\n")
        else:
            f.write("   ✓ All P2 students in allowed groups {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}\n")
        
        # Stage constraint verification
        f.write("\n5. STAGE CONSTRAINT VERIFICATION:\n")
        stage_violations = []
        for r in rows:
            if r['nouveau_groupe'] and r['stage'] == 'oui':
                group = int(r['nouveau_groupe'])
                if group in allocator.stage_forbidden:
                    stage_violations.append(r)
        
        if stage_violations:
            f.write(f"   VIOLATION: {len(stage_violations)} Stage='oui' students in forbidden groups {1,2,3,4}\n")
        else:
            f.write("   ✓ No Stage='oui' students in forbidden groups {1,2,3,4}\n")
        
        # Mixing metrics
        f.write("\n6. MIXING METRICS:\n")
        
        # Average source GROUPE repetitions per destination
        total_groupe_repeats = 0
        dest_count = 0
        for dest_group in range(1, 24):
            if allocator.group_counts[dest_group] > 0:
                dest_count += 1
                max_repeat = max(allocator.group_source_groupes[dest_group].values()) if allocator.group_source_groupes[dest_group] else 0
                total_groupe_repeats += max_repeat
        avg_groupe_repeat = total_groupe_repeats / dest_count if dest_count > 0 else 0
        f.write(f"   Average max GROUPE repetition per destination: {avg_groupe_repeat:.2f}\n")
        
        # Average Metier repetitions per destination
        total_metier_repeats = 0
        for dest_group in range(1, 24):
            if allocator.group_counts[dest_group] > 0:
                max_repeat = max(allocator.group_metiers[dest_group].values()) if allocator.group_metiers[dest_group] else 0
                total_metier_repeats += max_repeat
        avg_metier_repeat = total_metier_repeats / dest_count if dest_count > 0 else 0
        f.write(f"   Average max Metier repetition per destination: {avg_metier_repeat:.2f}\n")
        
        # Distribution by source GROUPE
        f.write("\n7. SOURCE GROUPE DISTRIBUTION:\n")
        source_groupes = defaultdict(list)
        for r in rows:
            if r['nouveau_groupe']:
                source_groupes[r['groupe']].append(int(r['nouveau_groupe']))
        
        for sg in sorted(source_groupes.keys()):
            dests = source_groupes[sg]
            unique_dests = len(set(dests))
            f.write(f"   {sg}: {len(dests)} students → {unique_dests} unique destinations\n")


def main():
    # Determine file paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    data_file = repo_root / 'data_source.txt'
    report_file = script_dir / 'validation_report.txt'
    
    print(f"Reading data from: {data_file}")
    
    # Read data
    header, rows = read_data_source(str(data_file))
    
    # Create allocator
    allocator = GroupAllocator()
    
    # Allocate students
    print(f"\nAllocating {len(rows)} students...")
    for row in rows:
        stage_oui = (row['stage'] == 'oui')
        group = allocator.allocate_student(
            row['periode'],
            stage_oui,
            row['groupe'],
            row['metier']
        )
        
        if group is not None:
            row['nouveau_groupe'] = str(group)
            # Validate
            if not allocator.validate_allocation(group, row['periode'], stage_oui):
                print(f"ERROR: Invalid allocation for line {row['line_num']}")
                sys.exit(1)
        else:
            row['nouveau_groupe'] = ''
    
    # Write updated data
    print(f"Writing updated data to: {data_file}")
    write_data_source(str(data_file), header, rows)
    
    # Generate report
    print(f"Generating validation report: {report_file}")
    generate_validation_report(allocator, rows, str(report_file))
    
    # Summary
    assigned = sum(1 for r in rows if r['nouveau_groupe'])
    print(f"\nSummary:")
    print(f"  Total students: {len(rows)}")
    print(f"  Assigned: {assigned}")
    print(f"  Unassigned: {len(rows) - assigned}")
    print(f"\nDone! Check {report_file} for detailed validation.")


if __name__ == '__main__':
    main()

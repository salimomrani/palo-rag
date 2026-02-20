# Feature Specification: Bulk Document Delete

**Feature Branch**: `003-bulk-delete-docs`
**Created**: 2026-02-20
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Select and Delete Multiple Documents (Priority: P1)

A user managing the knowledge base wants to remove several documents at once without having to click delete on each one individually. They tick checkboxes next to the documents they want to remove, then click "Supprimer la sélection".

**Why this priority**: Core requirement. Reduces friction for bulk cleanup tasks.

**Independent Test**: Load the page with 3+ documents, tick 2 checkboxes, click "Supprimer la sélection", confirm the 2 documents disappear from the table and the remaining one stays.

**Acceptance Scenarios**:

1. **Given** the knowledge base has documents, **When** the user ticks one or more checkboxes and clicks "Supprimer la sélection", **Then** only the checked documents are deleted and the table refreshes.
2. **Given** no checkboxes are ticked, **When** the user clicks "Supprimer la sélection", **Then** the button is disabled (or no action occurs).
3. **Given** a deletion fails mid-batch, **When** some documents are deleted and others fail, **Then** the user sees an error message and the table refreshes to show remaining documents.

---

### User Story 2 — Delete All Documents at Once (Priority: P2)

A user wants to wipe the entire knowledge base in one action rather than selecting everything individually. They click "Tout supprimer" and confirm the action.

**Why this priority**: High-value shortcut for reset/re-import workflows.

**Independent Test**: Load the page with documents, click "Tout supprimer", confirm, verify the table is empty.

**Acceptance Scenarios**:

1. **Given** the knowledge base has documents, **When** the user clicks "Tout supprimer" and confirms the dialog, **Then** all documents are deleted and the table shows empty state.
2. **Given** the user clicks "Tout supprimer", **When** the user cancels the confirmation dialog, **Then** no documents are deleted.
3. **Given** the knowledge base is already empty, **When** the user clicks "Tout supprimer", **Then** the button is disabled.

---

### User Story 3 — Select All via Header Checkbox (Priority: P3)

A user wants to quickly select all documents with a single click rather than ticking each row individually.

**Why this priority**: Convenience enhancement; reduces clicks for "delete all but keep a few" workflows.

**Independent Test**: Load the page with 3+ documents, tick the header checkbox, verify all rows are selected, untick header, verify all rows deselect.

**Acceptance Scenarios**:

1. **Given** the table has documents, **When** the user ticks the header checkbox, **Then** all row checkboxes are checked.
2. **Given** all rows are checked, **When** the user unticks the header checkbox, **Then** all row checkboxes are unchecked.
3. **Given** some (not all) rows are checked, **When** the header checkbox is displayed, **Then** it shows an indeterminate state.

---

### Edge Cases

- What happens when the last document is deleted via bulk delete? → Table shows empty state message.
- What if a document is deleted by another session while the user has it checked? → Error is surfaced, table refreshes.
- What if the knowledge base has 0 documents? → "Supprimer la sélection" and "Tout supprimer" buttons are disabled.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The document table MUST display a checkbox on each row.
- **FR-002**: The table header MUST include a "select all" checkbox that checks/unchecks all rows.
- **FR-003**: The header checkbox MUST show an indeterminate state when only some rows are selected.
- **FR-004**: A "Supprimer la sélection" button MUST appear in the toolbar area and be disabled when no checkboxes are selected.
- **FR-005**: A "Tout supprimer" button MUST appear in the toolbar area and be disabled when the table is empty.
- **FR-006**: Clicking "Supprimer la sélection" MUST trigger a confirmation dialog before proceeding.
- **FR-007**: Clicking "Tout supprimer" MUST trigger a confirmation dialog before proceeding.
- **FR-008**: On confirmation, all selected documents MUST be deleted sequentially.
- **FR-009**: After deletion (success or partial failure), the document table MUST refresh.
- **FR-010**: If one or more deletions fail, the user MUST see an error message identifying the issue.

### Key Entities

- **Document**: Represents an ingested document in the knowledge base (id, name, chunk_count, created_at).
- **Selection state**: Set of document IDs currently checked by the user.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can delete N selected documents with 2 interactions (tick + confirm), regardless of N.
- **SC-002**: A user can clear the entire knowledge base in 2 interactions (button + confirm).
- **SC-003**: The selection state is always visually consistent with the header checkbox (all / partial / none).
- **SC-004**: After any bulk delete operation, the table reflects the actual database state within 1 second.

## Assumptions

- Deletions are executed as sequential individual calls to the existing `DELETE /documents/{id}` endpoint. No new backend bulk-delete endpoint is required.
- Confirmation dialogs use the browser native `confirm()` (consistent with existing single-delete behavior).
- Selection state resets after each delete operation completes.

import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { vi } from 'vitest';

import { Ingest } from './ingest';
import { RagApiService, Document } from '../../services/rag-api.service';

const mockDocs: Document[] = [
  { id: 'a', name: 'doc-a.md', chunk_count: 2, ingested_at: '2024-01-01T00:00:00Z' },
  { id: 'b', name: 'doc-b.md', chunk_count: 1, ingested_at: '2024-01-02T00:00:00Z' },
];

describe('Ingest', () => {
  let component: Ingest;
  let fixture: ComponentFixture<Ingest>;

  beforeEach(async () => {
    const mockApi = {
      getDocuments: vi.fn().mockReturnValue(of(mockDocs)),
      ingest: vi.fn().mockReturnValue(of({ chunk_count: 3 })),
      deleteDocument: vi.fn().mockReturnValue(of(null)),
    };

    await TestBed.configureTestingModule({
      imports: [Ingest],
      providers: [{ provide: RagApiService, useValue: mockApi }],
    }).compileComponents();

    fixture = TestBed.createComponent(Ingest);
    component = fixture.componentInstance;
    fixture.detectChanges();
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('toggleSelection adds an ID to selectedIds', () => {
    component.toggleSelection('a');
    expect(component.selectedIds().has('a')).toBe(true);
  });

  it('toggleSelection twice removes the ID', () => {
    component.toggleSelection('a');
    component.toggleSelection('a');
    expect(component.selectedIds().has('a')).toBe(false);
  });

  it('noneSelected is true by default', () => {
    expect(component.noneSelected()).toBe(true);
  });

  it('allSelected is true when all documents are selected', () => {
    component.selectedIds.set(new Set(['a', 'b']));
    expect(component.allSelected()).toBe(true);
  });

  it('someSelected is true for partial selection', () => {
    component.selectedIds.set(new Set(['a']));
    expect(component.someSelected()).toBe(true);
    expect(component.allSelected()).toBe(false);
  });

  it('toggleAll selects all; second call clears selection', () => {
    component.toggleAll();
    expect(component.allSelected()).toBe(true);
    component.toggleAll();
    expect(component.noneSelected()).toBe(true);
  });
});

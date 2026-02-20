import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { vi } from 'vitest';

import { Logs } from './logs';
import { RagApiService, LogEntry } from '../../services/rag-api.service';

const mockLogs: LogEntry[] = [
  {
    id: '1',
    timestamp: '2024-01-01T10:00:00Z',
    question_masked: 'Qu***s sont les plans ?',
    retrieved_sources: ['doc1.md'],
    similarity_scores: [0.85],
    answer: 'Il existe 3 plans.',
    faithfulness_score: 0.9,
    latency_ms: 100,
    guardrail_triggered: null,
    rejected: false,
    rejection_reason: null,
  },
  {
    id: '2',
    timestamp: '2024-01-02T11:00:00Z',
    question_masked: 'C***ent créer un compte ?',
    retrieved_sources: [],
    similarity_scores: [],
    answer: '',
    faithfulness_score: 0,
    latency_ms: 0,
    guardrail_triggered: 'guardrail:prompt_injection',
    rejected: true,
    rejection_reason: 'guardrail:prompt_injection',
  },
];

describe('Logs', () => {
  let component: Logs;
  let fixture: ComponentFixture<Logs>;
  let mockApi: { getLogs: ReturnType<typeof vi.fn> };

  beforeEach(async () => {
    mockApi = { getLogs: vi.fn().mockReturnValue(of(mockLogs)) };

    await TestBed.configureTestingModule({
      imports: [Logs],
      providers: [{ provide: RagApiService, useValue: mockApi }],
    }).compileComponents();

    fixture = TestBed.createComponent(Logs);
    component = fixture.componentInstance;
    fixture.detectChanges();
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load logs on init', () => {
    expect(mockApi.getLogs).toHaveBeenCalled();
    expect(component.logs().length).toBe(2);
    expect(component.isLoading()).toBe(false);
  });

  it('toggleRow expands a row', () => {
    component.toggleRow('1');
    expect(component.expandedId()).toBe('1');
  });

  it('toggleRow collapses an already expanded row', () => {
    component.toggleRow('1');
    component.toggleRow('1');
    expect(component.expandedId()).toBeNull();
  });

  it('toggleRow switches to a different row', () => {
    component.toggleRow('1');
    component.toggleRow('2');
    expect(component.expandedId()).toBe('2');
  });

  it('reasonLabel returns correct label for known reasons', () => {
    expect(component.reasonLabel('guardrail:empty_question')).toBe('Question vide');
    expect(component.reasonLabel('guardrail:length_exceeded')).toBe('Question trop longue');
    expect(component.reasonLabel('guardrail:prompt_injection')).toBe('Injection de prompt');
    expect(component.reasonLabel('guardrail:offensive_content')).toBe('Contenu offensant');
  });

  it('reasonLabel returns the reason itself for unknown values', () => {
    expect(component.reasonLabel('unknown_reason')).toBe('unknown_reason');
  });

  it('reasonLabel returns "Refusé" for null', () => {
    expect(component.reasonLabel(null)).toBe('Refusé');
  });

  it('sets error signal on API failure', async () => {
    mockApi.getLogs.mockReturnValue(throwError(() => new Error('fail')));
    component.fetchLogs();
    fixture.detectChanges();
    await fixture.whenStable();
    expect(component.error()).toBe("Impossible de charger l'historique.");
    expect(component.isLoading()).toBe(false);
  });
});

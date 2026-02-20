import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { vi } from 'vitest';

import { Eval } from './eval';
import { RagApiService, EvalReport } from '../../services/rag-api.service';

const mockReport: EvalReport = {
  run_at: '2024-01-01T10:00:00Z',
  faithfulness: 0.9,
  answer_relevancy: 0.8,
  context_recall: 0.7,
  per_question: [
    { question: 'Q1', expected_source: 'doc1', source_found: true, answer_length: 120 },
    { question: 'Q2', expected_source: 'doc2', source_found: false, answer_length: 80 },
  ],
};

describe('Eval', () => {
  let component: Eval;
  let fixture: ComponentFixture<Eval>;
  let mockApi: {
    getEvalReport: ReturnType<typeof vi.fn>;
    runEval: ReturnType<typeof vi.fn>;
  };

  beforeEach(async () => {
    mockApi = {
      getEvalReport: vi.fn().mockReturnValue(of(mockReport)),
      runEval: vi.fn().mockReturnValue(of({ status: 'ok', scores: {} })),
    };

    await TestBed.configureTestingModule({
      imports: [Eval],
      providers: [{ provide: RagApiService, useValue: mockApi }],
    }).compileComponents();

    fixture = TestBed.createComponent(Eval);
    component = fixture.componentInstance;
    fixture.detectChanges();
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load report on init', () => {
    expect(mockApi.getEvalReport).toHaveBeenCalled();
    expect(component.report()).toEqual(mockReport);
    expect(component.isLoading()).toBe(false);
  });

  it('avg() returns the mean of the 3 scores', () => {
    expect(component.avg()).toBeCloseTo((0.9 + 0.8 + 0.7) / 3);
  });

  it('avg() returns 0 when report is null', () => {
    component.report.set(null);
    expect(component.avg()).toBe(0);
  });

  it('runEval() calls the API and refreshes the report', async () => {
    component.runEval();
    fixture.detectChanges();
    await fixture.whenStable();
    expect(mockApi.runEval).toHaveBeenCalled();
    expect(mockApi.getEvalReport).toHaveBeenCalledTimes(2);
    expect(component.isRunning()).toBe(false);
  });

  it('sets error signal when getEvalReport fails', async () => {
    mockApi.getEvalReport.mockReturnValue(throwError(() => new Error('fail')));
    component.fetchReport();
    fixture.detectChanges();
    await fixture.whenStable();
    expect(component.error()).toBe('Aucun rapport disponible. Lancez une évaluation.');
    expect(component.isLoading()).toBe(false);
  });

  it('sets error signal when runEval fails', async () => {
    mockApi.runEval.mockReturnValue(throwError(() => new Error('fail')));
    component.runEval();
    fixture.detectChanges();
    await fixture.whenStable();
    expect(component.error()).toBe("Erreur lors de l'évaluation.");
    expect(component.isRunning()).toBe(false);
  });
});

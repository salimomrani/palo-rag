import { Component, signal, inject, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { DatePipe, DecimalPipe } from '@angular/common';
import { RagApiService, EvalReport } from '../../services/rag-api.service';

@Component({
  selector: 'app-eval',
  standalone: true,
  imports: [DatePipe, DecimalPipe],
  templateUrl: './eval.html',
  styleUrls: ['./eval.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Eval implements OnInit {
  private readonly api = inject(RagApiService);

  report = signal<EvalReport | null>(null);
  isLoading = signal(true);
  isRunning = signal(false);
  error = signal<string | null>(null);

  ngOnInit(): void {
    this.fetchReport();
  }

  fetchReport(): void {
    this.isLoading.set(true);
    this.error.set(null);
    this.api.getEvalReport().subscribe({
      next: (data) => {
        this.report.set(data);
        this.isLoading.set(false);
      },
      error: () => {
        this.error.set('Aucun rapport disponible. Lancez une évaluation.');
        this.isLoading.set(false);
      },
    });
  }

  runEval(): void {
    this.isRunning.set(true);
    this.error.set(null);
    this.api.runEval().subscribe({
      next: () => {
        this.fetchReport();
        this.isRunning.set(false);
      },
      error: () => {
        this.error.set("Erreur lors de l'évaluation.");
        this.isRunning.set(false);
      },
    });
  }

  avg(): number {
    const r = this.report();
    if (!r) return 0;
    return (r.faithfulness + r.answer_relevancy + r.context_recall) / 3;
  }
}

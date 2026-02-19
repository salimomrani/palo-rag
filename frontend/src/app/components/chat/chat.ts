import { Component, signal, computed, inject, ChangeDetectionStrategy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { RagApiService, QueryResponse } from '../../services/rag-api.service';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: { file: string; score: number }[];
  confidence?: number;
  rejected?: boolean;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [FormsModule, DecimalPipe],
  templateUrl: './chat.html',
  styleUrls: ['./chat.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Chat {
  private readonly api = inject(RagApiService);

  prompt = signal('');
  messages = signal<Message[]>([]);
  isLoading = signal(false);
  error = signal<string | null>(null);

  canSend = computed(() => this.prompt().trim().length > 0 && !this.isLoading());

  sendMessage(): void {
    if (!this.canSend()) return;

    const question = this.prompt().trim();
    this.messages.update((msgs) => [...msgs, { role: 'user', content: question }]);
    this.prompt.set('');
    this.isLoading.set(true);
    this.error.set(null);

    this.api.query(question).subscribe({
      next: (res: QueryResponse) => {
        this.messages.update((msgs) => [
          ...msgs,
          {
            role: 'assistant',
            content: res.answer,
            sources: res.sources,
            confidence: res.confidence_score,
          },
        ]);
        this.isLoading.set(false);
      },
      error: (err) => {
        const detail = err?.error?.detail;
        this.error.set(detail ?? 'Erreur de communication avec le RAG.');
        this.isLoading.set(false);
      },
    });
  }

  onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }
}

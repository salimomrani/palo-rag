import { Component, signal, computed, inject, ChangeDetectionStrategy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { RagApiService } from '../../services/rag-api.service';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: { source: string; excerpt: string; score: number }[];
  confidence?: number;
  lowConfidence?: boolean;
  streaming?: boolean;
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
    const msgId = crypto.randomUUID();

    this.messages.update((msgs) => [
      ...msgs,
      { id: crypto.randomUUID(), role: 'user', content: question },
      { id: msgId, role: 'assistant', content: '', streaming: true },
    ]);
    this.prompt.set('');
    this.isLoading.set(true);
    this.error.set(null);

    this.api.streamQuery(question).subscribe({
      next: (event) => {
        if (event.type === 'meta') {
          const seen = new Map<string, { source: string; excerpt: string; score: number }>();
          for (const s of event.sources) {
            if (!seen.has(s.source) || s.score > seen.get(s.source)!.score) seen.set(s.source, s);
          }
          this.messages.update((msgs) =>
            msgs.map((m) =>
              m.id === msgId
                ? {
                    ...m,
                    sources: [...seen.values()].sort((a, b) => b.score - a.score),
                    confidence: event.confidence_score,
                    lowConfidence: event.low_confidence,
                  }
                : m,
            ),
          );
        } else if (event.type === 'token') {
          this.messages.update((msgs) =>
            msgs.map((m) => (m.id === msgId ? { ...m, content: m.content + event.content } : m)),
          );
        } else if (event.type === 'done') {
          this.messages.update((msgs) =>
            msgs.map((m) => (m.id === msgId ? { ...m, streaming: false } : m)),
          );
          this.isLoading.set(false);
        }
      },
      error: (err) => {
        this.messages.update((msgs) => msgs.filter((m) => m.id !== msgId));
        this.error.set(err?.detail ?? 'Erreur de communication avec le RAG.');
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

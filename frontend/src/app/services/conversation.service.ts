import { Injectable, inject, signal } from '@angular/core';
import { ConversationDetail, ConversationSummary, RagApiService } from './rag-api.service';

@Injectable({ providedIn: 'root' })
export class ConversationService {
  private readonly api = inject(RagApiService);

  private _historyOffset = 0;
  private _historyLimit = 50;

  readonly sessionId: string;
  readonly historyOpen = signal(false);
  readonly conversations = signal<ConversationSummary[]>([]);
  readonly selectedConversation = signal<ConversationDetail | null>(null);
  readonly hasMore = signal(false);

  constructor() {
    const stored = sessionStorage.getItem('palo_session_id');
    if (stored) {
      this.sessionId = stored;
    } else {
      this.sessionId = crypto.randomUUID();
      sessionStorage.setItem('palo_session_id', this.sessionId);
    }
  }

  loadHistory(limit = 50, offset = 0): void {
    this._historyLimit = limit;
    this._historyOffset = 0;
    this.api.getHistory(limit, offset).subscribe((data) => {
      this.conversations.set(data);
      this.hasMore.set(data.length === limit);
    });
  }

  loadMore(): void {
    this._historyOffset += this._historyLimit;
    this.api.getHistory(this._historyLimit, this._historyOffset).subscribe((data) => {
      this.conversations.update((existing) => [...existing, ...data]);
      this.hasMore.set(data.length === this._historyLimit);
    });
  }

  loadConversation(id: string): void {
    this.api.getConversation(id).subscribe((data) => this.selectedConversation.set(data));
  }

  deleteConversation(sessionId: string): void {
    this.api.deleteConversation(sessionId).subscribe(() => {
      this.conversations.update((list) => list.filter((c) => c.session_id !== sessionId));
      if (this.selectedConversation()?.session_id === sessionId) {
        this.selectedConversation.set(null);
      }
    });
  }

  toggleHistory(): void {
    this.historyOpen.update((v) => !v);
  }
}

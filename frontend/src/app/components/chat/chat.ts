import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrls: ['./chat.scss'],
})
export class Chat {
  prompt: string = '';
  messages: Array<{ role: 'user' | 'assistant'; content: string; sources?: any[] }> = [];
  isLoading: boolean = false;
  error: string | null = null;

  constructor(private api: ApiService) {}

  sendMessage() {
    if (!this.prompt.trim()) return;

    this.messages.push({ role: 'user', content: this.prompt });
    const currentPrompt = this.prompt;
    this.prompt = '';
    this.isLoading = true;
    this.error = null;

    this.api.query(currentPrompt).subscribe({
      next: (res) => {
        this.messages.push({
          role: 'assistant',
          content: res.answer,
          sources: res.sources,
        });
        this.isLoading = false;
      },
      error: (err) => {
        console.error(err);
        this.error = 'Une erreur est survenue lors de la communication avec le RAG.';
        this.isLoading = false;
      },
    });
  }
}

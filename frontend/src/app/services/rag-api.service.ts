import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface QueryResponse {
  answer: string;
  sources: { source: string; excerpt: string; score: number }[];
  confidence_score: number;
  low_confidence: boolean;
}

export interface IngestResponse {
  document_id: string;
  name: string;
  chunk_count: number;
}

export interface Document {
  id: string;
  name: string;
  chunk_count: number;
  ingested_at: string;
}

export interface LogEntry {
  id: number;
  timestamp: string;
  question_masked: string;
  answer: string | null;
  faithfulness_score: number | null;
  similarity_scores: { document_id: string; score: number }[];
  rejected: boolean;
  rejection_reason: string | null;
}

@Injectable({ providedIn: 'root' })
export class RagApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  query(question: string): Observable<QueryResponse> {
    return this.http.post<QueryResponse>(`${this.apiUrl}/query`, { question });
  }

  ingest(file: File): Observable<IngestResponse> {
    return new Observable((observer) => {
      const reader = new FileReader();
      reader.onload = () => {
        this.http
          .post<IngestResponse>(`${this.apiUrl}/ingest`, {
            text: reader.result as string,
            name: file.name,
          })
          .subscribe(observer);
      };
      reader.onerror = () => observer.error(reader.error);
      reader.readAsText(file);
    });
  }

  getDocuments(): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.apiUrl}/documents`);
  }

  deleteDocument(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/documents/${id}`);
  }

  getLogs(): Observable<LogEntry[]> {
    return this.http.get<LogEntry[]>(`${this.apiUrl}/logs`);
  }
}

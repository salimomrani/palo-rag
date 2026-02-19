import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface QueryResponse {
  answer: string;
  sources: { file: string; score: number }[];
  confidence_score: number;
}

export interface IngestResponse {
  document_id: string;
  chunks_count: number;
  message: string;
}

export interface Document {
  id: string;
  filename: string;
  chunks_count: number;
  created_at: string;
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
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<IngestResponse>(`${this.apiUrl}/ingest`, formData);
  }

  getDocuments(): Observable<Document[]> {
    return this.http.get<Document[]>(`${this.apiUrl}/documents`);
  }

  getLogs(): Observable<LogEntry[]> {
    return this.http.get<LogEntry[]>(`${this.apiUrl}/logs`);
  }
}

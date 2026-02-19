import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:8000/api/v1';

  constructor(private http: HttpClient) {}

  query(prompt: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/query`, { question: prompt });
  }

  ingest(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/ingest`, formData);
  }

  getLogs(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/logs`);
  }
}

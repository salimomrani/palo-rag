import { Injectable, effect, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

import { environment } from '../../environments/environment';

interface LoginResponse {
  access_token: string;
  token_type: 'bearer';
}

const AUTH_TOKEN_STORAGE_KEY = 'auth_token';

function decodeJwtPayload(token: string): { exp?: number } | null {
  try {
    const [, payload] = token.split('.');
    if (!payload) return null;
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
    const padded = normalized + '='.repeat((4 - (normalized.length % 4)) % 4);
    const decoded = atob(padded);
    return JSON.parse(decoded) as { exp?: number };
  } catch {
    return null;
  }
}

function isExpiredJwt(token: string): boolean {
  const payload = decodeJwtPayload(token);
  if (!payload?.exp) return false;
  return payload.exp <= Math.floor(Date.now() / 1000);
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  readonly isAuthenticated = signal(false);
  readonly token = signal<string | null>(null);

  constructor() {
    const storedToken = localStorage.getItem(AUTH_TOKEN_STORAGE_KEY);
    if (storedToken && !isExpiredJwt(storedToken)) {
      this.token.set(storedToken);
      this.isAuthenticated.set(true);
    } else if (storedToken) {
      localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
    }

    effect(() => {
      const currentToken = this.token();
      if (currentToken) {
        localStorage.setItem(AUTH_TOKEN_STORAGE_KEY, currentToken);
        return;
      }

      localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
    });
  }

  login(username: string, password: string): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(`${this.apiUrl}/auth/login`, { username, password })
      .pipe(
        tap((response) => {
          this.token.set(response.access_token);
          this.isAuthenticated.set(true);
        }),
      );
  }

  logout(): void {
    this.token.set(null);
    this.isAuthenticated.set(false);
  }
}

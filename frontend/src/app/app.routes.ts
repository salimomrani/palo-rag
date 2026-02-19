import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'chat', pathMatch: 'full' },
  {
    path: 'chat',
    loadComponent: () => import('./components/chat/chat').then((m) => m.Chat),
  },
  {
    path: 'ingest',
    loadComponent: () => import('./components/ingest/ingest').then((m) => m.Ingest),
  },
  {
    path: 'logs',
    loadComponent: () => import('./components/logs/logs').then((m) => m.Logs),
  },
];

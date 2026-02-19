import { Routes } from '@angular/router';
import { Chat } from './components/chat/chat';
import { Ingest } from './components/ingest/ingest';
import { Logs } from './components/logs/logs';

export const routes: Routes = [
  { path: '', redirectTo: 'chat', pathMatch: 'full' },
  { path: 'chat', component: Chat },
  { path: 'ingest', component: Ingest },
  { path: 'logs', component: Logs },
];

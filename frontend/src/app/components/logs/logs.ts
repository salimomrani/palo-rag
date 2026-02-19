import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-logs',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './logs.html',
  styleUrls: ['./logs.scss'],
})
export class Logs implements OnInit {
  logs: any[] = [];
  isLoading = true;
  error: string | null = null;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.fetchLogs();
  }

  fetchLogs() {
    this.isLoading = true;
    this.api.getLogs().subscribe({
      next: (data) => {
        this.logs = data;
        this.isLoading = false;
      },
      error: (err) => {
        console.error(err);
        this.error = 'Impossible de charger l\'historique des logs.';
        this.isLoading = false;
      },
    });
  }
}

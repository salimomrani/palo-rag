import { Component, signal, inject, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { RagApiService, Document } from '../../services/rag-api.service';

@Component({
  selector: 'app-ingest',
  standalone: true,
  imports: [],
  templateUrl: './ingest.html',
  styleUrls: ['./ingest.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Ingest implements OnInit {
  private readonly api = inject(RagApiService);

  selectedFile = signal<File | null>(null);
  isUploading = signal(false);
  successMsg = signal<string | null>(null);
  error = signal<string | null>(null);
  documents = signal<Document[]>([]);
  isLoadingDocs = signal(false);

  ngOnInit(): void {
    this.loadDocuments();
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;
    this.selectedFile.set(file);
    this.successMsg.set(null);
    this.error.set(null);
  }

  uploadFile(): void {
    const file = this.selectedFile();
    if (!file) return;

    this.isUploading.set(true);
    this.successMsg.set(null);
    this.error.set(null);

    this.api.ingest(file).subscribe({
      next: (res) => {
        this.successMsg.set(`"${file.name}" ingéré — ${res.chunks_count} chunks.`);
        this.selectedFile.set(null);
        this.isUploading.set(false);
        this.loadDocuments();
        const el = document.getElementById('fileInput') as HTMLInputElement | null;
        if (el) el.value = '';
      },
      error: (err) => {
        this.error.set(err?.error?.detail ?? "Erreur lors de l'envoi.");
        this.isUploading.set(false);
      },
    });
  }

  private loadDocuments(): void {
    this.isLoadingDocs.set(true);
    this.api.getDocuments().subscribe({
      next: (docs) => {
        this.documents.set(docs);
        this.isLoadingDocs.set(false);
      },
      error: () => {
        this.isLoadingDocs.set(false);
      },
    });
  }
}
